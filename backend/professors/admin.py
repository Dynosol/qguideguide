from django.contrib import admin
from .models import Professor, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'empirical_bayes_average', 'empirical_bayes_rank')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'departments',
        'total_ratings',
        'empirical_bayes_average',
        'empirical_bayes_rank',
        'overall_letter_grade',
        'intra_department_metrics',
    )
    list_filter = ('overall_letter_grade',)
    search_fields = ('name',)
    filter_horizontal = ()

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'departments')
        }),
        ('Ratings', {
            'fields': (
                'total_ratings',
                'empirical_bayes_average',
                'empirical_bayes_rank',
                'overall_letter_grade'
            )
        }),
    )

    ordering = ('empirical_bayes_rank',)
