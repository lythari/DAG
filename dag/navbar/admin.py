from django.contrib import admin
from django.db.models import Count

import navbar.models as navbar_models


class LinksInline(admin.TabularInline):
    model = navbar_models.Link
    extra = 10


@admin.register(navbar_models.Navbar)
class NavbarAdmin(admin.ModelAdmin):
    list_filter = ('state',)
    list_display = ('state', 'position')
    inlines = [LinksInline]