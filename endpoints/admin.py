from django.contrib import admin
from .models import RSS_Feed_Keyowrds,RSS_Feed_Database,RSS_Feed_Name_Icon,RSS_Feed_URL, RSS_Feed_Temp
# Register your models here.

admin.site.site_header = "CyberBriefs Admin Panel"


admin.site.register(RSS_Feed_Keyowrds)
admin.site.register(RSS_Feed_Database)
admin.site.register(RSS_Feed_Name_Icon)
admin.site.register(RSS_Feed_URL)
admin.site.register(RSS_Feed_Temp)

# Main@javascript 