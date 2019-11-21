from django.conf import settings
import requests
import logging
from datetime import date
from typing import Optional, Dict

logger = logging.getLogger(__name__)

def search_by_name(first_name: str, last_name: str, dob: Optional[date], court="both") -> Dict:
    assert court in ["both", "CP", "MDJ"]
    if court=="both":
        results=search_by_name(first_name,last_name,dob,court="CP")
        results.update(search_by_name(first_name,last_name,dob,court="MDJ"))
        return results
    logger.info(f"Searching {court} for {last_name}, {dob}")
    search_data = {
            "first_name": first_name,
            "last_name": last_name,
        }
    if dob:
        search_data["dob"] = dob.strftime(r"%m/%d/%Y")
    resp = requests.post(
        f"{settings.DOCKET_SCRAPER_URL}/searchName/{court}", 
        json=search_data)
    if resp.status_code != 200:
        logger.error("...search failed.")
        return {court: [], "msg": "search failed"}
    elif "dockets" not in resp.json().keys():
        logger.warning("    Search finished, but no dockets returned.")
        return {
            court: {
                "dockets": [], 
                "msg": resp.json()["status"]
            }
        }
    else:
        dockets = resp.json()["dockets"]
        logger.info(f"    Search succeeded, {len(dockets)} dockets found.")
        return {
            court: {
                "dockets": dockets, 
                "msg": resp.json()["status"]
            }
        }