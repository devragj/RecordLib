from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from RecordLib.crecord import CRecord
from RecordLib.summary.pdf import parse_pdf
from RecordLib.serializers import to_serializable
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


class FileUploadView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        """Process a Summary PDF file and return JSON to the user.

        This method expects a Summary PDF file to be posted by the frontend.
        Code from RecordLib is used to read the file, parse it,
        and store the extracted information in a CRecord object.
        Information in the CRecord is then serialized as JSON
        and returned to the frontend.
        """
        try:
            pdf_file = request.data["file"]
            rec = CRecord()
            base = os.path.dirname(os.path.abspath(__file__))
            tempdir = os.path.join(base, "tmp")
            summary = parse_pdf(
                pdf=pdf_file,
                tempdir=tempdir)
            rec.add_summary(summary)

            json_to_send = json.dumps({"defendant": rec.person, "cases": rec.cases}, default=to_serializable)
            # Uncomment for human-readable JSON.  Also comment out the above line.
            # json_to_send = json.dumps({"defendant": rec.person, "cases": rec.cases}, indent=4, default=to_serializable)
            return Response(json_to_send, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
