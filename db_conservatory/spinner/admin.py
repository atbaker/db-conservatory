from django.contrib import admin
from .models import Database, Container

class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'image', 'ports', 'order')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',),}
admin.site.register(Database, DatabaseAdmin)

class ContainerAdmin(admin.ModelAdmin):
    list_display = ('container_id', 'name', 'database', 'user', 'created')
admin.site.register(Container, ContainerAdmin)
