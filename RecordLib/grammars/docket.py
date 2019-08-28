from RecordLib.docket.custom_parsing_funcs import visit_content
from RecordLib.summary.utilities import visit_sentence_length

# Notes on adding a new section grammar
# 
# First, create the grammar docstring.
# Then create a list of the section's terminals
# Optionally create a list of the sections's nonterminals
# write any custom node visitor functions
# add this grammar, nonterminals, terminals, custom visitors as a tuple to 'section_grammars' at the end of this module.
# edit the section_header_remover function in parse_pdf.py to remove headers from the section on pages 
#  after the first page.

common_terminals = [
    "ws"
    "number",
    "number_w_comma",
    "date",
    "forward_slash",
    "single_content_char",
    "content_char_no_ws",
    "section_symbol",
    "new_line",
    "money",
]

docket_sections_nonterminals = [
    "docket",
    "page",
    "header",
    "rest_of_header",
    "court_name",
    "docket_number",
    "caption",
    "county",
    "commonwealth_line",
    "defendant_line",
    "aliases",
    "alias",
    "body",
    "section_case_info",
    "section_petitioner_information",
    "section_related_cases",
    "section_status_info",
    "section_calendar_events",
    "section_confinement_info",
    "section_defendant_info",
    "section_case_participants",
    "section_bail_info",
    "section_charges",
    "section_disposition_sentencing",
    "section_commonwealth_info",
    "section_entries",
    "section_payment_plan",
    "section_case_financial_info",
    "footer"
]

useful_symbols = \
r"""
    # nonterminals, but quiet ones that shouldn't create xml <tags>
    content = single_content_char*
    line = single_content_char* new_line
    empty_line = ws* (new_line / end_of_input)
    word = content_char_no_ws+
    words = word (ws words)*

    # quiet terminals with content that should just disappear
    page_break = "\f" / '\x0c'
    end_of_input = !~"."

    # Loud Terminals (include in list of terminals, so content of the
    # node ends up in the output)
    money = ~r"\(?\$[0-9\.,]+\)?"
    ws = " "
    date = number forward_slash number forward_slash number
    number = ~r"[0-9]"+
    number_w_comma = ~r"[0-9,]"+
    number_w_dec_hyp = ~r"[0-9\.-]"+
    forward_slash = "/"
    section_symbol = "§"
    single_content_char =  ~r"[\\\“\”a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§\+\<\>\!{}]"i
    content_char_no_ws =  ~r"[\\\“\”a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§\+\<\>\!{}]"i
    new_line = "\n"
    ws = " "
"""


docket_sections = \
r"""
###
#  This grammar separates dockets into sections. It goes a little more into the
#  details of the case info section than necessary. It may be a good idea
#  later to take that out and move it to a separate sub-grammar and
#  sub-NodeVisitor.
#
#  Also, its messy and doesn't use common_terminals because its mostly copied from NateV's project
#  DocketParse.
###
docket = page+
page = header body? footer page_break?

header = ws* court_name new_line line docket_number rest_of_header caption?
rest_of_header = (line !section_case_info_start !caption)+ line
court_name = ~"COURT OF COMMON PLEAS OF"i ws+ county ws*
county = word ws+ ~"COUNTY"i
docket_number = content new_line?
caption = (commonwealth_line line line defendant_line) / in_re
commonwealth_line = ws* ~"Commonwealth of Pennsylvania"i ws* new_line
defendant_line = content new_line

in_re = ws* ~"In Re:.*"i ws* new_line (line !section)+ line



# The body of a page might start with a section.
# It might also start with a few lines of the previous section, before a section.
# Or it might have just a few lines, and no new section.
body = ((section !start_of_footer)* section) /
       (line (section !start_of_footer)* section) /
       (line line (section !start_of_footer)* section) /
       (line line line (section !start_of_footer)* section) /
       (line line line line (section !start_of_footer)* section) /
       (line line line line line empty_line* (section !start_of_footer)* section) /
       (line line line line line line empty_line* (section !start_of_footer)* section) /
       (line line line line line line line empty_line* (section !start_of_footer)* section) /
       (((line / empty_line) !start_of_footer !section)+ (line / empty_line) &start_of_footer) 
       # this last rule is a catch-all meant to only catch pages
       # with a few extra lines in htme  
section = section_case_info /
          section_related_cases /
          section_status_info /
          section_calendar_events /
          section_confinement_info /
          section_defendant_info /
          section_case_participants /
          section_bail_info /
          section_charges /
          section_disposition_sentencing /
          section_commonwealth_info /
          section_entries /
          section_payment_plan /
          section_case_financial_info /
          section_petitioner_info


section_case_info_start = (ws* ~"CASE INFORMATION"i)
section_case_info = (section_case_info_start new_line) section_body
section_related_cases = (ws* ~"RELATED CASES"i new_line) section_body
section_status_info = (ws* ~"STATUS INFORMATION"i new_line) section_body
section_calendar_events = (ws* ~"calendar events"i new_line)  section_body
section_confinement_info = (ws* ~"CONFINEMENT INFORMATION") section_body
section_defendant_info =  (ws* ~"defendant information"i new_line) section_body
section_case_participants = (ws* ~"case participants"i new_line) section_body
section_bail_info = (ws* ~"bail information"i new_line) section_body
section_charges = (ws* ~"charges"i new_line) section_body
section_disposition_sentencing = (ws* ~"disposition sentencing/penalties"i new_line) section_body
section_commonwealth_info =  (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) section_body
section_entries = (ws* ~"entries"i new_line)  section_body
section_payment_plan = (ws* ~"payment plan summary"i new_line) section_body
section_case_financial_info = (ws* ~"case financial information"i new_line) section_body
section_petitioner_info = (ws* ~r"petitioner information"i new_line) section_body

section_body = (line &end_of_section) / ((line !end_of_section)+ line)
#This revision is meant to deal with sections that have just the header on a
# page, followed by the footer, and no content in the section.
# section_body = (line !end_of_section)+ line

end_of_section = start_of_footer / next_section_header

next_section_header = (ws* ~"CASE INFORMATION"i new_line) /
                      (ws* ~"RELATED CASES"i new_line) /
                      (ws* ~"STATUS INFORMATION"i new_line) /
                      (ws* ~"calendar events"i new_line) /
                      (ws* ~"CONFINEMENT INFORMATION") /
                      (ws* ~"defendant information"i new_line) /
                      (ws* ~"case participants"i new_line) /
                      (ws* ~"bail information"i new_line) /
                      (ws* ~"charges"i new_line) /
                      (ws* ~"disposition sentencing/penalties"i new_line) /
                      (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) /
                      (ws* ~"entries"i new_line) /
                      (ws* ~"payment plan summary"i new_line) /
                      (ws* ~"case financial information"i new_line) / 
                      (ws* ~"petitioner information"i new_line)



start_of_footer = (ws* ~"CPCMS 9082" content new_line)
footer = start_of_footer line+
""" + useful_symbols


defendant_info_section_nonterminals = ["defendant_information", "birth_date", "location", "aliases", "alias"]

defendant_info_section = \
r"""
#Nonterminals
defendant_information = new_line? birth_info 
                         (new_line empty_line* aliases empty_line*)?

alias_lines = new_line empty_line* aliases empty_line*

birth_info = "Date Of Birth:" ws+ (birth_date ws+)? "City/State/Zip:" ws* location?
birth_date = date+ 
location = words+
aliases = ws* "Alias Name" ws* new_line 
          (alias new_line?)*
alias = words+
""" + useful_symbols

disposition_section_terminals = ["date", "fraction", "grade", "no_further_penalty", "single_char_no_comma_or_ws",
"single_content_char", "number","forward_slash","single_content_char_no_comma","single_content_char_no_ws",
"single_content_char","single_letter_no_ws", "comma", "ws"]
disposition_section_nonterminals = ["disposition_section", "disposition_subsection", "disposition_type", "disposition_details", 
"case_event", "case_event_desc", "code_section", "case_event_desc_and_date", "is_final", "sequences", 
"sequence", "sequence_number", "sequence_description", "offense_disposition", "sequence_description_continued", 
"judge_action", "sentence_info", "program", "length_of_sentence", "program_length_start",
"extra_sentence_details", "heading", "footer", "time_served", "action_date"]

disposition_section = \
r"""
disposition_section = ws* new_line? disposition_subsection+ new_line? footer?

# this lines at the top of the disposition section that just identify the different columns
                     

disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line single_content_char_no_ws content new_line

disposition_details = ws ws+ !start_of_footer case_event+

case_event = new_line? case_event_desc_and_date sequences? new_line?

case_event_desc_and_date = ws* case_event_desc ws ws+ date ws ws ws+ is_final (new_line / end_of_input)
case_event_desc = (word ws)+

date = number forward_slash number forward_slash number
is_final = (word ws word) / word

sequences = sequence+
sequence = sequence_start new_line? sequence_details?
sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ 
                 offense_disposition ws ws ws+ grade? ws* code_section 
sequence_number = number+ &ws
sequence_description = (word ws)+
offense_disposition = (word ws)+
code_section = single_content_char+


sequence_details = !sequence_start sequence_description_continued* charge_replaced? judge_action*

# The complexity of the following rule is necessary because I need to
# distinguish lines that carry over from the sequence description, which
# could be just words without commas: "intent to distribute"
# or which can contain commas, as in
# "    Replaced by 18 § 2701 §§ A3, Simple Assault"
# I identify names by [words] comma [words], as in "Smith, John"
# In order to distinguish them, I'm assuming that a judge won't have more
# than two last names before the comma, and a sequence_description_continued line will
# have at least three words before any comma.
# N.B. If this turns out to be wrong, a couple other ideas might work:
# 1) Treat the "Replaced by" lines as an entirely separate optional line,
#    characterized by the presence of section symbols
# 2) Create a dictionary of judges' names, and explicitly check their names.
sequence_description_continued = (ws ws+ !number !name_line !charge_replaced word_no_comma (new_line / end_of_input)) /
                                 (ws ws+ !number !name_line !charge_replaced word_no_comma ws word_no_comma (new_line / end_of_input)) /
                                 (ws ws+ !number !name_line !charge_replaced word_no_comma ws word_no_comma  comma? ws* !date line (new_line / end_of_input)) /
                                 (ws ws+ !number !name_line !charge_replaced word_no_comma comma ws word_no_comma ws word_no_comma (ws !date word_no_comma)* (new_line / end_of_input)) /
                                 (ws ws+ ~r".*accommodation.*"i (new_line / end_of_input)) /# burglary offenses involving overnight accomm. are frequent 2-line offenses.
                                 (ws ws+ ~r".*Revoked\).*"i (new_line / end_of_input)) /# as in a disp. of (ARD Revoked).
                                 (ws ws+ ~r".*Offense.*"i (new_line / end_of_input)) /
                                 (ws ws+ ~r".*[Defendant|Parent].*"i (new_line / end_of_input)) # lines identifying an offense often start w/ a number, i.e. 1st Offense, so fail other tests.

charge_replaced = ws* "Replaced by" ws* words (new_line / end_of_input)

judge_action = name_line sentence_info*
sentence_info = !name_line program_length_start extra_sentence_details?

name_line = ws+ judge_name ws ws ws ws+ action_date (ws ws+ time_served)? (new_line / end_of_input)
judge_name = word_no_comma (ws word_no_comma)? comma ws word_no_comma (ws word_no_comma)? (ws word_no_comma)?
time_served = words+
action_date = date+
program_length_start = (ws ws+ no_further_penalty (new_line / end_of_input)) /
                        (ws ws+ program ws ws+ length_of_sentence (ws ws+ date)? (new_line / end_of_input))
program = word (ws word)*

extra_sentence_details = (!name_line !program_length_start !sequence_start ws+ line)*


length_of_sentence = word_or_numbers_or_fraction &(ws / new_line)
word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                                (fraction ws word_or_numbers_or_fraction) /
                                (number ws word_or_numbers_or_fraction) /
                                (word)/
                                (number)/
                                (fraction)

fraction = number forward_slash number

heading = first_heading_line 
          (ws+ "Case Event" line)?
          (ws+ "Sequence" line)?
          (ws+ "Sentencing Judge" line)?
          (ws+ "Sentence/Diversion" line)?
          (ws+ "Sentence Conditions")?
          empty_line*
first_heading_line = ws* ~"Disposition"i new_line


footer = start_of_footer line+ (words end_of_input)?
start_of_footer = (" LINKED SENTENCES:" new_line) /
                  (ws* "The following Judge Ordered Conditions are imposed:" new_line)

word_no_comma = single_char_no_comma_or_ws+
word = single_content_char_no_ws+
words = (word ws+)+ word

##Terminals
grade = ~r"[a-z0-9]"i+
no_further_penalty = ~"No Further Penalty"i
single_char_no_comma_or_ws = ~r"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]\/@§<\+]"i
line = content new_line?
content = single_content_char+
content_no_comma = single_content_char_no_comma+
content_no_ws = single_content_char_no_ws+
number = ~r"[0-9,\.]+"
forward_slash = "/"
single_content_char_no_comma =  ~r"[a-z0-9`\ \"=_\.\-\(\)\'\$\?\*%;:#&\[\]\/@§<\+]"i
single_content_char_no_ws =  ~r"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]\/@§<\+]"i
single_content_char =  ~r"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]\/@§<\+]"i
single_letter_no_ws = ~r"[a-z]"i
comma = ","
empty_line = ws* new_line
new_line = "\n"
ws = " "
end_of_input = !~"."
"""

case_financial_info_nonterminals = ["case_financial_info", "grand_totals", "assessed", "payments", "adjustments", 
"non_monetary_payments","total"]

case_financial_info = \
r"""
case_financial_info = ((line / empty_line) !grand_totals)+ (line / empty_line) grand_totals ws* new_line? 
                      (line / empty_line)* ws* words? end_of_input
grand_totals = ws* "Grand Totals:" ws+ assessed ws+ payments ws+ adjustments ws+ 
               non_monetary_payments ws+ total
assessed = money+
payments = money+
adjustments = money+
non_monetary_payments = money+
total = money+
""" + useful_symbols


charges_nonterminals = ["charges", "charges_heading", "charge", "charge_continued", 
    "seq_num", "orig_seq_num", "grade", "statute", "statute_description", "offense_date",
    "otn"]

charges = \
r"""
charges = (charges_heading new_line)? 
          (charge (new_line / end_of_input) 
          (charge_continued (new_line / end_of_input))*)+

charges_heading = ws* "Seq." ws+ "Orig Seq." ws+ "Grade" content

charge = ws+ seq_num ws+ orig_seq_num ws+ (grade ws+)? (statute ws+)? (statute_description ws+)? (offense_date ws+)? (otn ws*)?
charge_continued = ws+ !(number ws ws+) words+

seq_num = number_w_comma+
orig_seq_num = number_w_comma+
grade = words+
statute = words+
statute_description = words+
offense_date = date+
otn = words+
""" + useful_symbols

case_information_nonterminals = ["case_information", "judge_assigned", "date_filed", "initiation_date", "otn",
        "lotn", "orig_docket_no", "initial_issuing_auth", "final_issuing_auth", "arresting_agency", 
        "arresting_officer", "complaint_incident_no"]

case_information = \
r"""
case_information = (cross_court_line new_line)?
                   judge_line new_line 
                   otn_line new_line
                   issuing_auth_line new_line
                   arrest_line new_line 
                   (!complaint_line line)?
                   complaint_line (new_line / end_of_input)
                   line*
                   empty_line*
                   (content end_of_input)?

cross_court_line = ws* "Cross Court Docket Nos:" ws cross_court_docket_nos
judge_line = ws* judge_assigned_w ws+ date_filed ws+ initiation_date ws*
otn_line = ws* otn ws+ lotn ws+ orig_docket_no ws*
issuing_auth_line = ws* initial_issuing_auth ws+ final_issuing_auth ws*  
arrest_line = ws* arresting_agency ws+ arresting_officer ws*
complaint_line = ws* complaint_incident_no ws*

cross_court_docket_nos = words+
judge_assigned_w = "Judge Assigned:" judge_assigned?
judge_assigned = ws words
date_filed = "Date Filed:" (ws date)?
initiation_date = "Initiation Date:" (ws date)?
otn = "OTN:" (ws words)?
lotn = "LOTN:" (ws words)?
orig_docket_no = "Originating Docket No:" (ws words)?
initial_issuing_auth = "Initial Issuing Authority:" (ws words)?
final_issuing_auth = "Final Issuing Authority:" (ws words)?
arresting_agency = "Arresting Agency:" (ws words)?
arresting_officer = "Arresting Officer:" (ws words)?
complaint_incident_no = ~r"Complaint/Incident \#:" (ws words)?
""" + useful_symbols


status_information_nonterminals = ["status_information", "heading", "status_event", "complaint_date",
        "case_status", "arrest_date", "status_date", "status_type"]

status_information = \
r"""
status_information = heading new_line 
                     (status_event (new_line / end_of_input))+
                     empty_line*
                     (ws+ complaint_date ws* (new_line /end_of_input))?
                     empty_line*
                     (content end_of_input)?

heading = ws* "Case Status:" (ws+ case_status)? ws+ "Status Date" ws+ "Processing Status" (ws+ "Arrest Date:" ws+ arrest_date)? (ws+ complaint_date)?
case_status = words+
arrest_date = date+

status_event = ws+ status_date ws+ status_type ws* (new_line status_event_cont)* 
status_event_cont = (ws+ !date !complainet_date words)
complaint_date = "Complaint Date:" ws+ date
status_date = date+
status_type = words+

""" + useful_symbols

# default custom node_visitors. visit_content escapes special xml chars, which is why its used a lot.
custom_visitors = [("single_content_char", visit_content), ("single_content_char_no_ws", visit_content)]

# A list of tuples, 
# (name-of-section, grammar, terminals, nonterminals, custom visitor functions) 
# for parsing sections of a docket.
# 
# This has to come AFTER grammars and lists of terminals for docket sections.
section_grammars = [
    ("section_defendant_info", defendant_info_section, common_terminals, defendant_info_section_nonterminals, custom_visitors),
    ("section_disposition_sentencing", disposition_section, disposition_section_terminals, disposition_section_nonterminals, custom_visitors + [("length_of_sentence", visit_sentence_length)]),
    ("section_case_financial_info", case_financial_info, common_terminals, case_financial_info_nonterminals, custom_visitors),
    ("section_charges", charges, common_terminals, charges_nonterminals, custom_visitors),
    ("section_case_info", case_information, common_terminals, case_information_nonterminals, custom_visitors),
    ("section_status_info", status_information, common_terminals, status_information_nonterminals, custom_visitors),
]