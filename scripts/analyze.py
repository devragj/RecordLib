import click
import logging
from RecordLib.common import to_serializable # DataClassJSONEncoder
from RecordLib.crecord import CRecord
from RecordLib.summary import Summary
from RecordLib.analysis import Analysis
from RecordLib.ruledefs import (
    expunge_summary_convictions,
    expunge_nonconvictions,
    expunge_deceased,
    expunge_over_70,
)
import pytest
import json

@click.command()
@click.option("--pdf-summary", "-ps", type=click.Path(), required=True, default=None)
@click.option("--tempdir", "-td", type=click.Path(), default="tests/data/tmp")
def analyze(pdf_summary: str, tempdir: str) -> None:
    rec = CRecord()
    if pdf_summary is not None:
        rec.add_summary(Summary(pdf_summary, tempdir = tempdir))

    analysis = (
        Analysis(rec)
        .rule(expunge_deceased)
        .rule(expunge_over_70)
        .rule(expunge_nonconvictions)
        .rule(expunge_summary_convictions)
    )

    print(json.dumps(analysis.analysis, indent=4, default=to_serializable)) #cls=DataClassJSONEncoder))
