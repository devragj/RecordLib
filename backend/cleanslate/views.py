from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from RecordLib.crecord import CRecord
from RecordLib.summary.pdf import parse_pdf
from RecordLib.summary import Summary
from RecordLib.analysis import Analysis
from RecordLib.ruledefs import (
    expunge_summary_convictions,
    expunge_nonconvictions,
    expunge_deceased,
    expunge_over_70,
)

import json
import os
import os.path
from datetime import *


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, timedelta):
        serial = str(obj)
        return serial

    return obj.__dict__


class FileUploadView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        try:
            pdf_file = request.data["file"]
            rec = CRecord()
            base = os.path.dirname(os.path.abspath(__file__))
            tempdir = os.path.join(base, "tmp")
            summary = parse_pdf(
                pdf=pdf_file,
                tempdir=tempdir)
            rec.add_summary(summary)

            json_to_send = json.dumps({"defendant": rec.person, "cases": rec.cases}, default=serialize)
            # json_to_send = json.dumps({"defendant": rec.person, "cases": rec.cases}, indent=4, default=serialize)
            return Response(json_to_send, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)

