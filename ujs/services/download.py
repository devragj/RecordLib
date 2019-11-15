from datetime import datetime
from ujs.models import SourceRecord
from typing import List
import requests
from django.core.files.base import ContentFile

import urllib3
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'




def source_records(records: List[SourceRecord]) -> None:
    """ Download the source records in a list of source records, if they're not already present. """
    for rec in records:
        if rec.file._file is None:
            resp = requests.get(rec.url, headers={"User-Agent": "ExpungmentGeneratorTesting"})
            if resp.status_code == 200:
                rec.file.save(f"{rec.id}.pdf", ContentFile(resp.content))
            else:
                rec.fetch_status = SourceRecord.Statuses.FETCH_FAILED