from django.test import TestCase
from mixer.backend.django import mixer
from .models import Word, OrderLetters, TraningWord, WordError


class TestWord(TestCase):

    def setUp(self):
        self.full_obj = mixer.blend(Word, name='muffin')
        self.full_obj_uletter = 'mufin'

    def chech_by_letters(self, name, result):
        for letter in name:
            self.assertIn(letter, result)
        self.assertEqual(len(name), len(result))

    def test_unique_letter_by_name(self):
        self.chech_by_letters(self.full_obj_uletter, self.full_obj.unique_letter_by_name())

    def test_save(self):
        self.chech_by_letters(self.full_obj_uletter, self.full_obj.unique_letters)


class TestOrderLetters(TestCase):

    def setUp(self):
        self.order_letters = mixer.blend(OrderLetters, name='abcd')
        self.order_letters_other = mixer.blend(OrderLetters, name='dcab')

    def test_get_letter_order(self):
        self.assertEqual(self.order_letters.get_letter_order('a'), 0)
        self.assertEqual(self.order_letters.get_letter_order('c'), 2)
        with self.assertRaises(ValueError):
            self.order_letters.get_letter_order('e')

    def test_last_letter(self):
        self.assertEqual(self.order_letters.get_last_letter('a'), 'a')
        self.assertEqual(self.order_letters.get_last_letter('ba'), 'b')
        self.assertEqual(self.order_letters.get_last_letter('ca'), 'c')
        self.assertEqual(self.order_letters.get_last_letter('db'), 'd')

        # другая последовательность
        self.assertEqual(self.order_letters_other.get_last_letter('db'), 'b')

        # Буквы нет в поледовательности
        with self.assertRaises(WordError):
            self.order_letters.get_last_letter('ef')
        # self.assertEqual(self.order_letters.get_last_letter('db'), 'd')
        # В слове есть буквы, которых нет в последовательности
        with self.assertRaises(WordError):
            self.order_letters.get_last_letter('abh')

    def test_set_first_letter(self):
        self.assertEqual(self.order_letters.current_letter, 'a')
        self.assertEqual(self.order_letters.current_letter_order, 0)

        # Предыдущий уровень когда не должен поменяться
        self.order_letters.save_prev_letter()
        self.assertEqual(self.order_letters.current_letter, 'a')
        self.assertEqual(self.order_letters.current_letter_order, 0)

        self.assertEqual(self.order_letters_other.current_letter, 'd')
        self.assertEqual(self.order_letters_other.current_letter_order, 0)

        self.order_letters.save_next_letter()
        self.assertEqual(self.order_letters.current_letter, 'b')
        self.assertEqual(self.order_letters.current_letter_order, 1)

        self.order_letters.save_next_letter()
        self.assertEqual(self.order_letters.current_letter, 'c')
        self.assertEqual(self.order_letters.current_letter_order, 2)

        self.order_letters.save_next_letter()
        self.assertEqual(self.order_letters.current_letter, 'd')
        self.assertEqual(self.order_letters.current_letter_order, 3)

        # когда последняя буква
        self.order_letters.save_next_letter()
        self.assertEqual(self.order_letters.current_letter, 'd')
        self.assertEqual(self.order_letters.current_letter_order, 3)

        # предыдущий уровень
        self.order_letters.save_prev_letter()
        self.assertEqual(self.order_letters.current_letter, 'c')
        self.assertEqual(self.order_letters.current_letter_order, 2)

class TestTraningWord(TestCase):

    def setUp(self):
        self.order_letters = mixer.blend(OrderLetters, name='abcd')
        word = mixer.blend(Word, name='abba')
        self.tw = mixer.blend(TraningWord, base_word=word, order_letters=self.order_letters)
        word = mixer.blend(Word, name='cab')
        mixer.blend(TraningWord, base_word=word, order_letters=self.order_letters)
        word = mixer.blend(Word, name='db')
        mixer.blend(TraningWord, base_word=word, order_letters=self.order_letters)
        word = mixer.blend(Word, name='a')
        mixer.blend(TraningWord, base_word=word, order_letters=self.order_letters)

    def test_save_last_letter(self):
        self.assertEqual(self.tw.last_letter, 'b')
        self.assertEqual(self.tw.last_letter_order, 1)

    def test_get_current_words(self):
        # получение слов по текущей букве
        words = TraningWord.get_current_words('a', self.order_letters)
        self.assertEqual(len(words), 1)

        words = TraningWord.get_current_words('b', self.order_letters)
        self.assertEqual(len(words), 2)

        words = TraningWord.get_current_words('c', self.order_letters)
        self.assertEqual(len(words), 3)

        words = TraningWord.get_current_words('d', self.order_letters)
        self.assertEqual(len(words), 4)

        words = self.order_letters.get_current_words()
        self.assertEqual(len(words), 1)

        self.assertEqual(words[0], 'a')

        self.order_letters.save_next_letter()
        words = self.order_letters.get_current_words()
        self.assertEqual(len(words), 2)

        self.order_letters.save_next_letter()
        words = self.order_letters.get_current_words(count=1)
        self.assertEqual(len(words), 1)

        self.order_letters.save_next_letter()
        words = self.order_letters.get_current_words(count=1, is_random=True)
        self.assertEqual(len(words), 1)