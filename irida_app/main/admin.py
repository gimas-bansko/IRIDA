from django.contrib import admin

from .models import (
    AIPrompt,
    AppAttachment,
    BroadcastMessage,
    BroadcastMessageRead,
    Documents,
    Goal,
    Log,
    School,
    SchoolDayConfig,
    Session,
    SessionAttachment,
    SessionNote,
    SessionPoint,
    SessionTask,
    SessionTopic,
    Specialty,
    Subject,
    Topic,
    Unit,
    UserProfile,
)

admin.site.register(UserProfile)


# Персонализиран филтър за Specialty
# ЗАСЕГА НЕ СЕ ПОЛЗВА и е неработещ: queryset() филтрира по
# theme_id__specialty__id, а поле theme_id няма в нито един модел.
# Трябва да се пренапише, преди да се добави в list_filter на някой ModelAdmin.
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
admin.site.register(SchoolDayConfig)
admin.site.register(Specialty)
admin.site.register(Documents)
admin.site.register(Subject)
admin.site.register(Unit)
admin.site.register(Topic)
admin.site.register(Goal)
admin.site.register(Session)
admin.site.register(SessionTopic)
admin.site.register(SessionPoint)
admin.site.register(SessionNote)
admin.site.register(SessionTask)
@admin.register(SessionAttachment)
class SessionAttachmentAdmin(admin.ModelAdmin):
    list_display = ('num', 'name', 'original_filename', 'attachment_type', 'is_student_visible', 'session', 'point', 'file')
    list_filter = ('attachment_type', 'is_student_visible', 'session')
    search_fields = ('name', 'original_filename', 'description')
    ordering = ('session', 'num', 'id')


@admin.register(AppAttachment)
class AppAttachmentAdmin(admin.ModelAdmin):
    list_display = ('num', 'name', 'original_filename', 'file', 'is_system', 'created_by', 'created_at', 'updated_at')
    list_filter = ('is_system', 'created_by')
    search_fields = ('name', 'original_filename', 'description')
    ordering = ('num', 'id')


@admin.register(AIPrompt)
class AIPromptAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_key', 'is_system', 'order', 'created_by', 'updated_at')
    list_filter = ('page_key', 'is_system', 'created_by')
    search_fields = ('title', 'prompt_text', 'instructions')
    ordering = ('page_key', 'order', 'title')


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_role', 'is_active', 'created_by', 'created_at', 'expires_at', 'reads_count')
    list_filter = ('target_role', 'is_active', 'created_at')
    search_fields = ('title', 'message')
    ordering = ('-created_at', '-id')

    def reads_count(self, obj):
        return obj.reads.count()
    reads_count.short_description = 'Брой прочитания'


@admin.register(BroadcastMessageRead)
class BroadcastMessageReadAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'read_at')
    list_filter = ('read_at', 'message')
    search_fields = ('message__title', 'user__username', 'user__first_name', 'user__last_name')
    ordering = ('-read_at',)


@admin.register(Log)
class LogV(admin.ModelAdmin):
    list_display = ('date', 'user_name', 'action', 'user_id')
    list_display_links = ('date', 'user_name', 'action')
    search_fields = ('user_name', 'action')
    list_filter = ('user_name',)
    ordering = ('-date', '-id')
    readonly_fields = ('date', 'user_name', 'user_id', 'action')
