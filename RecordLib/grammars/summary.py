from parsimonious.grammar import Grammar  # type: ignore

useful_terminals = r"""
    # nonterminals, but quiet ones that shouldn't create xml <tags>

    line = single_content_char+ new_line
    empty_line = ws* (new_line / end_of_input)
    word = content_char_no_ws+
    words = word (ws words)*

    # quiet terminals with content that should just disappear
    page_break = "\f" / '\x0c'
    end_of_input = !~"."

    # Loud Terminals (include in list of terminals, so content of the
    # node ends up in the output)
    ws = " "
    date = number forward_slash number forward_slash number
    number = ~r"[0-9]"+
    number_w_dec_hyp = ~r"[0-9\.-]"+
    forward_slash = "/"
    section_symbol = "§"
    single_content_char =  ~r"[\\\“\”a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§\+\<\>\!]"i
    content_char_no_ws =  ~r"[\\\“\”a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§\+\<\>\!]"i
    new_line = "\n"
    ws = " "
"""

# List of the terminal symbols for the summary_page_grammar
# These terminals are the same for CP and MD dockets.
summary_page_terminals = [
    "ws",
    "number",
    "forward_slash",
    "single_content_char",
    "new_line",
    "section_symbol",
    "content_char_no_ws",
]

summary_page_nonterminals = [
    "summary",
    "first_page",
    "following_page",
    "header",
    "court_name",
    "caption",
    "defendant_name",
    "def_dob",
    "def_sex",
    "def_addr",
    "def_eyecolor",
    "def_hair",
    "alias",
    "def_race",
    "summary_info",
    "footer",
]

# It can be useful for debugging to include 'new_line' as
# a terminal so that its included in output xml.
summary_body_terminals = [
    "ws",
    "number",
    "number_w_dec_hyp",
    "forward_slash",
    "single_content_char",
    "content_char_no_ws",
    "section_symbol",
    "migration",
    "ungraded",
]

shared_summary_page_grammar_nonterminals = r"""
    defendant_name = words+
    def_dob = "DOB:" ws* date?
    def_sex = "Sex:" ws* words?
    def_addr = words*
    def_eyecolor = "Eyes:" ws* words?
    def_hair = "Hair:" ws* words?
    def_race = "Race:" ws* words?
    alias = ws? words+
    """


md_summary_page_grammar = Grammar(
    r"""
    # Grammar for parsing CP summary pages, to separate
    # header, body, and footer for each page.
    # the body of each page will be combined and separately parsed.
    summary = first_page following_page*

    first_page = header
                 caption
                 (ws* "Aliases:"  alias* new_line
                    (ws* alias+ new_line)* )?
                 empty_line*
                 summary_info
                 footer

    header = ws* court_name ws* new_line
             ws* "Public Court Summary" ws* new_line+

    court_name = single_content_char+

    caption = ws* defendant_name ws+ def_dob ws* def_sex ws* new_line
              ws* def_addr ws+ def_eyecolor ws* new_line
              ws+ def_hair ws* new_line
              ws+ def_race ws* new_line

    summary_info = ((line / empty_line) !start_of_footer)+ line

    footer = start_of_footer (line / empty_line)+ page_break

    start_of_footer = new_line* ws* "MDJS" line

    following_page = ws* "Public Court Summary" ws* new_line
                     caption
                     empty_line?
                     summary_info
                     footer


    """ + shared_summary_page_grammar_nonterminals + useful_terminals
)


cp_summary_page_grammar = Grammar(
    r"""
    # Grammar for parsing CP summary pages, to separate
    # header, body, and footer for each page.
    # the body of each page will be combined and separately parsed.
    summary = first_page following_page*
    first_page = header caption summary_info footer
    header = ws* court_name ws* new_line ws* "Court Summary" ws* new_line+
    court_name = single_content_char+

    caption = defendant_name ws+ def_dob ws* def_sex ws* new_line ws* def_addr ws+ def_eyecolor ws* new_line "Aliases:" ws+ def_hair ws* new_line alias? ws+ def_race ws* new_line (alias new_line)* empty_line

    summary_info = ((line / empty_line) !start_of_footer)+ line

    following_page = header continuation summary_info footer
    continuation = ~r".* \(Continued\)" new_line

    footer = start_of_footer (line / empty_line)+ page_break
    start_of_footer = new_line* ws* "CPCMS" line

    """
    + shared_summary_page_grammar_nonterminals + useful_terminals
)

cp_summary_body_nonterminals = [
    "summary_body",
    "case_category",
    "case_status",
    "cases_in_county",
    "county",
    "case",
    "case_basics",
    "docket_num",
    "proc_status",
    "dc_num",
    "otn_num",
    "arrest_disp_actions",
    "arrest_disp",
    "arrest_trial",
    "legacy_num_cont",
    "arrest_date",
    "disp_date",
    "prob_psi",
    "disp_judge",
    "def_atty",
    "charges",
    "closed_sequences",
    "closed_sequence",
    "open_sequences",
    "open_sequence",
    "sequence_num",
    "statute",
    "grade",
    "description",
    "closed_sequence_header",
    "seq_no_header",
    "sentence_dt_header",
    "open_sequence_header",
    "sequence_disposition",
    "sequence_disposition",
    "sequence_continued",
    "sentencing_info",
    "sentence_date",
    "sentence_type",
    "program_period",
    "sentence_length",
    "trial_date",
    "legacy_num",
    "action_list",
    "last_actions",
    "last_action",
    "last_action_date",
    "last_action_room",
    "next_actions",
    "next_action",
    "next_action_date",
    "next_action_room",
    "archives",
    "archived_case",
]

md_summary_body_nonterminals = [
    "summary_body",
    "case_category",
    "court_or_county",
    "court",
    "county",
    "county_name_only",
    "cases_with_status",
    "case_status",
    "case",
    "case_basics",
    "arrest_disp_actions",
    "docket_num",
    "proc_status",
    "proc_stat_cont",
    "otn_num",
    "arrest_disp",
    "case_status",
    "legacy_num_cont",
    "arrest_date",
    "disp_date",
    "disp_judge",
    "bail_info",
    "bail_type",
    "bail_amount",
    "bail_status",
    "charges",
    "charge_header",
    "charge",
    "charge_continued",
    "sentence",
    "sentence_type",
    "sentence_date",
    "sentence_length",
    "program_period",
    "statute",
    "grade",
    "description",
    "disposition",
    "counts",
    "last_actions",
    "last_action",
    "last_action_date",
    "next_actions",
    "next_action",
    "next_action_date",
    "archives",
    "archived_case",
]

md_summary_body_grammar = Grammar(
    r"""
    summary_body = case_category+ empty_line*
    case_category = ws* court_or_county new_line
                    (cases_with_status+ / empty_line)

    court_or_county = court / county / statewide
    court = "Court:" ws* words
    county = "County:" ws* words
    statewide = ws* "Statewide"
    county_name_only = ws+ word  # i.e., "Cambria", not "County: Cambria"

    cases_with_status = ws* case_status ws* new_line
                        empty_line? empty_line?
                        (case+ /
                         (empty_line* &(((ws* county) /
                                         (county_name_only))
                                        new_line)))
                        # there may be a county/status line w/ no cases included
    case_status = words
    case = (county_name_only new_line empty_line?)? ws* case_basics new_line arrest_disp_actions charges? (empty_line* / (empty_line* ws* end_of_input))

    case_basics = docket_num ws+ (proc_status ws+)? otn_num

    docket_num = content_char_no_ws+

    proc_status = "Processing Status:" ws* words?
    proc_stat_cont = !disp_date words+

    otn_num = ("OTN:" / "OTN/LOTN:") ws* words?

    arrest_disp_actions = (arrest_disp new_line)?
                          (case_status new_line)?
                          (last_actions new_line)?
                          (case_status new_line)?
                          (next_actions new_line)?
                          (case_status new_line)?
                          (bail_info new_line)?
                          (case_status new_line)?

    arrest_disp = ws* arrest_date (ws+ proc_stat_cont)? ws* disp_date
    arrest_date = "Arrest Date:" (ws* date)?
    disp_date = "Disp. Event Date:" ws* date?

    last_actions = ws* last_action ws+ last_action_date
    last_action = "Last Action:" ws? words?
    last_action_date = "Last Action Date:" ws? date?

    next_actions = ws* next_action ws+ next_action_date
    next_action = "Next Action:" ws? words?
    next_action_date = "Next Action Date:" ws? date?

    bail_info = ws* bail_type ws+ bail_amount ws+ bail_status
    bail_type = "Bail Type:" (ws* !bail_amount words)?
    bail_amount = "Bail Amount:" ws* words?
    bail_status = "Bail Status:" ws* words?

    charges = charge_header new_line
              (charge)*

    charge_header = ws+ "Statute" ws+ "Grade" ws+ "Description" ws+ "Disposition" ws+ "Counts" ws*
    charge = ws+ statute ws* (grade ws+)? (description ws+)?
        (disposition ws+)? counts? new_line
        (charge_continued new_line)* sentences?

    # a charge_continued is the contiuation of a description of an offense.
    # We know its a continuation line, and not a new sequence because it doesn't start
    # with a number. Except sometimes they do start with numbers.
    # If the line does start with a number, require there are more words immediately
    # after, to distinguish a sequence like "  2     " from "    13 years of age".
    charge_continued = (ws+ !(number ws) !date words ws* words?) /
                         (ws+ number ws words ws* words?)

    sentences = empty_line+ sentence_header new_line sentence+
    sentence_header = ws+ "Program Type" ws+ "Sentence Date" ws+ "Sentence Length"
                      ws+ "Program Period"

    # the &word lookahead functions to make sure this line is not
    # simply an empty line w/ a space or two. It must have _some_
    # text content, even if we can't guarantee it'll have any particular
    # details of the sentence filled in.
    sentence = ws+ &word sentence_type? ws* sentence_date? ws*
               sentence_length? ws* program_period? new_line

    sentence_type = words+
    sentence_date = date+
    sentence_length = words+
    program_period = words+

    statute = ((number / word) ws+ section_symbol ws+ word (ws+ section_symbol+ ws word)?) / migration

    migration = "Migration" ws+ section_symbol ws+ "Migration"

    grade = ungraded / (content_char_no_ws content_char_no_ws?)
    ungraded = "NONE"

    description = words+
    disposition = words+
    counts = number+

    archives = ws+ "Archived" ws* new_line (archived_case new_line empty_line*)+
    archived_case = ws+ docket_num ws+ words
    """ + useful_terminals
)

cp_summary_body_grammar = Grammar(
    r"""
    summary_body = case_category+ empty_line*
    case_category = ws* case_status ws* new_line cases_in_county+ archives?
    case_status = words
    cases_in_county = county new_line case+
    county = ws* words ws*
    case = ws* case_basics new_line arrest_disp_actions charges? (empty_line* / (empty_line* ws* end_of_input))

    case_basics = docket_num ws+ proc_status ws+ dc_num ws+ otn_num
    docket_num = content_char_no_ws+
    proc_status = "Proc Status: " words?
    dc_num = "DC No: " content_char_no_ws*
    otn_num = "OTN:" ws* content_char_no_ws*

    # The arrest_disp section can be any combination of a set of lines,
    # possibly interrupted by a repeated case_basics line.
    arrest_disp_actions = (arrest_disp new_line)?
                      (case_basics new_line)?
                      (arrest_trial new_line)?
                      (legacy_num_cont new_line)? # assuming legacy num won't split pages
                      (case_basics new_line)?
                      (def_atty new_line)?
                      (case_basics new_line)?
                      (last_actions new_line)?
                      (case_basics new_line)?
                      (next_actions new_line)?
                      (case_basics new_line)?
                      (disp_date_and_judge new_line)?
                      (case_basics new_line)?
                      (prob_psi new_line)?
                      (case_basics new_line)?


    arrest_disp = ws* arrest_date ws+ disp_date ws+ disp_judge (ws+ is_appeal)?
    arrest_trial = ws* arrest_date ws+ trial_date ws+ legacy_num
    legacy_num_cont = ws+ word
    def_atty = ws* "Def Atty:" ws+ single_content_char+
    last_actions = ws+ last_action ws+ last_action_date ws+ last_action_room
    next_actions = ws+ next_action ws+ next_action_date ws+ next_action_room
    disp_date_and_judge = ws+ disp_date ws+ disp_judge
    prob_psi = ws+ "Prob #:" ws+ word? ws+ "PSI#:" ws*


    arrest_date = "Arrest Dt:" ws? date?
    disp_date = "Disp Date:" ws? date?
    disp_judge = "Disp Judge:" ws? words?
    is_appeal = words+
    trial_date = "Trial Dt:" ws? date?
    legacy_num = "Legacy No:" ws* words?

    last_action = "Last Action:" ws? words?
    last_action_date = "Last Action Date:" ws? date?
    last_action_room = "Last Action Room:" ws? words?
    next_action = "Next Action:" ws? words?
    next_action_date = "Next Action Date:" ws? date?
    next_action_room = "Next Action Room:" ws? words?

    # Closed and Active-ish cases have different formats for the sequence table.
    charges = closed_sequences / open_sequences

    closed_sequences = closed_sequence_header+
                       (closed_sequence* / (line closed_sequence*))?
    closed_sequence_header = (seq_no_header new_line)+
                             (sentence_dt_header new_line)+


    seq_no_header = ws+ "Seq No" ws+ "Statute" ws+ "Grade" ws+ "Description" ws+ "Disposition"
    sentence_dt_header = ws+ "Sentence Dt." ws+ "Sentence Type" ws+ "Program Period" ws+ "Sentence Length"

    closed_sequence = ws* sequence_num ws+ statute ws* (grade ws+)? description? ws* sequence_disposition? ws* new_line
                     (sequence_continued new_line)*
                     closed_sequence_header?
                     (empty_line closed_sequence_header)?
                     (sentencing_info empty_line? closed_sequence_header?)*

    open_sequences = open_sequence_header+ (open_sequence+ / (line open_sequence_header open_sequence*))?
    open_sequence_header = ws+ "Seq No" line
    open_sequence = ws* sequence_num ws+ statute ws* (grade ws+)? description? (ws+ sequence_disposition)? new_line (sequence_continued new_line)* open_sequence_header?

    sequence_num = !date number
    statute = ((number / word) ws+ section_symbol ws+ word (ws+ section_symbol+ ws word)?) / migration
    migration = "Migration" ws+ section_symbol ws+ "Migration"
    grade = content_char_no_ws content_char_no_ws?
    description = words+
        # + is needed only to make the parser not totally conflate this rule
        # with the underlying words rule. W/out +, the description non-terminal
        # disappears in the parser.
    sequence_disposition = words+

    # a sequence_continued is the contiuation of a description of an offense.
    # We know its a continuation line, and not a new sequence because it doesn't start
    # with a number. Except sometimes they do start with numbers.
    # If the line does start with a number, require there are more words immediately
    # after, to distinguish a sequence like "  2     " from "    13 years of age".
    sequence_continued = (ws+ !(number ws) !date words ws* words?) /
                         (ws+ number ws words ws* words?)

    sentencing_info = ws+ sentence_date ws+ sentence_type? (ws+ program_period? ws* sentence_length? ws*)? new_line
    sentence_date = date ws
    sentence_type = words+
    program_period = words+
    sentence_length = words+

    archives = ws+ "Archived" ws* new_line (archived_case new_line empty_line*)+
    archived_case = ws+ docket_num ws+ words
    """
    + useful_terminals
)
