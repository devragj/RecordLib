import zipfile
import io 
from typing import List, Tuple
import secrets
from RecordLib.petitions import Petition
from docxtpl import DocxTemplate
from contextlib import contextmanager
import os 
import string

def random_temp_directory() -> str:
    """
    return a random name for a temporary directory.
    """
    alphabet = string.ascii_letters
    return ''.join(secrets.choice(alphabet) for i in range(30))


class Compressor:

    def __init__(self, archive_name: str, files: List[Tuple[str, DocxTemplate]] = None, tempdir = None):
        # self.__buffer__ = io.BytesIO()
        if tempdir is None:
            tempdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
        while True:
            # Make sure the new directory we're creating to temporarily 
            # store files does not exist.
            self.__rootdir__ = os.path.join(tempdir, random_temp_directory())
            if not os.path.exists(self.__rootdir__):
                os.makedirs(self.__rootdir__)
                break

        self.archive_name = archive_name
        self.archive_path = os.path.join(self.__rootdir__, self.archive_name)
        self.archive = zipfile.ZipFile(self.archive_path, mode='x')
        if files is not None:
            for fname, f in files:
                self.append(fname, f)
    

    def append(self, filename, file) -> None:
        """
        Add 'file' to this zip archive
        
        TODO this should be done in membory somehow.
        """

        filepath = os.path.join(self.__rootdir__, filename)
        file.save(filepath)
        self.archive.write(filepath, filename)

    def delete_dir(self) -> None:
        """ Delete the directory where all the files were temporarily written
        """
        os.rmtree(self.__rootdir__)

    def save(self) -> str:
        """
        Save the archive to the temporary directory, and
        return the path to it.
        """
        self.archive.close()
