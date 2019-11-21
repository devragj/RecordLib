from typing import Union, BinaryIO
import os
import tempfile

def get_text_from_pdf(pdf: Union[BinaryIO, str], tempdir = None) -> str:
    """
    Function which extracts the text from a pdf document.
    Args:
        pdf:  Either a file object or the location of a pdf document.
        tempdir:  Place to store intermediate files.

    TODO: remove tempdir arg.

    Returns:
        The extracted text of the pdf.
    """
    with tempfile.TemporaryDirectory() as out_dir:
        if hasattr(pdf, "read"):
            # the pdf attribute is a file object,
            # and we need to write it out, for pdftotext to use it.
            pdf_path = os.path.join(out_dir, "tmp.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf.read())
        else:
            pdf_path = pdf
        # TODO - remove the option of making tempdir anything other than a tempfile. 
        #        Only doing it this way to avoid breaking old tests that send tempdir.
        #out_path = os.path.join(tempdir, "tmp.txt")
        out_path = os.path.join(out_dir, "tmp.txt")
        os.system(f'pdftotext -layout -enc "UTF-8" { pdf_path } { out_path }')
        try:
            with open(os.path.join(out_dir, "tmp.txt"), "r", encoding="utf8") as f:
                text = f.read()
                return text
        except IOError as e:
            raise ValueError("Cannot extract pdf text..")
