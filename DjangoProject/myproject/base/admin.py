from django.contrib import admin
from .models import Room, User, Availability, Message, Tcourt

class TcourtAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
# Register your models here.
admin.site.register(Room)
admin.site.register(User)
admin.site.register(Availability)
admin.site.register(Message)
admin.site.register(Tcourt, TcourtAdmin)
