import django_filters
from accounts.models import *
from django_filters import DateFilter, CharFilter

class commentsFilters(django_filters.FilterSet):
	class Meta:
		model = Sentiment_Records
		fields = ['sentiment_result']

	Upper_Date = DateFilter(field_name='date_created', label='Upper Than ', lookup_expr='gte')
	Lower_Date = DateFilter(field_name='date_created', label='Lower Than ', lookup_expr='lte')
	sentiment_result = CharFilter(field_name='sentiment_result', label='Sentiment Result', lookup_expr='icontains')
	song_comments = CharFilter(field_name='song_comments', label='Comments', lookup_expr='icontains')