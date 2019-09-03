from typing import Tuple, Union, List
import mysql.connector
import os

def int_or_float(n: float) -> Union[int, float]:
    """
    Return a number an int, if it can be an int, else a float.

    For example, 10.0 is returned as 10, but 10.3 returns as 10.3.
    """
    if int(n) == n: return int(n)
    return n

def percent_to_float(s: str) -> float:
    """
    Return the float representation of a string containing a percent.

    For ex., "10%" returns 10.0
    """
    try:
        return float(s.strip("%"))
    except:
        return 0.0

def guess_grade(ch: "Charge") -> List[Tuple[str, float]]:
    """
    Guess the grade of a charge.

    Args:
        ch (Charge): A criminal Charge.

    Returns:
        List of tuples like (a string indicating the most likely grade of the offense, probability of that grade)
    """
    if ch.get_statute_section() == "" or ch.get_statute_chapter() == "":
        return ("Unknown", 1)
    cnx = mysql.connector.connect(user=os.environ['mysql_user'], password=os.environ['mysql_pw'],
                              host=os.environ['mysql_host'],
                              database='cpcms_aopc_summary')
    cur = cnx.cursor()
    chapter = int_or_float(ch.get_statute_chapter())
    section = int_or_float(ch.get_statute_section())
    if ch.get_statute_subsections() == "":
        # If the statute doesn't have a subsection, then query the table without subsections.
        query = ("SELECT Grade, Percent as P FROM crimes_wo_subsection WHERE title=%s AND section=%s")
        cur.execute(query, (chapter, section))
    else:
        query = ("SELECT Grade, Percent_w_Subsection as P FROM crimes_w_subsection WHERE title=%s AND section=%s AND subsection LIKE %s")
        cur.execute(query, (chapter, section, ch.get_statute_subsections()))
    try:
        percents = [(g,percent_to_float(p)) for g, p in cur]
        return sorted(percents, key=lambda i: i[1])
    except IndexError:
        return [("", 0)]
