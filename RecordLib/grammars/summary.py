from parsimonious.grammar import Grammar

useful_terminals = r"""
    # nonterminals

    line = single_content_char+ new_line
    empty_line = ws* new_line

    # quiet terminals with content that should just disappear
    page_break = "\f"

    # Loud Terminals (include in list of terminals, so content of the
    # node ends up in the output)
    ws = " "
    number = ~r"[0-9]"+
    forward_slash = "/"
    single_content_char =  ~r"[\“\”a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
    new_line = "\n"
    ws = " "
"""

summary_page_grammar = Grammar(
    r"""
    # Grammar for parsing summary pages, to separate
    # header, body, and footer for each page.
    # the body of each page will be combined and separately parsed.
    summary_page = first_page following_page*
    first_page = header caption summary_info footer !header
    header = ws* court_name ws* new_line ws* "Court Summary" ws* new_line+
    court_name = single_content_char+

    caption = line+ empty_line

    summary_info = (line !start_of_footer)+ line

    following_page = header continuation summary_info footer
    continuation = ~r"Curry, Randall Keith (Continued)" new_line

    footer = start_of_footer (line / empty_line)+ page_break
    start_of_footer = new_line* ws* "CPCMS" line

    """ + useful_terminals
)

summary_body_grammar = None
