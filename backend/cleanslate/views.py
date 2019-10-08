from rest_framework.response import Response 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
import logging
from RecordLib.crecord import CRecord
from RecordLib.analysis import Analysis
from RecordLib.summary.pdf import parse_pdf
from RecordLib.serializers import to_serializable
from RecordLib.summary import Summary
from RecordLib.analysis import Analysis
from RecordLib.ruledefs import (
    expunge_summary_convictions,
    expunge_nonconvictions,
    expunge_deceased,
    expunge_over_70,
    seal_convictions,
)
from RecordLib.petitions import (
    Expungement, Sealing
)
from .serializers import (
    CRecordSerializer, DocumentRenderSerializer, FileUploadSerializer
)
from RecordLib.compressor import Compressor
import json
import os
import os.path
from datetime import *
import zipfile
import tempfile 


class FileUploadView(APIView):
    
    parser_classes = [MultiPartParser, FormParser]
    
    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        """Process a Summary PDF file and return JSON to the user.

        This method expects a Summary PDF file to be posted by the frontend.

        This POST needs to be a FORM post, not a json post. 

        Code from RecordLib is used to read the file, parse it,
        and store the extracted information in a CRecord object.
        Information in the CRecord is then serialized as JSON
        and returned to the frontend.
        """        
        file_serializer = FileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            pdf_files = [f for f in file_serializer.validated_data.get("files")]
            rec = CRecord()
            tempdir = tempfile.mkdtemp()
            try:
                for summary_file in pdf_files:
                    summary = parse_pdf(
                        pdf=summary_file,
                        tempdir=tempdir)
                    rec.add_summary(summary)
                json_to_send = json.dumps({"defendant": rec.person, "cases": rec.cases}, default=to_serializable)
                # Uncomment for human-readable JSON.  Also comment out the above line.
                # json_to_send = json.dumps({"defendant": rec.person, "cases": rec.cases}, indent=4, default=to_serializable)
                return Response(json_to_send, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error_message": "Parsing failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error_message": "Invalid Data.", "errors": file_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AnalyzeView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        """ Analyze a Criminal Record for expungeable and sealable cases and charges.
        
        POST body should be json-endoded CRecord object. 

        Return, if not an error, will be a json-encoded Decision that explains the expungements
        and sealings that can be generated for this record.

        """
        try: 
            data = JSONParser().parse(request)
            serializer = CRecordSerializer(data=data)
            if serializer.is_valid():
                rec = CRecord.from_dict(serializer.validated_data) 
                analysis = (
                    Analysis(rec)
                    .rule(expunge_deceased)
                    .rule(expunge_over_70)
                    .rule(expunge_nonconvictions)
                    .rule(expunge_summary_convictions)
                    .rule(seal_convictions)
        )
                return Response(to_serializable(analysis))
            else: 
                return Response({"validation_errors": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(e)
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


class RenderDocumentsView(APIView):
    """ Create pettions and an Overview document from an Analysis. 
    
    POST should be a json-encoded object with an 'petitions' property that is a list of petitions to generate
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = DocumentRenderSerializer(data=data)
            if serializer.is_valid():
                petitions = []
                for petition in serializer.validated_data["petitions"]:
                    if petition["petition_type"] == "Sealing":
                        petitions.append(Sealing.from_dict(petition))
                    else:
                        petitions.append(Expungement.from_dict(petition))
                client_last = petitions[0].client.last_name

                with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", "rb") as doc:
                    for petition in petitions:
                        petition.set_template(doc)
                petitions = [(p.file_name(), p.render()) for p in petitions]
                package = Compressor(f"ExpungementsFor{client_last}.zip", petitions)
                package.save()
                return Response({"download":package.archive_path})
            else:
                raise ValueError
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


