import django_filters
from haversine import haversine, Unit

from .models import CustomUser


class CustomUserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")
    gender = django_filters.ChoiceFilter(choices=CustomUser.GENDER_CHOICES)
    distance = django_filters.NumberFilter(method="filter_distance")

    def filter_distance(self, queryset, name, value):
        requesting_user = self.request.user
        requesting_user_location = (
            requesting_user.latitude,
            requesting_user.longitude,
        )

        filtered_queryset = queryset.exclude(pk=requesting_user.pk).filter(
            latitude__isnull=False, longitude__isnull=False
        )

        result_queryset = []
        for user in filtered_queryset:
            user_location = (user.latitude, user.longitude)
            distance = haversine(
                requesting_user_location, user_location, unit=Unit.KILOMETERS
            )
            if distance <= value:
                result_queryset.append(user.pk)

        return queryset.filter(pk__in=result_queryset)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "gender", "distance"]
