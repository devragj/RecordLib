from rest_framework.response import Response 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
import logging
from RecordLib.crecord import CRecord
from RecordLib.docket import Docket
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
    CRecordSerializer, DocumentRenderSerializer, FileUploadSerializer, 
    UserProfileSerializer, UserSerializer, IntegrateSourcesSerializer, SourceRecordSerializer
)
from cleanslate.compressor import Compressor
from ujs.models import SourceRecord
import json
import os
import os.path
from datetime import *
import zipfile
import tempfile 
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class FileUploadView(APIView):
    
    parser_classes = [MultiPartParser, FormParser]
    
    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        """Accept dockets and summaries locally uploaded by a user, save them to the server, and return pointers with information about them.


        This POST needs to be a FORM post, not a json post. 

        
        """        
        file_serializer = FileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            files = [f for f in file_serializer.validated_data.get("files")]
            results = []
            try:
                for f in files:
                    source_record = SourceRecord.from_unknown_file(f, owner=request.user)
                    source_record.save()
                    if source_record is not None: 
                        results.append(source_record)
                        # TODO FileUploadView should also report errors in turning uploaded pdfs into SourceRecords.
                return Response({"source_records": SourceRecordSerializer(results, many=True).data}, status=status.HTTP_200_OK)
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
            serializer = CRecordSerializer(data=request.data)
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
            logger.error(e)
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


class RenderDocumentsView(APIView):
    """ Create pettions and an Overview document from an Analysis. 
    
    POST should be a json-encoded object with an 'petitions' property that is a list of petitions to generate
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = DocumentRenderSerializer(data=request.data)
            if serializer.is_valid():
                petitions = []
                for petition_data in serializer.validated_data["petitions"]:
                    if petition_data["petition_type"] == "Sealing":
                        new_petition = Sealing.from_dict(petition_data)
                        # this could be done earlier, if needed, to avoid querying db over and over.
                        # but we'd need to test what types of templates are actually needed.
                        try:
                            new_petition.set_template(
                                request.user.userprofile.sealing_petition_template.file
                            )
                            petitions.append(new_petition)
                        except Exception as e:
                            print(e)
                            logging.error("User has not set a sealing petition template, or ")
                            logging.error(str(e))
                            continue
                    else:
                        new_petition = Expungement.from_dict(petition_data)
                        try: 
                            new_petition.set_template(
                                request.user.userprofile.expungement_petition_template.file
                            )
                            petitions.append(new_petition)
                        except Exception as e:
                            print(e)
                            logging.error("User has not set an expungement petition template, or ")
                            logging.error(str(e))
                            continue
                client_last = petitions[0].client.last_name
                petitions = [(p.file_name(), p.render()) for p in petitions]
                package = Compressor(f"ExpungementsFor{client_last}.zip", petitions)

                logger.info("Returning x-accel-redirect to zip file.")

                resp = HttpResponse()
                resp["Content-Type"] = "application/zip"
                resp["Content-Disposition"] = f"attachment; filename={package.name}"
                resp["X-Accel-Redirect"] = f"/protected/{package.name}"
                return resp
            else:
                raise ValueError
        except Exception as e:
            print(e)
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user).data,
            "profile": UserProfileSerializer(request.user).data
        })

class IntegrateCRecordWithSources(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):    
        """
        Accept a CRecord and a set of SourceRecords. Incorporate the information that the SourceRecords contain into the CRecord.

        TODO this should replace FileUpload view. 
        """
        try:
            serializer = IntegrateSourcesSerializer(data=request.data)
            if serializer.is_valid():
                crecord = CRecord.from_dict(serializer.validated_data["crecord"])
                for source_record_data in serializer.validated_data["source_records"]:
                    source_record = SourceRecord.objects.get(id=source_record_data["id"])
                    if source_record.record_type == SourceRecord.RecTypes.SUMMARY_PDF:
                        summary = parse_pdf(source_record.file.path)
                        crecord.add_summary(summary, case_merge_strategy="overwrite_old", override_person=True)
                    elif source_record.record_type == SourceRecord.RecTypes.DOCKET_PDF:
                        docket, errs = Docket.from_pdf(source_record.file.path)
                        crecord.add_docket(docket)
                    else:
                        logger.error(f"Cannot parse a source record with type {source_record.record_type}")
                return Response({'crecord': CRecordSerializer(crecord).data}, status=status.HTTP_200_OK) 
            else:
                return Response({
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err: 
            return Response({
                "errors": [str(err)]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)