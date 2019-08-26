import click
from RecordLib.docket import Docket


@click.command()
@click.option("--doctype", required=True, type=click.Choice(["summary","docket"]))
@click.option("--tempdir", "-td", type=click.Path(), default="tests/data/tmp")
@click.argument("path")
def parse(path, doctype, tempdir):
    """
    Parse a pdf file. Probably only useful for testing.
    """
    if doctype == "summary":
        print("Not implemented yet")
    elif doctype == "docket":
        d = Docket.from_pdf(path, tempdir)
        print(d._defendant)
        print(d._case)
    print("Done.") 