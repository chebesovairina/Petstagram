from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PetUser, Post, Comment, Like, Subscription


class PetUserAdmin(UserAdmin):
    list_display = ('username', 'pet_name', 'pet_type', 'email', 'is_staff')
    list_filter = ('pet_type', 'is_staff')
    search_fields = ('username', 'pet_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('pet_name', 'pet_type', 'email', 'avatar', 'bio')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'short_caption', 'created_at', 'like_count')
    list_filter = ('author', 'created_at')
    search_fields = ('caption', 'author__username')
    readonly_fields = ('like_count', 'comment_count')

    def short_caption(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption

    short_caption.short_description = 'Описание'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'short_text', 'post', 'created_at')
    search_fields = ('text', 'author__username', 'post__caption')

    def short_text(self, obj):
        return obj.text[:30] + '...' if len(obj.text) > 30 else obj.text

    short_text.short_description = 'Комментарий'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'target', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('subscriber__username', 'target__username')


admin.site.register(PetUser, PetUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(Subscription, SubscriptionAdmin)