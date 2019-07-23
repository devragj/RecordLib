import click
import logging
from RecordLib.common import to_serializable # DataClassJSONEncoder
from RecordLib.crecord import CRecord
from RecordLib.summary import Summary
from RecordLib.analysis import Analysis
from RecordLib.redis_helper import RedisHelper
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
@click.option("--redis-collect", "-rc", default=None, type=str, help="connection to redis, in the form [host]:[port]:[db number]:[environment name]. For example, 'localhost:6379:0:development'")
def analyze(pdf_summary: str, tempdir: str, redis_collect: str) -> None:
    rec = CRecord()
    if pdf_summary is not None:
        rec.add_summary(Summary(pdf_summary, tempdir = tempdir))

    if redis_collect is not None:
        try:
            redis_options = redis_collect.split(":")
            rh = RedisHelper(host=redis_options[0], port=redis_options[1],
                             db=redis_options[2],env=redis_options[3])
            rh.sadd_crecord(rec)
        except Exception as e:
            logging.error("You supplied --redis-collect, but collection failed.")

    analysis = (
        Analysis(rec)
        .rule(expunge_deceased)
        .rule(expunge_over_70)
        .rule(expunge_nonconvictions)
        .rule(expunge_summary_convictions)
    )


    print(json.dumps(analysis.analysis, indent=4, default=to_serializable)) #cls=DataClassJSONEncoder))
