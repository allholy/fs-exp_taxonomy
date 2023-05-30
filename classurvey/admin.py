from django.contrib import admin

from . import models


class SoundAnswerAdmin(admin.ModelAdmin):
    list_display = ('user_id','chosen_class','confidence','date_created')
    list_filter = ['date_created']

class ExitInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id','date_created')
    search_fields = ['answer']

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_id','ip_address','q1','q2','q3','q4','date_created')
    search_fields = ['answer']

class TestSoundAdmin(admin.ModelAdmin):
    list_display = ('sound_id','sound_class','sound_group','sound_difficulty','sound_name')

class ClassChoiceAdmin(admin.ModelAdmin):
    list_display = ('class_key','class_name','top_level','description','examples')


# given data
admin.site.register(models.ClassChoice, ClassChoiceAdmin)
admin.site.register(models.TestSound, TestSoundAdmin)

# user data
admin.site.register(models.SoundAnswer, SoundAnswerAdmin)
admin.site.register(models.ExitInfoModel, ExitInfoAdmin)
admin.site.register(models.UserDetailsModel, UserDetailsAdmin)