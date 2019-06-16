# from django.test import TestCase
# from mixer.backend.django import mixer
# from .models import NamedObj
#
#
# class TestNamedObj(TestCase):
#
#     def test_save(self):
#         obj = mixer.blend(NamedObj, name='obj name')
#         assert obj.slug == 'obj-name'
#         # на русском
#         obj = mixer.blend(NamedObj, name='имя объекта')
#         assert obj.slug == 'imia-obekta'
#
#     def test_is_created_updated(self):
#         obj = NamedObj(name='new')
#         assert obj.is_new
#         obj.save()
#         assert not obj.is_new
