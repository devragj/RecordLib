import click
import logging
import requests
import os
from RecordLib.number_generator import create_docket_numbers
import pytest


@click.command()
@click.argument("DOCUMENT_TYPE")
@click.option("--n", default=1, show_default=True)
@click.option("--dest-path", default="tests/data", show_default=True)
@click.option("--scraper-url", default="http://localhost:5000", show_default=True)
@click.option("--court", default="CP", type=click.Choice(["CP", "MDJ", "either"]))
def cli(
    document_type: str, n: int, dest_path: str, scraper_url: str, court: str
) -> None:
    """
    Download <n> random "summary" documents or "docket" documents to <dest-path>.

    You need to have the DocketScraperAPI running at <scraper-url>
    """
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(dest_path):
        logging.warning(f"{dest_path} does not already exist. Creating it")
        os.mkdir(dest_path)

    for _ in range(n):
        docket_number = next(create_docket_numbers(court))
        logging.info(f"Finding { docket_number } ... ")
        url = f"{ scraper_url }/lookupDocket/{ court }"
        logging.debug(f"... posting to { url }")
        resp = requests.post(url, json={"docket_number": docket_number})
        if resp.status_code == 200 and resp.json().get("docket") is not None:
            logging.info("... URL found. Downloading file.")
            if document_type.lower() in ["s", "summary", "summaries"]:
                # download the summar
                resp = requests.get(resp.json()["docket"]["summary_url"])
            else:
                resp = requests.get(resp.json()["docket"]["docket_sheet_url"])
            if resp.status_code == 200:
                with open(
                    os.path.join(dest_path, f"{ docket_number }_{ document_type }.pdf"),
                    "wb",
                ) as f:
                    f.write(resp.content)
            else:
                logging.error(
                    f"...request for summary url failed. Status code: { resp.status_code }"
                )
            logging.info("... Downloading complete. Moving on.")
        else:
            logging.info("Request failed. Moving on.")

    logging.info("Complete.")
