from typing import Union, BinaryIO
import os

def get_text_from_pdf(pdf: Union[BinaryIO, str], tempdir: str = "tmp") -> str:
    """
    Function which extracts the text from a pdf document.
    Args:
        pdf:  Either a file object or the location of a pdf document.
        tempdir:  Place to store intermediate files.

    Returns:
        The extracted text of the pdf.
    """
    if hasattr(pdf, "read"):
        # the pdf attribute is a file object,
        # and we need to write it out, for pdftotext to use it.
        pdf_path = os.path.join(tempdir, "tmp.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf.read())
    else:
        pdf_path = pdf
    out_path = os.path.join(tempdir, "tmp.txt")
    os.system(f'pdftotext -layout -enc "UTF-8" { pdf_path } { out_path }')
    try:
        with open(os.path.join(tempdir, "tmp.txt"), "r", encoding="utf8") as f:
            text = f.read()
    except IOError as e:
        raise ValueError("Cannot extract pdf text..")

    os.remove(os.path.join(tempdir, "tmp.txt"))
    return text
