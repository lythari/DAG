from django.urls import path

import homepage.views as homepage_views

app_name = "homepage"

urlpatterns = [
    path("", homepage_views.home, name="home")
]
