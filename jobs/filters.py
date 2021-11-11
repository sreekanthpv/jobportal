import django_filters
from jobs.models import Application,Jobs

class JobFilter(django_filters.FilterSet):
        post_name=django_filters.CharFilter(lookup_expr="icontains")
        class Meta:
            model=Jobs
            fields=["post_name","company"]