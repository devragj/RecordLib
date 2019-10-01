""" Draft expungments from the command line. """


import click
import os
from RecordLib.summary.pdf import parse_pdf
from RecordLib.docket.docket import Docket
from RecordLib.crecord import CRecord
from RecordLib.analysis import Analysis
from RecordLib.ruledefs import * 
from RecordLib.compressor import Compressor
from RecordLib.attorney import Attorney

@click.group()
def cli():
    return



@cli.command()
@click.option("--directory", "-d", type=click.Path(), required=True)
@click.option("--archive", "-a", type=click.Path(), required=True)
@click.option("--expungement-template", "-et", type=click.Path(), required=True)
@click.option("--sealing-template", "-st", type=click.Path(), required=True)
@click.option("--atty-name", default="")
@click.option("--atty-org", default="")
@click.option("--atty-org-addr", default="")
@click.option("--atty-org-phone", default="")
@click.option("--atty-bar-id", default="")
@click.option("--tempdir", "-td", type=click.Path(), default="tests/data/tmp")
def dir(directory, archive, expungement_template, sealing_template, atty_name, atty_org, atty_org_addr, atty_org_phone, atty_bar_id, tempdir):
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    summaries = []
    dockets = []
    atty = Attorney(name=atty_name, organization=atty_org, organization_address=atty_org_addr, organization_phone=atty_org_phone, bar_id=atty_bar_id)
    for f in files:
        print(f"  Processing {f}")
        try:
            dk = Docket.from_pdf(f, tempdir=tempdir)
            print(f"    It looks like {f} is a docket.")
            dockets.append(dk)
        except:
            try:
                sm = parse_pdf(f, tempdir=tempdir)
                print(f"    It looks like {f} is a summary.")
                summaries.append(sm)
            except:
                print(f"    It seems {f} is neither a summary nor a docket.")
    
    crec = CRecord()
    [crec.add_summary(summary) for summary in summaries]
    [crec.add_docket(docket) for docket in dockets]

    analysis = (
        Analysis(crec)
        .rule(expunge_deceased)
        .rule(expunge_over_70)
        .rule(expunge_nonconvictions)
        .rule(expunge_summary_convictions)
        .rule(seal_convictions)
    )

    petitions = [petition for decision in analysis.decisions for petition in decision.value] 
    for petition in petitions: petition.attorney = atty
    with open(sealing_template, "rb") as doc:
        for petition in petitions:
            if petition.petition_type == "Sealing":
                petition.set_template(doc)

    with open(expungement_template, "rb") as doc:
        for petition in petitions:
            if petition.petition_type == "Expungement":
                petition.set_template(doc)


    petition_tuples = []
    for pt in petitions:
        petition_tuples.append((pt.file_name(), pt.render()))
    pkg = Compressor(archive, petition_tuples, tempdir=tempdir)
    pkg.save()
    print ("*********************************")
    print ("****** COMPLETE *****************")
    print ("*********************************")