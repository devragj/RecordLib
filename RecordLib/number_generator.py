import random
import logging
from typing import Generator


def create_docket_numbers(court: str = "either") -> Generator[str, None, None]:
    """
    Generate srandom docket numbers

    Args:
        num: the number of dockets numbers to create
        court: CP or MD dockets? or "both" for both.
    """
    court = random.choice(["CP", "MDJ"]) if court == "either" else court
    county_num = f"0{ random.randrange(1,68) }"[-2:]
    docket_sequence = f"0000000{ random.randrange(1, 2000) }"[-7:]
    year = random.randrange(2007, 2019)
    if court == "CP":
        court_type = random.choice(["CR", "MD"])
        docket_number = f"CP-{ county_num }-{ court_type }-{ docket_sequence}-{ year }"
        yield docket_number
    if court == "MDJ":
        # ct_office doesn't have to end in 101, but the offices that
        # exist are different in each county. Might be up to 2-03 or
        # or something else. But for testing, I think
        # just generating random number from the 101 office will be
        # fine.
        ct_office = f"{ county_num }101"
        docket_number = f"MJ-{ ct_office }-CR-{ docket_sequence }-{ year }"
        yield docket_number

    logging.warning(
        "Odd. You didn't create any docket numbers. Did you select CP, MJ or either for the `court` parameter?"
    )
    yield ""
