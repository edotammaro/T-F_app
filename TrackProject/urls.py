from django.contrib import admin
from django.urls import path
from trackApp.views import (
    home, calendario_pubblico, login_view, logout_view, registrazione_view,
    aggiungi_atleta, aggiungi_persona, aggiungi_gara, aggiungi_partecipazione,
    lista_gare, dettaglio_gara, profilo_utente
)
from trackApp import views
from django.urls import path
from trackApp import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('calendario/', calendario_pubblico, name='calendario'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registrazione/', registrazione_view, name='registrazione'),
    path('presidente/aggiungi_atleta/', aggiungi_atleta, name='aggiungi_atleta'),
    path('presidente/aggiungi_persona/', aggiungi_persona, name='aggiungi_persona'),
    path('regione/aggiungi_gara/', aggiungi_gara, name='aggiungi_gara'),
    path('partecipazione/aggiungi/', aggiungi_partecipazione, name='aggiungi_partecipazione'),
    path('gare/', lista_gare, name='lista_gare'),
    path('gare/<int:gara_id>/', dettaglio_gara, name='dettaglio_gara'),
    path('profilo/', profilo_utente, name='profilo_utente'),
    path('eventi-gare/', views.eventi_gare, name='eventi_gare'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('eventi-gare/', views.eventi_gare, name='eventi_gare'),
    path('dettagli-gara/<int:gara_id>/', views.dettagli_gara, name='dettagli_gara'),
    path('eventi-gare-statici/', views.eventi_gare_statici, name='eventi_gare_statici'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    



]