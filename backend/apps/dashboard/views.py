from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_dashboard


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_date = request.query_params.get("date", "")
        selected_date = parse_date(raw_date) if raw_date else timezone.localdate()
        if raw_date and selected_date is None:
            raise ValidationError({"date": "Use YYYY-MM-DD format."})
        return Response(get_dashboard(request.user, selected_date))
