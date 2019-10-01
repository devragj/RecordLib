import click
from RecordLib.docket import Docket
from RecordLib.serializers import to_serializable
import json

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
        d, errs = Docket.from_pdf(path, tempdir)
        print("---Errors---")
        print(errs)
        print("---Person---")
        print(json.dumps(d._defendant, default=to_serializable))
        print("---Case---")
        print(json.dumps(d._case, default=to_serializable))
    print("Done.") 