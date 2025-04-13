from django.urls import path
from . import views


urlpatterns = [path('', views.PublicationView.as_view(), name='home_screen'),
               path('<int:pk>/', views.SingleEntryView.as_view(), name='single_entry'),
               path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
               path('review/<int:pk>/', views.AddCommentView.as_view(), name='add_comment'),
               path('<int:pk>/add_like/', views.AddLikeView.as_view(), name='add_like'),
               path('<int:pk>/delete_like/', views.RemoveLikeView.as_view(), name='remove_like')
               ]
