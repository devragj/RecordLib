from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import Optional
from dataclasses import dataclass, asdict
import re 


@dataclass
class SourceRecordFileInfo:
    caption: str = ""
    docket_num: str= ""
    court: str  = "" 
    url: str = ""
    record_type: str = ""
    fetch_status: str = ""

def source_record_info(filename: str):
    file_info = SourceRecordFileInfo()
    if re.search("pdf$", filename, re.IGNORECASE):
        if re.search("summary", filename, re.IGNORECASE):
            file_info.record_type = SourceRecord.RecTypes.SUMMARY_PDF
        elif re.search("docket", filename, re.IGNORECASE):
            file_info.record_type = SourceRecord.RecTypes.DOCKET_PDF
    
        if re.search("CP", filename):
            file_info.court = SourceRecord.Courts.CP
        elif re.search("MD", filename):
            file_info.court = SourceRecord.Courts.MDJ

        file_info.fetch_status = SourceRecord.Statuses.FETCHED
        return file_info
    else:
        return None


class SourceRecord(models.Model):
    """
    Class to manage documents that provide information about a person's criminal record, such as a 
    summary pdf sheet or a docket pdf sheet.
    
    caption="Comm. v. Smith",
        docket_num="CP-1234", 
        court=SourceRecord.COURTS.CP,
        url="https://ujsportal.gov", 
        record_type=SourceRecord.RecTypes.SUMMARY,
        owner=admin_user
    """

    @classmethod
    def from_unknown_file(cls, a_file: InMemoryUploadedFile, **kwargs) -> Optional[SourceRecord]:
        """ Create a SourceRecord from an uploaded file, or return None if we cannot tell what the file is. """
        try: 
            file_info = source_record_info(a_file.name)
            if file_info:   
                return cls(**asdict(file_info), file=a_file, **kwargs)
            else: 
                return None
        except:
            return None

    class Courts:
        """ Documents may come from one of these courts. """
        CP = "CP"
        MDJ = "MDJ"
        __choices__ = [
            ("CP", "CP"),
            ("MDJ", "MDJ"),
        ]

    class RecTypes:
        """ These types of records may be stored in this class. 
        """
        SUMMARY_PDF = "SUMMARY_PDF"
        DOCKET_PDF = "DOCKET_PDF"
        __choices__ = [
            ("SUMMARY_PDF", "SUMMARY_PDF"),
            ("DOCKET_PDF", "DOCKET_PDF"),
        ]

    class Statuses:
        """
        Documents have to be fetched and saved locally. 
        Has a particular document been fetched?
        """
        NOT_FETCHED = "NOT_FETCHED"
        FETCHING = "FETCHING"
        FETCHED = "FETCHED"
        FETCH_FAILED = "FETCH_FAILED"
        __choices__ = [
            ("NOT_FETCHED","NOT_FETCHED"),
            ("FETCHING", "FETCHING"),
            ("FETCHED", "FETCHED"),
            ("FETCH_FAILED", "FETCH_FAILED"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    caption = models.CharField(blank=True, max_length=300)
    
    docket_num = models.CharField(blank=True, max_length=50)
    
    court = models.CharField(
        max_length=3, 
        choices=Courts.__choices__,
        blank=True)
    
    url = models.URLField(blank=True, default="")
    
    record_type = models.CharField(
        max_length=30, 
        blank=True,
        choices=RecTypes.__choices__)
        
    fetch_status = models.CharField(
        max_length=100,
        choices=Statuses.__choices__,
        default=Statuses.NOT_FETCHED,
    )
    
    file = models.FileField(null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)