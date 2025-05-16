# trackApp/models.py
from django.db import models

class Persona(models.Model):
    TIPO_PERSONA = [
        ('presidente', 'Presidente'),
        ('allenatore', 'Allenatore'),
        ('fisioterapista', 'Fisioterapista'),
        ('atleta', 'Atleta'),
    ]

    SESSO = [
        ('M', 'Maschio'),
        ('F', 'Femmina'),
    ]

    id_persona = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    data_nascita = models.DateField()
    sesso = models.CharField(max_length=1, choices=SESSO)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    tipo_persona = models.CharField(max_length=20, choices=TIPO_PERSONA)
    password = models.CharField(max_length=64)  # MD5 hash (32) può stare anche su 64 per sicurezza

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.tipo_persona})"

class Presidente(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

class Allenatore(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

class Fisioterapista(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    specializzazione = models.CharField(max_length=100)

class Squadra(models.Model):
    nome_squadra = models.CharField(max_length=50)
    presidente = models.OneToOneField(Presidente, on_delete=models.CASCADE, null=True, blank=True)

class Atleta(models.Model):
    CATEGORIA = [
        ('AM', 'Allievi Maschi'),
        ('AF', 'Allieve Femmine'),
        ('JR', 'Juniores'),
        ('PM', 'Promesse'),
        ('SM', 'Senior'),
        ('SM35', 'Senior 35'),
        # Aggiungi altre categorie
    ]
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=10, choices=CATEGORIA)
    stato = models.CharField(max_length=20)
    id_squadra = models.ForeignKey(Squadra, on_delete=models.SET_NULL, null=True)
    specialita = models.CharField(max_length=100)  # valori come "100m", "200m", ecc.


class Specialita(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Gara(models.Model):
    data = models.DateField()
    ora = models.TimeField()
    luogo = models.CharField(max_length=100)
    specialita = models.ForeignKey(Specialita, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    # id_regione e id_torneo possono essere aggiunti se servono

    def __str__(self):
        return f"{self.nome} - {self.data}"


class PartecipaGara(models.Model):
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    gara = models.ForeignKey(Gara, on_delete=models.CASCADE)
    tempo_prestazione = models.FloatField(null=True, blank=True)
    punti = models.IntegerField(null=True, blank=True)
    posizione = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.atleta.persona.nome} in {self.gara.nome}"
