from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (Answer, Category, Coupon, Difficulty, Note, Profile,
                     Subscription, WritingContent)


class WritingContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_code', 'category', 'difficulty', 'day', 'sequence')
    search_fields = ['content_code', 'content_text_en']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.model.objects.filter(content_text_en__icontains=search_term)
        return queryset, use_distinct

    def get_list_filter(self, request):
        # 수정: 입력 상자로 필터링할 조건 목록 정의
        list_filter = ['day', 'sequence']

        return list_filter

    # 추가: category와 difficulty 필드를 검색 가능하도록 함
    search_fields = ['content_code', 'content_text_en', 'category__name', 'difficulty__name']
    
admin.site.register(WritingContent, WritingContentAdmin)
admin.site.register(Profile)
admin.site.register(Category)
# admin.site.register(WritingContent)
admin.site.register(Answer)
admin.site.register(Subscription)
admin.site.register(Coupon)
admin.site.register(Note)
