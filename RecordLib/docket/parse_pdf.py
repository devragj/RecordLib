from typing import Union, BinaryIO, Tuple, Callable, List, Optional
from RecordLib.common import Charge, Sentence, SentenceLength
from RecordLib.person import Person
from RecordLib.case import Case
from RecordLib.grammars.docket import (
    docket_sections, docket_sections_nonterminals, common_terminals, 
    section_grammars)
from RecordLib.CustomNodeVisitorFactory import CustomVisitorFactory
from RecordLib.docket.custom_parsing_funcs import docket_sections_custom_nodevisitors
from RecordLib.parsingutilities import get_text_from_pdf
from parsimonious import Grammar
import parsimonious
from lxml import etree
import logging
import re
from datetime import datetime

def text_to_pages(txt: str) -> str:
    """ Convert raw text of a docket to an xml-string, where the nodes are the pages and sections of the docket.
    
    i.e. 
    <docket>
        <page>
            <section> 
            </section
        </page>
        <page>
            <section_continued>
            </section_continued>
        </page>
    </docket>"""
    grammar = Grammar(docket_sections)
    try:
        nodes = grammar.parse(txt)
        visitor = CustomVisitorFactory(common_terminals, 
        docket_sections_nonterminals, docket_sections_custom_nodevisitors).create_instance()
        return visitor.visit(nodes)
    except Exception as e:
        slines = txt.split("\n")
        logging.error("text_to_pages failed.")
        return "<docket></docket>"


def create_section_header_remover(section_name: str) -> Callable:
    """
    Return a function that can strip the header lines from a docket section.

    Each section has different header lines, and these lines need to be removed 
    when a section overflows across pages, so that the header lines of a section don't end up 
    inside the body of the section.

    This needs to be flexible enough that it can remove partial headers if, for example, only 
    a few lines of header are repeated at the top of a page.

    So really, this function just identifies a list of lines, such that any of those lines that appear
    at the top of a section, they should get removed. And this function returns a function that can remove them.
    """
    lines_to_remove = []
    if section_name == "section_disposition_sentencing":
        lines_to_remove = [
            re.compile(r"\s*Disposition.*"),
            re.compile(r"\s*Case Event.*"),
            re.compile(r"\s*Sequence\/Description.*"),
            re.compile(r"\s*Sentencing Judge.*"),
            re.compile(r"\s*Sentence\/Diversion Program Type.*"),
            re.compile(r"\s*Sentence Conditions.*"),
        ]
    elif section_name == "section_charges":
        lines_to_remove = [
            re.compile(r"\s*Seq..*"),
        ]
    def section_header_remover(section_text):
        slines = section_text.split("\n")
        keep_going = True
        while keep_going:
            any_matched = False
            if len(slines) == 0: 
                break
            for patt in lines_to_remove:
                if patt.match(slines[0]):
                    del slines[:1]
                    any_matched = True
            if any_matched is False: keep_going = False
        return "\n".join(slines)
    
    return section_header_remover

def sections_from_pages(ptree: etree) -> etree:
    """
    Splice together sections in `ptree` that are separated across pages, 
    and get rid of the `page` level of the `ptree` entirely
    
    From 
    <docket>
        <page>
            <section> 
            </section
        </page>
        <page>
            <section_continued>
            </section_continued>
        </page>
    </docket>
    
    To
    <docket>
        <section>
        </section>
    </docket>
    """
    # create an empty tree to add all the other sections onto.
    stitched_xml = etree.Element("docket")
    stitched_xml.append(ptree.xpath("//header[1]")[0])
    pages = ptree.xpath("//page")
    logging.info(f"    {len(pages)} pages in this docket.")
    # Recombine a section if it carries onto the following page(s).
    combined_sections = []
    for page_num, page in enumerate(pages):
        sections = page.xpath(".//section")
        for section in sections:
            if len(combined_sections) != 0:
                #if the section last added to combined sections is the same kind of
                # section, then add the current section's text to the most recent
                # combined section's text.
                if section.xpath("@name")[0] == combined_sections[-1].xpath("@name")[0]:
                    # here is where we'd remove the overflowing header lines from this section, before
                    # appending it to the previous section.
                    section_header_remover = create_section_header_remover(section.xpath("@name")[0])
                    # strip() removes empty lines at the beginning of the section, 
                    # which is good. But it also removes spaces at the beginning of the first line with text.
                    # some grammar pieces rely on the indentation of a line to know what kind of line it is.
                    # this strip() removes that indentation.
                    section_text = "\n".join([ln for ln in section.text.split("\n") if ln.strip()]) 
                    section_text = section_header_remover(section_text)
                    # now combine the previous section with this section, because this section 
                    # is just the overflow of the last on a different page.
                    combined_sections[-1].text = "\n".join([combined_sections[-1].text.strip(), section_text])
                #else the current section is new, so add the current section to the end of combined_sections
                else:
                    combined_sections.append(section)
            else:
                combined_sections.append(section)

        [stitched_xml.append(section_node)  for section_node in combined_sections]
    last_page = pages[-1]
    if len(last_page.xpath(".//section")) == 0:
        # add the traling <body> lines to the last section in combined_sections
        last_page_body = last_page.xpath("body")[0].text
        stitched_xml.xpath("//section[last()]")[0].text += last_page_body
    docket_tree = etree.ElementTree(stitched_xml)
    return docket_tree    


def split_first_name(full_name: str) -> Tuple[str, str]:
    """
    Captions list names in 'first middle? last` order.
    This tries to break them up correctly.

    """
    names = full_name.split(" ")
    return " ".join(names[:-1]), names[-1]

def xpath_or_blank(stree: etree, xpath: str) -> str:
    """ given an etree and an xpath expression, return the value of the expression, or 
    an empty string. 
    
    A helper method"""
    try:
        return stree.xpath(xpath)[0].text.strip()
    except IndexError:
        return ""

def xpath_date_or_blank(tree: etree, xpath: str) -> Optional[datetime]:
    """ Given an etree and an xpath expression, return the value of the expression 
    as a date, or None"""
    try:
        return datetime.strptime(tree.xpath(xpath)[0].text.strip(), r"%m/%d/%Y")
    except (IndexError, ValueError) as e:
        return None

def xpath_or_empty_list(tree: etree, xpath: str) -> List[str]:
    """ Given an etree, find a list of strings, or return an empty list."""
    return [el.text.strip() for el in tree.xpath(xpath)]

def str_to_money(money: str) -> float:
    """ 
    Turn a money string into a float.
    """
    if money.strip() == "": return 0
    return float(money.replace("$", "").replace(",","").replace("(","").replace(")",""))

def get_person(stree: etree) -> Person:
    """
    Extract a Person the xml of a docket, parsed into sections.

    Returns an empty Person object on errors.

    Args:
        stree: xml tree of a docket, parsed into a header and some number of sections
    
    Returns:
        a Person object
    """
    try:
        name = stree.xpath("docket/header/caption/defendant_line")[0].text.strip()
        first_name, last_name = split_first_name(name)
    except IndexError:
        first_name = ""
        last_name = ""    

    aliases = xpath_or_empty_list(stree, "//alias")
    date_of_birth = xpath_date_or_blank(stree, "//birth_date")
    return Person(first_name = first_name, last_name = last_name, 
                  date_of_birth = date_of_birth,
                  aliases = aliases)
    
def get_sentences(stree: etree) -> List[Sentence]:
    """Find the sentences in a sequence (as an xml tree) from a disposition section of a docket.
    """
    sequence_date = xpath_date_or_blank(stree, "//action_date")
    sentences = stree.xpath("//sentence_info")
    sentences = [
        Sentence(
            sentence_date = sequence_date,
            sentence_type = xpath_or_blank(s, "//program"),
            sentence_period = "...",
            sentence_length = SentenceLength(
                min_time = (
                    s.xpath("//sentence_length/min_length/time")[0].text,
                    s.xpath("//sentence_length/min_length/unit")[0].text),
                max_time = ( 
                    s.xpath("//sentence_length/min_length/time")[0].text,
                    s.xpath("//sentence_length/min_length/unit")[0].text
                    ),
            )
        )
        for s in sentences
    ]
    return sentences


def get_charges(stree: etree) -> List[Charge]:
    """
    Find a list of the charges in a parsed docket.
    """
    # find the charges in the Charges section
    charges = stree.xpath("//section[@name='section_charges']//charge")
        # charges is temporarily a list of tuples of [(sequence_num, Charge)]
    charges = [
        (
            xpath_or_blank(charge, "./seq_num"),
            Charge(
                offense = xpath_or_blank(charge, "./statute_description"),
                grade = xpath_or_blank(charge, "./grade"),
                statute = xpath_or_blank(charge, "./statute"),
                disposition = "Unknown",
                disposition_date = None,
                sentences = [],
            )
        )
        for charge in charges
    ]
    # figure out the disposition dates by looking for a final disposition date that matches a charge.
    final_disposition_events = stree.xpath("//section[@name='section_disposition_sentencing']//case_event[case_event_desc_and_date/is_final[contains(text(),'Final Disposition')]]")
    for final_disp_event in final_disposition_events:
        final_disp_date = xpath_date_or_blank(final_disp_event, ".//case_event_date")
        applies_to_sequences = xpath_or_empty_list(final_disp_event, ".//sequence_number")
        for seq_num in applies_to_sequences:    
            # set the final_disp date for the charge with sequence number seq_num
            for sn, charge in charges:
                if sn == seq_num:
                    charge.disposition_date = final_disp_date


    # Figure out the disposition of each charge from the disposition section.
    #   Do this by finding the last sequence in the disposition section for 
    #   the sequence with seq_num. The disposition of the charge is that 
    #   sequence's disposition. Sentence is in that xml element too.
    try:
        disposition_section = stree.xpath("//section[@name='section_disposition_sentencing']")[0]
        for seq_num, charge in charges:
            try:
                # seq is the last sequence for the charge seq_num.
                seq = disposition_section.xpath(
                    f"./disposition_section/disposition_subsection/disposition_details/case_event/sequences/sequence[sequence_number/text()=' {seq_num} ']")[-1]
                charge.disposition = xpath_or_blank(seq, "./offense_disposition")
                charge.sentences = get_sentences(seq)
            except IndexError:
                continue
    except IndexError:
        pass
    return [c for i,c in  charges]


def get_case(stree: etree) -> Case:
    """
    Extract a list of Cases from the xml of a docket that has been parsed into sections.

    Returns and empty Case on failure.

    Args:
         stree: xml tree of a docket, parsed into a header and some number of sections
    
    Returns:
        a Cases object. 
    
    """
    county = xpath_or_blank(stree, "/docket/header/court_name/county")
    docket_number = xpath_or_blank(stree, "/docket/header/docket_number")
    otn = xpath_or_blank(stree, "//section[@name='section_case_info']//otn")
    dc = xpath_or_blank(stree, "//section[@name='section_case_info']//dc")
    judge = xpath_or_blank(stree, "//section[@name='section_case_info']//judge_assigned")
    affiant = xpath_or_blank(stree, "//arresting_officer")
    arresting_agency = xpath_or_blank(stree, "//arresting_agency")
    complaint_date = xpath_date_or_blank(stree, "//section[@name='section_status_info']//complaint_date")
    arrest_date = xpath_date_or_blank(stree, "//section[@name='section_status_info']//arrest_date")
    status = xpath_or_blank(stree, "//section[@name='section_status_info']//case_status")

    # If the case's status is Closed, find the disposition date by finding the last status event date.
    # TODO I'm not sure this is the right date. Is the 'disposition date' the date the case status changed to 
    #       Completed, or the date of "Sentenced/Penalty Imposed"
    if re.search("close", status, re.IGNORECASE):
        disposition_date = xpath_or_blank(stree, "//section[@name='section_status_info']//status_event[1]/status_date")
        try:
            disposition_date = datetime.strptime(disposition_date, r"%m/%d/%Y")
        except ValueError:
            #logging.error(f"disposition date {disposition_date} did not parse.")
            disposition_date = None
    else: 
        disposition_date = None
    
    
    # fines and costs
    total_fines = str_to_money(xpath_or_blank(stree, "//section[@name='section_case_financal_info']/case_financial_info/grand_toals/assessed"))
    fines_paid = str_to_money(xpath_or_blank(stree, "//section[@name='section_case_financial_info']/case_financial_info/grant_totals/payments"))
    # charges
    charges = get_charges(stree) 

    return Case(
        status=status, county=county, docket_number=docket_number, otn=otn, 
        dc=dc, charges=charges,total_fines=total_fines, fines_paid=fines_paid,
        arrest_date=arrest_date, disposition_date=disposition_date, 
        judge=judge, affiant=affiant, arresting_agency=arresting_agency, 
        complaint_date=complaint_date)

def parse_pdf(pdf: Union[BinaryIO, str], tempdir: str = "tmp") -> Tuple[Person, Case]:
    """
    Parse the a pdf of a criminal record docket. 

    The 'see' references are to the DocketParse library, which also parses pdf dockets. 

    Args:
        pdf: a binary reader or a string path to a pdf file.
        tempdir: The pdf must be written to txt with pdftotext, so we need a temporary directory for it.
    
    Returns:
        The Person to whom the docket relates, and the Case to which the Docket relates.
    """
    # a list of strings
    errors = []
    # pdf to raw text
    txt = get_text_from_pdf(pdf, tempdir=tempdir)
    # text to xml sections (see DocketParse.sectionize). This handles page breaks.
    pages_tree = etree.fromstring(text_to_pages(txt))
    sections_tree = sections_from_pages(pages_tree)
    # parse individual sections with grammars for those sections
    # TODO add try catch blocks that allow for continuing even after certain parts fail, like
    #       if a single section fails to parse.
    for section_name, grammar, terminals, nonterminals, custom_visitors in section_grammars:
        try:
            section = sections_tree.xpath(f"//section[@name='{section_name}']")[0]
            # remove blank lines at the ends of the section.
            section_text = "\n".join([ln for ln in section.text.split("\n") if ln.strip()]) 
            grammar = Grammar(grammar)
            try:
                nodes = grammar.parse(section_text)
            except Exception as e:
                slines = section_text.split("\n")
                errors.append(f"    Text for {section_name} failed to parse.")
                logging.error(f"    Text for {section_name} failed to parse.")
                continue
            visitor = CustomVisitorFactory(terminals, nonterminals, custom_visitors).create_instance()
            parsed_section_text = visitor.visit(nodes)
            parsed_section_xml = etree.fromstring(parsed_section_text)
            # replace original unparsed section's text w/ the parsed xml.
            sections_tree.xpath(f"//section[@name='{section_name}']")[0].text = ""
            sections_tree.xpath(f"//section[@name='{section_name}']")[0].append(parsed_section_xml)
        except (Exception, IndexError) as e:
            # not all dockets have all sections, so not being able to find a section is not
            # necessarily an error.
            #slines = section_text.split("\n")
            logging.info(f"    Could not find section {section_name}")
            #slines = etree.tostring(sections_tree, encoding="unicode").split("\n")
    # extract Person and Case information from xml.
    # i.e. defendant_name = section_tree.xpath("//caption/name")[0].text
    defendant = get_person(sections_tree)
    case = get_case(sections_tree)
    return  defendant, case, errors