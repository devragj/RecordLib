import click
import logging
import requests
import os
from RecordLib.number_generator import create_docket_numbers
import pytest
import csv


@click.group()
def cli():
    return

def download(url, dest_path, name, doc_type):
    """ Download something from a url """
    resp = requests.get(url, headers={"User-Agent": "DocketAnalyzerTesting"})
    if resp.status_code == 200:
        logging.info(f"Downloaded {doc_type}")
        with open(f"{dest_path}/{name}_{doc_type}.pdf", "wb") as downloaded:
            downloaded.write(resp.content)
    return

def download_docket(scraper_url: str, court: str, docket_number: str, doc_type: str):
    """ Download a single docket using the DocketScraperAPI.

    Args:
        scraper_url: the first part of the url to the DocketScraperAPI app.
        court: the initials of the court this docket is from. CP or MDJ.
        docket_number: the docket number.
        doc_type: summary or docket.

    Returns:
        If successful, a tuple with the url of the downloaded file
        as well as the downloaded file. Otherwise, a tuple (None, None)
    """
    resp = requests.post(
        f"{scraper_url}/lookupDocket/{court}", json={"docket_number": docket_number})
    if "Error" in resp.json().get("status"):
        logging.error("Error from ScraperAPI:" + resp.json().get("status"))
        return None, None
    if resp.status_code == 200 and resp.json().get("docket") is not None:
        logging.info("... URL found. Downloading file.")
        if doc_type.lower() in ["s", "summary", "summaries"]:
            # download the summary
            url = resp.json()["docket"]["summary_url"]
        else:
            url = resp.json()["docket"]["docket_sheet_url"]

        resp = requests.get(url, headers={"User-Agent": "DocketAnalyzerTesting"})
        if resp.status_code == 200:
            return url, resp.content
        else:
            logging.error(
                f"...request for url failed. Status code: { resp.status_code }"
            )
            logging.error(
                f"   URL was { url }"
            )
        logging.info("... Downloading complete. Moving on.")
    else:
        logging.info("Request failed. Moving on.")
    return None, None


@cli.command()
@click.option("-p", "--dest-path", default="tests/data", show_default=True)
@click.option("-u", "--scraper-url", default="http://localhost:5000", show_default=True)
@click.option("-dt", "--doc-type", default="summary", show_default=True, type=click.Choice(["summary", "docket", "both"]))
@click.option("-i", "--input-csv", required=True)
@click.option("-o", "--output-csv", default=None)
@click.option("-c", "--court", default="CP", show_default=True, type=click.Choice(["CP","MDJ", "both"]))
def names(dest_path: str, scraper_url: str, doc_type: str, input_csv: str, output_csv: str, court: str) -> None:
    """Download dockets from a list of names.

    TODO need to be able to search both CP and MDJ dockets in one call of this cli.
    """
    logging.basicConfig(level=logging.INFO)

    if court == "CP":
        courts = ["CP"]
    elif court == "MDJ":
        courts = ["MDJ"]
    else:
        courts = ["MDJ", "CP"]

    if not os.path.exists(dest_path):
        logging.warning(f"{dest_path} does not already exist. Creating it")
        os.mkdir(dest_path)

    with open(input_csv, 'r') as input_file:
        reader = csv.DictReader(input_file)
        if output_csv:
            output_file = open(output_csv, "a+")
            writer = csv.DictWriter(output_file, reader.fieldnames + ["Name", "DOB", "url", "doctype"])
        if "Name" not in reader.fieldnames or "DOB" not in reader.fieldnames:
            logging.error("Input-file must have the columns 'Name' and 'DOB'")
            return

        for row in reader:
            name = row["Name"].split(" ")
            first_name = name[0]
            last_name = name[-1]
<<<<<<< HEAD
            resp = requests.post(f"{scraper_url}/searchName/{court}",
                json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "dob": row["DOB"]
                })
            if resp.status_code == 200:
                logging.info(f"Successful search for {row['Name']}")
                if doc_type.lower() in ["s", "summary", "summaries", "both"]:
                    # download the summary
                    try:
                        logging.info("... Downloading summary")
                        row["url"] = resp.json()["dockets"][0]["summary_url"]
                        row["doctype"] = "summary"
                        download(row["url"], dest_path, row["Name"], doc_type)
                    except:
                        logging.error(f"... No summary found for {row['Name']}.")
                        row["url"] = ""
                        row["doctype"] = ""
                    if output_csv: writer.writerow(row)
                if doc_type.lower() in ["d", "docket", "both"]:
                    logging.info("... Downloading dockets")
                    try:
                        for i, docket in enumerate(resp.json()["dockets"]):
                            logging.info(f"... ({ str(i) })")
                            row["url"] = docket["docket_sheet_url"]
                            row["doctype"] = "docket"
=======
            for court_to_search in courts:
                resp = requests.post(f"{scraper_url}/searchName/{court_to_search}",
                    json={
                        "first_name": first_name,
                        "last_name": last_name,
                        "dob": row["DOB"]
                    })
                if resp.status_code == 200:
                    logging.info(f"Successful search for {row['Name']}")
                    if doc_type.lower() in ["s", "summary", "summaries", "both"]:
                        # download the summary
                        try:
                            logging.info("... Downloading summary")
                            row["url"] = resp.json()["dockets"][0]["summary_url"]
                            row["doctype"] = "summary"
>>>>>>> origin/master
                            if output_csv: writer.writerow(row)
                            download(row["url"], dest_path, row["Name"], doc_type)
                        except:
                            logging.error(f"... No summary found for {row['Name']}.")
                            row["url"] = ""
                            row["doctype"] = "none"
                    if doc_type.lower() in ["d", "docket", "both"]:
                        logging.info("... Downloading dockets")
                        try:
                            for i, docket in enumerate(resp.json()["dockets"]):
                                logging.info(f"... ({ str(i) })")
                                row["url"] = docket["docket_sheet_url"]
                                row["doctype"] = "docket"
                                if output_csv: writer.writerow(row)
                                download(row["url"], dest_path, row["Name"] + "_" + str(i), doc_type)
                        except:
                            logging.error(f" No dockets found for {row['Name']}.")
                            row["url"] = ""
                            row["doctype"] = "none"
                else:
                    logging.warning(f"Did not find any results for {row['Name']}")
                if output_csv: writer.writerow(row)

    if output_csv: output_file.close()
    logging.info("Complete.")
    return


@cli.command()
@click.option("-p", "--dest-path", default="tests/data", show_default=True)
@click.option("-u", "--scraper-url", default="http://localhost:5000", show_default=True)
@click.option("-dt", "--doc-type", default="summary", show_default=True, type=click.Choice(["summary","docket"]))
@click.option("-i", "--input-csv", required=True)
@click.option("-o", "--output-csv", default=None)
def docket_numbers(dest_path: str, scraper_url: str, doc_type: str, input_csv: str, output_csv: str) -> None:
    """
    Download dockets or summary sheets for the docket numbers listed in <input-csv>

    You need to have the DocketScraperAPI running at <scraper-url>
    """
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(dest_path):
        logging.warning(f"{dest_path} does not already exist. Creating it")
        os.mkdir(dest_path)
    with open(input_csv, 'r') as input_file:
        if output_csv:
            output_file = open(output_csv, "a+")
            writer = csv.DictWriter(output_file, ["Docket Number", "url"])
        reader = csv.DictReader(input_file)
        if "Docket Number" not in reader.fieldnames:
            logging.error("Input-file must have the column 'Docket Number'")
            return
        for row in reader:
            docket_number = row["Docket Number"]
            court = "CP" if "CP-" in docket_number else "MDJ"
            url, resp_content = download_docket(scraper_url, court, docket_number, doc_type)
            if resp_content is not None:
                with open(
                    os.path.join(dest_path, f"{ docket_number }_{ doc_type }.pdf"),
                    "wb",
                ) as f:
                    f.write(resp_content)
                    row["url"] = url
                    if output_csv: writer.writerow(row)
            else:
                logging.error(f"Could not find {docket_number}.")
        if output_csv:
            output_file.close()
        logging.info("Complete.")



@cli.command()
@click.argument("DOCUMENT_TYPE")
@click.option("--number", "-n", default=1, show_default=True)
@click.option("--dest-path", default="tests/data", show_default=True)
@click.option("--scraper-url", default="http://localhost:5000", show_default=True)
@click.option("--court", default="CP", type=click.Choice(["CP", "MDJ", "either"]))
def random(
    document_type: str, number: int, dest_path: str, scraper_url: str, court: str
) -> None:
    """
    Download <n> random "summary" documents or "docket" documents to <dest-path>.

    You need to have the DocketScraperAPI running at <scraper-url>
    """
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(dest_path):
        logging.warning(f"{dest_path} does not already exist. Creating it")
        os.mkdir(dest_path)

    for _ in range(number):
        docket_number = next(create_docket_numbers(court))
        logging.info(f"Finding { docket_number } ... ")
        if court == "either":
            court_to_search = "CP" if "CP-" in docket_number else "MDJ"
            logging.info("court is now " + court_to_search)
        else:
            court_to_search = court
        url_to_fetch, resp_content = download_docket(scraper_url, court_to_search, docket_number, document_type)
        if resp_content is not None:
            with open(
                os.path.join(dest_path, f"{ docket_number }_{ document_type }.pdf"),
                "wb",
            ) as f:
                f.write(resp_content)


    logging.info("Complete.")
