from django.contrib import admin
from .models import *

from django.contrib import messages

admin.site.register(UserProfile)

# Персонализиран филтър за Specialty
class SpecialtyFilter(admin.SimpleListFilter):
    title = 'Специалност'  # Име на филтъра в админ панела
    parameter_name = 'specialty'  # Параметърът, който ще се използва в заявката

    def lookups(self, request, model_admin):
        # Връща списък от специалности за филтриране
        specialties = Specialty.objects.all()
        return [(specialty.id, str(specialty)) for specialty in specialties]

    def queryset(self, request, queryset):
        # Филтрира ThemeItem по специалност
        if self.value():
            return queryset.filter(theme_id__specialty__id=self.value())
        return queryset

admin.site.register(School)
admin.site.register(Specialty)
admin.site.register(Documents)

@admin.register(Log)
class LogV(admin.ModelAdmin):
    list_display = ('user_name', 'action', 'date' )
    list_display_links = ('user_name', 'action', )
    list_filter = ('user_name', 'action', )
    ordering = ('-date', )


