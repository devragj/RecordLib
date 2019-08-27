

"""
The docket parser uses lots of custom NodeVisitor Methods, 

The default NodeVisitor methods just wrap the content of nonterminals in xml tags, and 
return the text of terminals. 

The docket parser needs a function for each section that adds a name attribute containing the 
name of the section. This module creates all those functions, and also provides them to the parser
as a list to tuples of custom functions that gets passed to the CustomNodeVisitor.
"""

__docket_sections__ = [
    "section_case_info",
    "section_related_cases",
    "section_status_info",
    "section_calendar_events",
    "section_confinement_info",
    "section_defendant_info",
    "section_case_participants",
    "section_bail_info",
    "section_charges",
    "section_disposition_sentencing",
    "section_disposition_sentencing_body",
    "section_commonwealth_info",
    "section_entries",
    "section_payment_plan",
    "section_case_financial_info",
]


def __generate_section_visitor_func__(section_name):
    """
    Create a custom node-visitor function that wraps the contents of the node
    (and its kids) in a <section> tag, and also adds an attribute 
    'name' that is the `section_name`

    Args:
        section_name: string thats the name of 
    """
    def custom_visitor(self, node, vc):
        # stringify is a function of the class CustomNodeVisiorFactory creates that turns a list of 
        # nodes that are single characters into a joined string.
        contents = self.stringify(vc)
        contents = f" <section name='{section_name}'> {contents} </section> "
        return contents
    return custom_visitor

def visit_content(self, node, vc):
    """ Custom visitor for visiting a single character that might be an ampersand."""
    if node.text == "&":
        return "&amp;"
    elif node.text == "<":
        return "&lt;"
    elif node.text == ">":
        return "&gt;"
    return node.text

docket_sections_custom_nodevisitors = (
    [(name, __generate_section_visitor_func__(name)) for name in __docket_sections__] + 
    [("single_content_char", visit_content), ("single_content_char_no_ws", visit_content)])