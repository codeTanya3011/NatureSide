from django.db import models


class Publication(models.Model):
    title = models.CharField('Заголовок запису', max_length=100)
    description = models.TextField('Текст запису')
    author = models.CharField('Автор', max_length=100)
    date = models.DateField('Дата публікації')

    # Мультимедіа
    img = models.ImageField('Зображення', upload_to='images/%Y', blank=True, null=True)
    video = models.FileField('Відео', upload_to='videos/%Y', blank=True, null=True)
    audio = models.FileField('Аудіо', upload_to='audios/%Y', blank=True, null=True)

    def __str__(self):
        return f'{self.title}, {self.author}'

    class Meta:
        verbose_name = 'Публікація'
        verbose_name_plural = 'Публікації'


class Comment(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=50)
    text_comments = models.TextField('Текст коментаря', max_length=2000)
    post = models.ForeignKey(Publication, verbose_name='Публікація', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавляем дату создания

    def __str__(self):
        return f'{self.name}, {self.post}'

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'


class Likes(models.Model):
    ip = models.CharField('IP-адрес', max_length=50)
    post = models.ForeignKey(Publication, verbose_name='Публікація', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ip', 'post'], name='unique_like_per_ip')
        ]
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'Лайк від {self.ip} для {self.post}'
