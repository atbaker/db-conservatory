from django.contrib import admin
from .models import Database, Container

class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'ports',)
    prepopulated_fields = {'slug': ('name',),}
admin.site.register(Database, DatabaseAdmin)

class ContainerAdmin(admin.ModelAdmin):
    list_display = ('container_id', 'name', 'database', 'created')
admin.site.register(Container, ContainerAdmin)
