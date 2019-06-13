from parsimonious.grammar import Grammar


summary_grammar = Grammar(
    r"""
    summary = line+
    line = ~r".+\n"i
    """
)
