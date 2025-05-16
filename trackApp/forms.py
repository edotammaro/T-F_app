from django import forms
from .models import Persona, Atleta, Gara, PartecipaGara, Specialita


class PersonaForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Persona
        fields = ['nome', 'cognome', 'data_nascita', 'sesso', 'email', 'telefono', 'tipo_persona', 'password']



#class PersonaForm(forms.ModelForm):
 #   class Meta:
  #      model = Persona
   #     fields = '__all__'

class AtletaForm(forms.ModelForm):
    specialita = forms.ModelMultipleChoiceField(
        queryset=Specialita.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Atleta
        fields = ['categoria', 'stato', 'id_squadra', 'specialita']

class GaraForm(forms.ModelForm):
    class Meta:
        model = Gara
        fields = '__all__'

class PartecipazioneGaraForm(forms.ModelForm):
    class Meta:
        model = PartecipaGara
        fields = '__all__'
