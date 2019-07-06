from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from .models import OrderLetters, Word, TraningWord, WordError
from .forms import OrderLettersEditForm, WordEditForm, UploadFileForm
import random


# Create your views here.
class OrderLettersListView(ListView):
    model = OrderLetters

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderLettersCreateView(CreateView):
    model = OrderLetters
    success_url = reverse_lazy('dictionary:order_list')
    form_class = OrderLettersEditForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OrderLettersUpdateView(UpdateView):
    model = OrderLetters
    success_url = reverse_lazy('dictionary:order_list')
    form_class = OrderLettersEditForm


class OrderLettersDeleteView(DeleteView):
    model = OrderLetters
    success_url = reverse_lazy('dictionary:order_list')


class OrderLetterDetailView(DetailView):
    model = OrderLetters


class GameDetailView(DetailView):
    """
    See - Write training
    """
    model = OrderLetters
    template_name = 'dictionary/game.html'


class GameHideDetailView(DetailView):
    """
    Hide traning
    """
    model = OrderLetters
    template_name = 'dictionary/game_hide.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_time'] = self.request.user.show_time
        return context

# СЛова

class WordListView(ListView):
    model = Word
    # TODO: вывести пагинацию на стрнице
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['obj_count'] = self.model.objects.count()
        return context


class WordCreateView(CreateView):
    model = Word
    success_url = reverse_lazy('dictionary:word_list')
    form_class = WordEditForm


class WordUpdateView(UpdateView):
    model = Word
    success_url = reverse_lazy('dictionary:word_list')
    form_class = WordEditForm


class WordDeleteView(DeleteView):
    model = Word
    success_url = reverse_lazy('dictionary:word_list')


def word_delete_all(request):
    if request.method == 'POST':
        Word.objects.all().delete()
        return HttpResponseRedirect(reverse('dictionary:word_list'))
    else:
        raise Http404


def handle_uploaded_file(f):
    # TODO: перенести логику создания слов в модель, она будет использоваться и при добавлении 1-го слова
    # destination = open('some/file/name.txt', 'wb+')
    # for chunk in f.chunks():
    # destination.write(chunk)
    # print('FILE: !!!!', f.multiple_chunks())
    # destination.close()
    if f.multiple_chunks():
        # TODO: сдлеать загузку файла по частям если он очень большой
        pass
    else:
        text = f.read()
        text = text.decode('utf-8')
        words = text.split('\n')
        result = []
        for word in words:
            if word and word != '\n':
                # Создаем слово если его еще нету в базе
                # Если ест желательно это увидеть
                ERROR_KEY = 'error'
                # good_word = str(word).lower().replace(' ', '').replace('\n', '').replace('\t', '').rstrip()
                good_word = word.lower().rstrip()

                # print('good_word', good_word)
                # print('len', len(good_word))
                word_result = {'name': good_word, ERROR_KEY: False}
                try:
                    new_word = Word.objects.create(name=good_word)
                except Exception:
                    word_result[ERROR_KEY] = True
                    result.append(word_result)
                # else:
                #     # Если слово прошло, добавляем знаки припинания [ ] ; ' \ , . /
                #     end_simbols = [',', '.', ';']
                #     for item in end_simbols:
                #         new_name = new_word.name + item
                #         Word.objects.create(name=new_name)
                #
                #     random_simbols = ['/', '\\']
                #     for item in random_simbols:
                #         if random.random() > 0.5:
                #             new_name = new_word.name + item
                #         else:
                #             new_name = item + new_word.name
                #         Word.objects.create(name=new_name)
                #
                #     pair_simbols = [('[', ']')]
                #     for item in pair_simbols:
                #         new_name = item[0] + new_word.name + item[1]
                #         Word.objects.create(name=new_name)
                #
                #     both_simbols = ['\'']
                #     for item in both_simbols:
                #         new_name = item + new_word.name + item
                #         Word.objects.create(name=new_name)

        return result


def add_specsimbols(request):
    if request.method == 'POST':
        words = Word.objects.all()
        words_count = words.count()
        current_words = 1
        end_simbols = [',', '.', ';', '!', ':', '?']
        random_simbols = ['/', '\\', '-', '=', '$', '%', '&', '*', '_', '+', '|']
        pair_simbols = [('[', ']'), ('(', ')'), ('{', '}'), ('<', '>')]
        both_simbols = ['\'', '"']
        start_simbols = ['@', '#', '^']

        #ADD_CHANCE = 0.7

        wariants = [0, 1, 2, 3, 4, 5]

        for word in words:
            wariant = random.choice(wariants)
            if wariant == 0:
                # Добавляем такой же слова но с заглавной буквы
                Word.objects.create(name=word.name.title())
            elif wariant == 1:
                # Добавляем спецсимволы
                for item in end_simbols:
                    new_name = word.name + item
                    Word.objects.create(name=new_name)
            elif wariant == 2:
                for item in start_simbols:
                    #if random.random() > ADD_CHANCE:
                    new_name = item + word.name
                    Word.objects.create(name=new_name)
            elif wariant == 3:

                for item in random_simbols:
                    #if random.random() > ADD_CHANCE:
                    if random.random() > 0.5:
                        new_name = word.name + item
                    else:
                        new_name = item + word.name
                    Word.objects.create(name=new_name)

            elif wariant == 4:
                for item in pair_simbols:
                    #if random.random() > ADD_CHANCE:
                    new_name = item[0] + word.name + item[1]
                    Word.objects.create(name=new_name)

            elif wariant == 5:
                for item in both_simbols:
                    #if random.random() > ADD_CHANCE:
                    new_name = item + word.name + item
                    Word.objects.create(name=new_name)

            persent = int((current_words/words_count)*100)
            print(word.name, ':', persent, '%')
            current_words+=1

        return HttpResponseRedirect(reverse('dictionary:word_list'))

    else:
        raise Http404


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result = handle_uploaded_file(request.FILES['file'])
            return render(request, 'dictionary/upload.html', {'form': form, 'result': result})
    else:
        form = UploadFileForm()
    return render(request, 'dictionary/upload.html', {'form': form})


class TraningWordList(ListView):
    model = TraningWord
    # TODO: вывести пагинацию на стрнице
    paginate_by = 100

    def get(self, request, *args, **kwargs):
        order_letters_pk = kwargs['pk']
        self.order_lettres = get_object_or_404(OrderLetters, pk=order_letters_pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['order_letters'] = self.order_lettres
        context['obj_count'] = self.model.objects.count()
        return context

    def get_queryset(self):
        return self.order_lettres.traningword_set.all().order_by('last_letter_order')


@transaction.atomic
def create_traning_words(request, order_letters_pk):
    if request.method == 'POST':
        # Получаем последовательность
        order_letters = get_object_or_404(OrderLetters, pk=order_letters_pk)
        # Надо создать слова для тренировки из слов из словаря

        # Удаляем то что уже есть
        TraningWord.objects.filter(order_letters=order_letters).delete()
        # Получаем слова для словаря
        words = Word.objects.all()
        for word in words:
            try:
                TraningWord.objects.create(base_word=word, order_letters=order_letters)
            except WordError:
                # TODO: обработать ошибки
                pass
        return HttpResponseRedirect(reverse('dictionary:traning_word_list', kwargs={'pk': order_letters.pk}))
    else:
        raise Http404


def set_next_level(request, pk):
    if request.method == 'POST':
        order_letters = get_object_or_404(OrderLetters, pk=pk)
        order_letters.save_next_letter()
        return HttpResponseRedirect(reverse('dictionary:game', kwargs={'pk': order_letters.pk}))
    else:
        raise Http404


def set_prev_level(request, pk):
    if request.method == 'POST':
        order_letters = get_object_or_404(OrderLetters, pk=pk)
        order_letters.save_prev_letter()
        return HttpResponseRedirect(reverse('dictionary:game', kwargs={'pk': order_letters.pk}))
    else:
        raise Http404
