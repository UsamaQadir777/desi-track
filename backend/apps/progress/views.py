from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_progress


class ProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_start = request.query_params.get("start", "")
        raw_end = request.query_params.get("end", "")
        start = parse_date(raw_start) if raw_start else None
        end = parse_date(raw_end) if raw_end else None
        errors = {}
        if raw_start and start is None:
            errors["start"] = "Use YYYY-MM-DD format."
        if raw_end and end is None:
            errors["end"] = "Use YYYY-MM-DD format."
        if start and end and start > end:
            errors["date_range"] = "Start date must be before or equal to end date."
        if errors:
            raise ValidationError(errors)
        return Response(get_progress(request.user, start, end))
