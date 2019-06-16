from django.urls import path
from dictionary import views

app_name = 'dictionary'

urlpatterns = [
    path('order-list', views.OrderLettersListView.as_view(), name='order_list'),
    path('order-create', views.OrderLettersCreateView.as_view(), name='order_create'),
    path('order-delete/<int:pk>/', views.OrderLettersDeleteView.as_view(), name='order_delete'),
    path('order-update/<int:pk>/', views.OrderLettersUpdateView.as_view(), name='order_update'),
    path('order-detail/<int:pk>/', views.OrderLetterDetailView.as_view(), name='order_detail'),

    path('order-next-level/<int:pk>/', views.set_next_level, name='order_next_level'),
    path('order-prev-level/<int:pk>/', views.set_prev_level, name='order_prev_level'),

    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game'),

    path('word-list', views.WordListView.as_view(), name='word_list'),
    path('word-create', views.WordCreateView.as_view(), name='word_create'),
    path('word-delete/<int:pk>/', views.WordDeleteView.as_view(), name='word_delete'),
    path('word-update/<int:pk>/', views.WordUpdateView.as_view(), name='word_update'),
    path('word-file-upload/', views.upload_file, name='word_file_upload'),
    path('word-delete-all/', views.word_delete_all, name='word_delete_all'),

    path('traning-word-list/<int:pk>/', views.TraningWordList.as_view(), name='traning_word_list'),
    path('create-traning-word/<int:order_letters_pk>/', views.create_traning_words, name='create_traning_word'),
]
