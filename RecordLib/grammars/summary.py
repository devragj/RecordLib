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
    single_content_char =  ~r"[\“\”a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§\+\<\>]"i
    content_char_no_ws =  ~r"[\“\”a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§\+\<\>]"i
    new_line = "\n"
    ws = " "
"""

# List of the terminal symbols for the summary_page_grammar
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

summary_page_grammar = Grammar(
    r"""
    # Grammar for parsing summary pages, to separate
    # header, body, and footer for each page.
    # the body of each page will be combined and separately parsed.
    summary = first_page following_page*
    first_page = header caption summary_info footer
    header = ws* court_name ws* new_line ws* "Court Summary" ws* new_line+
    court_name = single_content_char+

    caption = defendant_name ws+ def_dob ws* def_sex ws* new_line ws* def_addr ws+ def_eyecolor ws* new_line "Aliases:" ws+ def_hair ws* new_line alias? ws+ def_race ws* new_line (alias new_line)* empty_line

    defendant_name = words+
    def_dob = "DOB:" ws* date?
    def_sex = "Sex:" ws* words?
    def_addr = words*
    def_eyecolor = "Eyes:" ws* words?
    def_hair = "Hair:" ws* words?
    def_race = "Race:" ws* words?
    alias = words+

    summary_info = ((line / empty_line) !start_of_footer)+ line

    following_page = header continuation summary_info footer
    continuation = ~r".* \(Continued\)" new_line

    footer = start_of_footer (line / empty_line)+ page_break
    start_of_footer = new_line* ws* "CPCMS" line

    """
    + useful_terminals
)

summary_body_nonterminals = [
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
    "arrest_and_disp",
    "arrest_date",
    "disp_date",
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
]

summary_body_grammar = Grammar(
    r"""
    summary_body = case_category+ empty_line*
    case_category = ws* case_status ws* new_line cases_in_county+ archives?
    case_status = words
    cases_in_county = county new_line case+
    county = ws* words ws*
    case = ws* case_basics new_line arrest_and_disp new_line charges? (empty_line* / (empty_line* ws* end_of_input))

    case_basics = docket_num ws+ proc_status ws+ dc_num ws+ otn_num
    docket_num = content_char_no_ws+
    proc_status = "Proc Status: " words
    dc_num = "DC No: " content_char_no_ws*
    otn_num = "OTN:" ws* content_char_no_ws*

    # There seem to be two different formats for the arrest_and_disp section,
    # closed cases have one format, and active-ish ones have a different.
    arrest_and_disp = closed_arrest_and_disp / active_arrest_and_disp

    closed_arrest_and_disp = ws* arrest_date ws+ disp_date ws+ disp_judge (new_line def_atty)?
    arrest_date = "Arrest Dt:" ws? date?
    disp_date = "Disp Date:" ws? date?
    disp_judge = "Disp Judge:" ws? words?
    def_atty = ws* "Def Atty:" ws+ single_content_char+

    active_arrest_and_disp = ws* arrest_date ws+ trial_date ws+ legacy_num (new_line def_atty)? new_line action_list
    trial_date = "Trial Dt:" ws? date?
    legacy_num = "Legacy No:" ws? words?
    action_list = last_actions new_line next_actions
    last_actions = ws+ last_action ws+ last_action_date ws+ last_action_room
    next_actions = ws+ next_action ws+ next_action_date ws+ next_action_room
    last_action = "Last Action:" ws? words?
    last_action_date = "Last Action Date:" ws? date?
    last_action_room = "Last Action Room:" ws? words?
    next_action = "Next Action:" ws? words?
    next_action_date = "Next Action Date:" ws? date?
    next_action_room = "Next Action Room:" ws? words?

    # Closed and Active-ish cases have different formats for the sequence table.
    charges = closed_sequences / open_sequences

    closed_sequences = closed_sequence_header (closed_sequence* / (line closed_sequence*))?
    closed_sequence_header = ws+ "Seq No" ws+ "Statute" ws+ "Grade" ws+ "Description" ws+ "Disposition" new_line ws+ "Sentence Dt." ws+ "Sentence Type" ws+ "Program Period" ws+ "Sentence Length" new_line # this is just the labels of columns.

    # the closed sequence header is interspersed because on page overflows,
    # it can end up inserted in the middle of a sequence.
    closed_sequence = ws* sequence_num ws+ statute ws+ (grade ws+)? description ws+ sequence_disposition ws* new_line (sequence_continued new_line)? closed_sequence_header? (sentencing_info closed_sequence_header?)*

    open_sequences = open_sequence_header+ (open_sequence+ / (line open_sequence_header open_sequence*))?
    open_sequence_header = ws+ "Seq No" line
    open_sequence = ws* sequence_num ws+ statute ws+ (grade ws+)? description (ws+ sequence_disposition)? new_line (sequence_continued new_line)? open_sequence_header?

    sequence_num = !date number
    statute = (number ws+ section_symbol ws+ number_w_dec_hyp (ws+ section_symbol+ ws word)?) / migration
    migration = "Migration" ws+ section_symbol ws+ "Migration"
    grade = content_char_no_ws content_char_no_ws?
    description = words+
        # + is needed only to make the parser not totally conflate this rule
        # with the underlying words rule. W/out +, the description non-terminal
        # disappears in the parser.
    sequence_disposition = words+

    sequence_continued = ws+ !(number ws) !date words ws* words?

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
