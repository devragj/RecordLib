from rest_framework.response import Response 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
import logging
from django.conf import settings
from .serializers import NameSearchSerializer, DownloadDocsSerializer
from .services import searchujs, download
from .models import SourceRecord


logger = logging.getLogger(__name__)

class SearchName(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            to_search = NameSearchSerializer(data=request.data)
            if to_search.is_valid():
                # search ujs portal for a name.
                # and return the results.
                results = searchujs.search_by_name(**to_search.validated_data)
                return Response({
                    "searchResults": results
                })
            else:
                return Response({
                    "errors": to_search.errors
                }, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({
                "errors": [str(ex)]
            })

class DownloadDocs(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        API endpoint that takes a list of info about documents with urls, downloads them, 
        and returns the info with ids that correspond to the documents' ids in the database.
        """
        try:
            posted_data = DownloadDocsSerializer(data=request.data)
            if posted_data.is_valid():
                records = posted_data.save(owner=request.user)
                download.source_records(records)
                return Response(
                    DownloadDocsSerializer({"source_records": records}).data,
                )
                
            else:
                breakpoint()
                return Response({
                    "errors": posted_data.errors
                })
        except Exception as e:
            return Response({
                "errors": [str(e)]
            })