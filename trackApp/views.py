from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Persona, Presidente, Allenatore, Fisioterapista, Atleta
from .forms import PersonaForm
from .models import Gara
import hashlib
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Vista per la home
def home(request):
    return render(request, 'home.html')

# Vista per il calendario pubblico
def calendario_pubblico(request):
    return render(request, 'trackApp/calendario.html')

# Vista per il login personalizzato
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            utente = Persona.objects.get(email=email, password=hashed_password)
            request.session['utente_id'] = utente.id_persona
            request.session['ruolo'] = utente.tipo_persona
            messages.success(request, f"Benvenuto, {utente.nome}!")
            return redirect('home')
        except Persona.DoesNotExist:
            messages.error(request, 'Credenziali non valide. Riprova.')
    return render(request, 'login.html')

# Vista per il logout personalizzato
def logout_view(request):
    request.session.flush()
    return redirect('home')

# Vista per la registrazione
def registrazione_view(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save(commit=False)
            persona.password = hashlib.md5(persona.password.encode()).hexdigest()
            persona.save()

            # Creazione automatica dell'entità legata al ruolo
            if persona.tipo_persona == 'presidente':
                Presidente.objects.create(persona=persona)
            elif persona.tipo_persona == 'allenatore':
                Allenatore.objects.create(persona=persona)
            elif persona.tipo_persona == 'fisioterapista':
                Fisioterapista.objects.create(persona=persona, specializzazione="Da definire")
            elif persona.tipo_persona == 'atleta':
                Atleta.objects.create(
                    persona=persona,
                    categoria='AM',
                    stato='attivo',
                    id_squadra=None,
                    specialita='100m'
                )

            # 🔐 Impostazione della sessione e redirect alla dashboard
            request.session['utente_id'] = persona.id_persona
            request.session['ruolo'] = persona.tipo_persona
            messages.success(request, f"Registrazione completata! Benvenuto, {persona.nome}.")
            return redirect('dashboard')
        else:
            messages.error(request, 'Errore nei dati inseriti. Ricontrolla il form.')
    else:
        form = PersonaForm()
    return render(request, 'registrazione.html', {'form': form})

# Vista per aggiungere un atleta
def aggiungi_atleta(request):
    return render(request, 'aggiungi_atleta.html')

# Vista per aggiungere una persona
def aggiungi_persona(request):
    return render(request, 'aggiungi_persona.html')

# Vista per aggiungere una gara
def aggiungi_gara(request):
    return render(request, 'aggiungi_gara.html')

# Vista per aggiungere una partecipazione
def aggiungi_partecipazione(request):
    return render(request, 'aggiungi_partecipazione.html')

# Vista per la lista delle gare
def lista_gare(request):
    return render(request, 'lista_gare.html')

# Vista per il dettaglio di una gara
def dettaglio_gara(request, gara_id):
    return render(request, 'dettaglio_gara.html', {'gara_id': gara_id})


def profilo_utente(request):
    if 'utente_id' not in request.session:
        messages.error(request, "Devi essere loggato per accedere al profilo.")
        return redirect('login')

    persona_id = request.session['utente_id']
    persona = get_object_or_404(Persona, id_persona=persona_id)

    contesto = {'persona': persona}

    # Aggiungi dati specifici per ruolo (facoltativo)
    if persona.tipo_persona == 'atleta':
        try:
            atleta = Atleta.objects.get(persona=persona)
            contesto['atleta'] = atleta
        except Atleta.DoesNotExist:
            pass

    return render(request, 'profilo.html', contesto)


#def calendario_view(request):
 #   return render(request, 'trackApp/calendario.html')

def calendario_view(request):
    return render(request, 'trackApp/calendario.html')

def eventi_gare(request):
    eventi = []
    gare = Gara.objects.all()
    if not gare.exists():
        return JsonResponse(eventi, safe=False)  # Restituisce un array vuoto
    for gara in gare:
        eventi.append({
            'title': gara.nome,
            'start': f"{gara.data}T{gara.ora}",
            'url': f"/dettagli-gara/{gara.id}/",
        })
    return JsonResponse(eventi, safe=False)

def dettagli_gara(request, gara_id):
    gara = get_object_or_404(Gara, id=gara_id)
    return render(request, 'trackApp/dettagli_gara.html', {'gara': gara})



def eventi_gare_statici(request):
    eventi = [
        # Golden Circuit Series 2025
        {"title": "Doha – Golden Circuit", "start": "2025-05-10", "end": "2025-05-12", "color": "#007bff"},
        {"title": "Nairobi – Golden Circuit", "start": "2025-05-17", "color": "#007bff"},
        {"title": "Oslo – Golden Circuit", "start": "2025-05-30", "color": "#007bff"},
        {"title": "Parigi – Golden Circuit", "start": "2025-06-14", "color": "#007bff"},

        # Sprint & Field Masters 2025
        {"title": "Los Angeles – Sprint Masters", "start": "2025-06-03", "color": "#28a745"},
        {"title": "Toronto – Sprint Masters", "start": "2025-06-08", "color": "#28a745"},
        {"title": "Monaco – Sprint Masters", "start": "2025-06-15", "color": "#28a745"},
        {"title": "Tokyo – Sprint Masters", "start": "2025-06-22", "color": "#28a745"},
        {"title": "Sydney – Sprint Masters", "start": "2025-06-29", "color": "#28a745"},
        {"title": "Berlino – Grand Final", "start": "2025-07-06", "end": "2025-07-08", "color": "#28a745"},

        # Extra Events
        {"title": "Mixed 4x400m Relay – Monaco", "start": "2025-06-15", "color": "#ffc107"},
        {"title": "Mixed 4x400m Relay – Sydney", "start": "2025-06-29", "color": "#ffc107"},
        {"title": "100m Legends Race", "start": "2025-06-03", "color": "#ffc107"},
        {"title": "60m Indoor – Zurigo", "start": "2025-02-15", "color": "#ffc107"},
        {"title": "4x100m U20 Nations – Toronto", "start": "2025-06-08", "color": "#ffc107"},
        {"title": "Lancio Martello – Tokyo", "start": "2025-06-22", "color": "#ffc107"},
        {"title": "Street Pole Vault – Berlino", "start": "2025-07-05", "color": "#ffc107"},
    ]
    return JsonResponse(eventi, safe=False)

def dashboard_view(request):
    if 'utente_id' not in request.session:
        messages.error(request, "Devi effettuare il login.")
        return redirect('login')

    persona_id = request.session['utente_id']
    persona = get_object_or_404(Persona, id_persona=persona_id)
    ruolo = persona.tipo_persona

    context = {'persona': persona}

    if ruolo == 'atleta':
        atleta = Atleta.objects.filter(persona=persona).first()
        context['checklist'] = [
            "Completa il tuo profilo sportivo",
            "Iscriviti alla tua prima gara",
            "Consulta il calendario gare"
        ]
        context['sezione'] = 'atleta'

    elif ruolo == 'presidente':
        context['checklist'] = [
            "Crea una squadra",
            "Aggiungi atleti",
            "Gestisci le gare"
        ]
        context['sezione'] = 'presidente'

    elif ruolo == 'allenatore':
        context['checklist'] = [
            "Visualizza gli atleti assegnati",
            "Consulta il calendario allenamenti",
            "Monitora prestazioni"
        ]
        context['sezione'] = 'allenatore'

    elif ruolo == 'fisioterapista':
        context['checklist'] = [
            "Visualizza atleti assegnati",
            "Gestisci i trattamenti",
            "Inserisci rapporti clinici"
        ]
        context['sezione'] = 'fisioterapista'

    return render(request, 'TemplateFolder/trackApp/dashboard.html', context)
