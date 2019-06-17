from parsimonious.grammar import Grammar

useful_terminals = r"""
    # nonterminals

    line = single_content_char+ new_line
    empty_line = ws* new_line
    word = content_char_no_ws+
    words = word (ws words)*

    # quiet terminals with content that should just disappear
    page_break = "\f"
    end_of_input = !~"."

    # Loud Terminals (include in list of terminals, so content of the
    # node ends up in the output)
    ws = " "
    number = ~r"[0-9]"+
    forward_slash = "/"
    single_content_char =  ~r"[\“\”a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
    content_char_no_ws =  ~r"[\“\”a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
    new_line = "\n"
    ws = " "
"""

# List of the terminal symbols for the summary_page_grammar
summary_page_terminals = ["ws", "number", "forward_slash", "single_content_char", "new_line"]

summary_page_nonterminals = ["summary", "first_page", "following_page", "header", "court_name", "caption", "summary_info", "footer"]

summary_page_grammar = Grammar(
    r"""
    # Grammar for parsing summary pages, to separate
    # header, body, and footer for each page.
    # the body of each page will be combined and separately parsed.
    summary = first_page following_page*
    first_page = header caption summary_info footer
    header = ws* court_name ws* new_line ws* "Court Summary" ws* new_line+
    court_name = single_content_char+

    caption = line+ empty_line

    summary_info = ((line / empty_line) !start_of_footer)+ line

    following_page = header continuation summary_info footer
    continuation = ~r".* \(Continued\)" new_line

    footer = start_of_footer (line / empty_line)+ page_break
    start_of_footer = new_line* ws* "CPCMS" line

    """ + useful_terminals
)

summary_body_nonterminals = [
    "summary_body",
    "case_category",
    "case_status",
    "cases_in_county",
    "county",
    "case",
    "case_basics"
]

summary_body_terminals = [
    "ws", "number", "forward_slash", "single_content_char", "new_line",
    "content_char_no_ws"
]

summary_body_grammar = Grammar(
    r"""
    summary_body = case_category+
    case_category = ws* case_status ws* new_line cases_in_county
    case_status = words
    cases_in_county = county new_line case+
    county = ws* words ws*
    case = ws* case_basics new_line arrest_and_disp new_line def_atty new_line line+ (empty_line+ / (empty_line* ws* end_of_input))
    #case = case_basics new_line arrest_and_disp new_line def_atty new_line charges empty_line
    #
    case_basics = docket_num ws+ proc_status ws+ dc_num ws+ otn_num
    docket_num = content_char_no_ws+
    proc_status = "Proc Status: " words
    dc_num = "DC No: " content_char_no_ws*
    otn_num = "OTN:" ws* content_char_no_ws+

    arrest_and_disp = ws* arrest_date ws+ disp_date ws+ disp_judge
    arrest_date = "Arrest Dt:" ws? content_char_no_ws*
    disp_date = "Disp Date:" ws? content_char_no_ws+
    disp_judge = "Disp Judge: " words

    def_atty = ws* "Def Atty:" ws+ single_content_char+
    #
    # charges = sequence_header sequence+
    # sequence_header = line line
    # sequence = sequence_num ws+ statute ws+ (grade ws+)? description ws+ disposition ws* new_line (sentence_desc_continued new_line)? sentence_date ws+ sentence_type ws+ program_period ws+ sentence_length ws* new_line
    #
    # sequence_num = number
    # statute = number ws+ "§" ws+ number
    # grade = ~"[MF][0-9]*"
    # desciption =

    """ + useful_terminals
)
