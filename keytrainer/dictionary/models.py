from django.db import models
from core.models import AbstractUniqueSlugifyNamedObj, AbstractUniqueNamedObj
from django.conf import settings
import random


class WordError(Exception):

    def __str__(self):
        # TODO: сделать нормальный вывод ошибки
        return 'Слово не подходит для последовательности'


class OrderLetters(models.Model):
    """
    Порядок букв
    """
    name = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_letter = models.CharField(max_length=1, default='a')
    current_letter_order = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    def get_current_words(self, count=None, is_random=True):
        words = TraningWord.get_current_words(self.current_letter, self)

        #print(words)
        if is_random:
            random.shuffle(words)
        if count:
            words = words[:count]


        return words

    def get_current_text(self):
        user_count = self.user.words_count
        words = self.get_current_words(user_count, True)

        while user_count > len(words):
            words.append(random.choice(words))


        return ' '.join(words)

    def save_next_letter(self):
        next_letter_order = self.current_letter_order + 1
        if len(self.name) > next_letter_order:
            self.current_letter_order = next_letter_order
            self.current_letter = self.name[self.current_letter_order]
            self.save()

    def save_prev_letter(self):
        new_letter_order = self.current_letter_order - 1
        if new_letter_order >= 0:
            self.current_letter_order = new_letter_order
            self.current_letter = self.name[self.current_letter_order]
            self.save()

    def save(self, *args, **kwargs):
        # создаем 1-ый раз
        if not self.pk:
            FIRST_LETTER_INDEX = 0
            self.current_letter = self.name[FIRST_LETTER_INDEX]
            self.current_letter_order = FIRST_LETTER_INDEX
        return super().save(*args, **kwargs)

    def get_letter_order(self, letter):
        return str(self.name).index(letter)

    def get_last_letter(self, text):
        for item in text:
            if item not in self.name:
                raise WordError
        # Идем с конца
        for letter in self.name[::-1]:
            if letter in text:
                return letter
        # Если ничего не нашли, то ошибка
        raise WordError


class Word(AbstractUniqueNamedObj):
    unique_letters = models.CharField(max_length=16)

    def unique_letter_by_name(self):
        result = set()
        for letter in self.name:
            result.add(letter)

        return ''.join(result)

    def save(self, *args, **kwargs):
        self.unique_letters = self.unique_letter_by_name()
        return super().save(*args, **kwargs)


class TraningWord(models.Model):
    base_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    order_letters = models.ForeignKey(OrderLetters, on_delete=models.CASCADE)
    last_letter = models.CharField(max_length=1, blank=True)
    last_letter_order = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ['last_letter_order']

    @property
    def name(self):
        return self.base_word.name

    def save(self, *args, **kwargs):
        last_letter = self.order_letters.get_last_letter(self.base_word.name)
        self.last_letter = last_letter
        last_letter_order = self.order_letters.get_letter_order(last_letter)
        self.last_letter_order = last_letter_order
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('base_word', 'order_letters')

    @classmethod
    def get_current_words(cls, current_letter, order_letters):
        words = cls.objects.filter(last_letter_order__lte=order_letters.get_letter_order(current_letter), order_letters=order_letters)
        words = [word.name for word in words]
        return words
