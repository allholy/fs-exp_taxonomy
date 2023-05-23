from django.contrib import admin

from . import models


class SoundAnswerAdmin(admin.ModelAdmin):
    list_display = ('user_id','chosen_class','confidence','date_created')
    list_filter = ['date_created']

class ExitInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id','date_created')
    search_fields = ['answer']

class UserDetailsAdmin(admin.ModelAdmin):
    search_fields = ['answer']


# given data
admin.site.register(models.ClassChoice)
admin.site.register(models.TestSound)

# user data
admin.site.register(models.SoundAnswer, SoundAnswerAdmin)
admin.site.register(models.ExitInfoModel, ExitInfoAdmin)
admin.site.register(models.UserDetailsModel, UserDetailsAdmin)