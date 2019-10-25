import click
import logging
from RecordLib.serializers import to_serializable
from RecordLib.crecord import CRecord
from RecordLib.summary import Summary
from RecordLib.docket import Docket
from RecordLib.analysis import Analysis
from RecordLib.redis_helper import RedisHelper
from RecordLib.ruledefs import (
    expunge_summary_convictions,
    expunge_nonconvictions,
    expunge_deceased,
    expunge_over_70,
    seal_convictions,
)
from RecordLib.ruledefs.seal import (
    no_f1_convictions,
    any_felony_convictions_n_years,
    more_than_x_convictions_y_grade_z_years,
)
from RecordLib.summary.pdf import parse_pdf as parse_pdf_summary
import pytest
import json
import glob
import os
import csv


@click.group()
def cli():
    return

@cli.command()
@click.option("--directory", "-d", type=click.Path(), required=True)
@click.option("--tempdir", "-td", type=click.Path(), default="tests/data/tmp")
@click.option("--output", "-o", type=click.Path(), required=True)
def triage(directory, tempdir, output):
    """
    Read through a set of directories each containing records for a single person. Screen each person for obviously disqualifying elements in their record.
    """
    logging.basicConfig(level=logging.ERROR)
    if not os.path.exists(directory):
        logging.info(f"{directory} does not exist.")
        return
    subdirs = os.listdir(directory)
    recs = []
    logging.info(f"Constructing {len(subdirs)} records.")
    for sd in subdirs:
        rec = CRecord()
        pdfs = glob.glob(os.path.join(directory, sd, "*_Summary.pdf"))
        try:
            for pdf in pdfs: 
                try:
                    rec.add_summary(parse_pdf_summary(pdf, tempdir=tempdir))
                except:
                    try:
                        d, _ = Docket.from_pdf(pdf, tempdir=tempdir)
                        rec.add_docket(d)
                    except Exception as e:
                        raise e
            logging.info(f"Constructed a record for {rec.person.full_name()}, with {len(rec.cases)} cases.")
            recs.append((sd, rec))
        except Exception as e:
            logging.error(f"Error for {sd}: {str(e)}")
    logging.info(f"Now analyzing {len(recs)} records.")
    results = []
    for sd, rec in recs:
        
        res = {
                "dir": sd,
                "name": rec.person.full_name(),
                "cases": len(rec.cases),
                "felony_5_yrs": bool(any_felony_convictions_n_years(rec, 5)),
                "2plus_m1s_15yrs": bool(more_than_x_convictions_y_grade_z_years(rec, 2, "M1", 15)),
                "4plus_m2s_20yrs": bool(more_than_x_convictions_y_grade_z_years(rec, 4, "M2", 20)),
                "any_f1_convictions": not no_f1_convictions(rec),
        }
        res["any_disqualifiers"] = any([
            res["felony_5_yrs"],
            res["2plus_m1s_15yrs"],
            res["4plus_m2s_20yrs"],
            res["any_f1_convictions"],
        ])
        results.append(res)
    with open(output, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "dir", "name", "cases", "felony_5_yrs", "2plus_m1s_15yrs", 
            "4plus_m2s_20yrs", "any_f1_convictions", "any_disqualifiers"])
        writer.writeheader()
        for res in results:
            writer.writerow(res)
    
    logging.info("Complete.")

@cli.command()
@click.option("--pdf-summary", "-ps", type=click.Path(), required=True, default=None)
@click.option("--tempdir", "-td", type=click.Path(), default="tests/data/tmp")
@click.option("--redis-collect", "-rc", default=None, type=str, help="connection to redis, in the form [host]:[port]:[db number]:[environment name]. For example, 'localhost:6379:0:development'")
def summary(pdf_summary: str, tempdir: str, redis_collect: str) -> None:
    """
    Analyze a single summary sheet for all sealings and expungements.
    """

    rec = CRecord()
    if pdf_summary is not None:
        rec.add_summary(parse_pdf_summary(pdf_summary, tempdir = tempdir))

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
        .rule(seal_convictions)
    )

    print(json.dumps(analysis, indent=4, default=to_serializable)) #cls=DataClassJSONEncoder))
