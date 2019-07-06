from django.core.management.base import BaseCommand
from dictionary.models import TraningWord




class Command(BaseCommand):


    def handle(self, *args, **options):
       items = TraningWord.objects.select_related('base_word')
       count = items.count()
       i=0
       for item in items:
           i+=1
           item.name = item.base_word.name
           item.save()
           print(f'{i} from {count}: {(i/count)*100} %')

