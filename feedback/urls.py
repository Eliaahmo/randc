"""
URL configuration for feedback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from zeugnis.views import zeugnis
from zeugnis.views import login, danke
from zeugnis.views import bewertung_view
from zeugnis.views import zeugnis2
from zeugnis.views import mitarbeiter_erstellen
urlpatterns = [
    path("admin/", admin.site.urls),
    path("zeugnis/", zeugnis),
    path("login/", login),
    path("bewertung/" ,bewertung_view),
    path("zeugnis2/", zeugnis2),
    path("danke/", danke, name='danke'),
    path("mitarbeiter/", mitarbeiter_erstellen, name='mitarbeiter_erstellen'),
    path("mitarbeiter/erstellen", mitarbeiter_erstellen, name='mitarbeiter_erstellen'),

    
]
