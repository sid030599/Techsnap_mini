from pandas import DataFrame as df
import os
from django.http.response import HttpResponse, JsonResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

# Register your models here.
def export_users(modeladmin, request, queryset):
    users = {}
    users['username'] = []
    users['email'] = []
    for user in queryset:
        users['username'].append(user.username)
        users['email'].append(user.email)
    df(users).to_csv('media/users.csv', index=False)
    with open('media/users.csv', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/force-download')
        response['Content-Disposition']='inline;filename=users.csv'
    os.remove('media/users.csv')
    return response
        
export_users.short_description = 'Select Users to Export'

class MyUserAdmin(UserAdmin, admin.ModelAdmin):
    actions = [export_users]
    ordering = ('date_joined', )
    list_display = ('username', 'email', 'date_joined', 'first_name', 'last_name', 'is_staff')
    
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', ),
        }),
    )

class NotificationsInline(admin.StackedInline):
    model = Notifications
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    inlines = [NotificationsInline]
    search_fields=['user__username']
    list_filter = (('bio', admin.EmptyFieldListFilter), ('profile_pic', admin.EmptyFieldListFilter),
                   ('full_name', admin.EmptyFieldListFilter), ('gender', admin.EmptyFieldListFilter),
                   ('country', admin.EmptyFieldListFilter), ('state', admin.EmptyFieldListFilter),
                   ('city', admin.EmptyFieldListFilter), ('email', admin.EmptyFieldListFilter),
                   ('ph_num', admin.EmptyFieldListFilter), ('skills', admin.EmptyFieldListFilter),
                   ('languages', admin.EmptyFieldListFilter), ('default_coding_lang', admin.EmptyFieldListFilter),
                   ('resume', admin.EmptyFieldListFilter), ('workExp', admin.EmptyFieldListFilter),
                   ('current_CTC', admin.EmptyFieldListFilter), ('notice_period', admin.EmptyFieldListFilter),
                   ('willing_to_relocate', admin.EmptyFieldListFilter), ('expected_CTC', admin.EmptyFieldListFilter),
                   ('current_company', admin.EmptyFieldListFilter), ('dream_company', admin.EmptyFieldListFilter), 
                   ('designation', admin.EmptyFieldListFilter))

class NotificationsAdmin(admin.ModelAdmin):
    list_filter = ('mark_as_read',)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
#admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(TransactionHistory)
admin.site.register(Education)
admin.site.register(Proffesion)
admin.site.register(PaytmHistory)