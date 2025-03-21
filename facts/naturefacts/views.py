from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from .form import CommentsForm
from .models import Publication, Likes, Comment


class PublicationView(View):
    def get(self, request):
        publication = Publication.objects.all()
        return render(request, 'facts/home_screen.html', {'publication_list': publication})


class SingleEntryView(View):
    def get(self, request, pk):
        single = Publication.objects.get(id=pk)
        liked_ips = Likes.objects.filter(post=single).values_list('ip', flat=True)  # Отримуємо список IP
        return render(request, 'facts/single_entry.html', {'single': single, 'liked_ips': list(liked_ips)})


class AddCommentView(View):
    def post(self, request, pk):
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Правильное сохранение формы
            comment.post_id = pk  # Привязываем комментарий к публикации
            comment.save()
        return redirect(f'/{pk}')


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AddLikeView(View):
    def get(self, request, pk):
        ip_user = get_user_ip(request)
        Likes.objects.get_or_create(ip=ip_user, post_id=pk)
        return redirect(f'/{pk}')


class RemoveLikeView(View):
    def get(self, request, pk):
        ip_user = get_user_ip(request)  # Получаем IP пользователя
        publication = get_object_or_404(Publication, pk=pk)

        # Удаляем лайк, если он существует
        Likes.objects.filter(ip=ip_user, post_id=pk).delete()

        return redirect(f'/{pk}')

