from django.urls import path

from . import views


# allows for namespacing 
app_name = 'recipes'
# recipes app URLs
urlpatterns = [
    # page for a list of recipes
    path('', views.recipe_list, name='recipe_list'),
    # page for list of sessions for a given recipe primary key
    path('<recipe_pk>/sessions/', views.recipe_sessions, name='sessions'),
    # path for a new session here!!!
    path('<recipe_pk>/new_session/', views.new_session, name='new_session'),
    # page for the details of a given session
    path('<recipe_pk>/session_detail/<session_pk>/', views.session_detail,
        name='session_detail'),
    # page for the timer of a brew session
    path('<recipe_pk>/session_timer/<session_pk>/', views.session_timer,
        name='session_timer'),
    # page for details of a particular recipe
    path('<pk>/<slug>/', views.recipe_detail, name='recipe_detail'),
]
