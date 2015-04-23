from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

class StatusFilter(SimpleListFilter):
    title = _('status')
    parameter_name = 'sn'

    def lookups(self, request, model_admin):
        statuses = set([p.status for p in model_admin.model.objects.all()])
        return [(s.id, s.lazy_translation_getter('name', str(s.id))) for s in statuses]
        # You can also use hardcoded model name like "Country" instead of
        # "model_admin.model" if this is not direct foreign key filter

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value())
        else:
            return queryset
