from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WaterIntake
from .serializers import WaterIntakeSerializer


class WaterIntakeView(APIView):
    permission_classes = [IsAuthenticated]

    def _parse_date(self, value, field):
        parsed = parse_date(value) if value else None
        if value and parsed is None:
            raise ValidationError({field: "Use YYYY-MM-DD format."})
        return parsed

    def get(self, request):
        start = self._parse_date(request.query_params.get("start"), "start")
        end = self._parse_date(request.query_params.get("end"), "end")
        date = self._parse_date(request.query_params.get("date"), "date") or timezone.localdate()

        if start and end:
            if start > end:
                raise ValidationError({"date_range": "Start date must be before or equal to end date."})
            records = WaterIntake.objects.filter(user=request.user, date__range=[start, end])
            return Response(WaterIntakeSerializer(records, many=True).data)

        intake, _ = WaterIntake.objects.get_or_create(user=request.user, date=date)
        return Response(WaterIntakeSerializer(intake).data)

    def post(self, request):
        date = self._parse_date(request.data.get("date"), "date") or timezone.localdate()
        intake, _ = WaterIntake.objects.get_or_create(user=request.user, date=date)
        serializer = WaterIntakeSerializer(intake, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    def patch(self, request):
        return self.post(request)
