from django.contrib import admin
from django.utils.html import format_html
from .models import Publication, Comment, Likes


class LikesInline(admin.TabularInline):
    model = Likes
    extra = 1


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'preview_img', 'video', 'audio')
    fields = ('title', 'description', 'author', 'date', 'img', 'preview_img', 'video', 'audio')
    readonly_fields = ('preview_img',)
    search_fields = ('title', 'author__username')
    inlines = [LikesInline]

    def preview_img(self, obj):
        if obj.img:
            return format_html(
                '<img src="{}" width="100" height="100" css="object-fit: cover;"/>',
                obj.img.url
            )
        return "Немає зображення"
    preview_img.short_description = "попередній перегляд"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at')
    search_fields = ('name', 'post__title')
    list_filter = ('created_at',)


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('ip', 'post', 'created_at')
    search_fields = ('ip', 'post__title')
    list_filter = ('created_at',)
