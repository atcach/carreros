from django import forms
from .models import Attachment
from elecciones.models import Mesa


class AsignarMesaForm(forms.ModelForm):
    mesa = forms.IntegerField(label='Nº Mesa',
        required=False,
        help_text='A que número pertenece esta acta'
    )
    mesa_confirm = forms.IntegerField(required=False)


    class Meta:
        model = Attachment
        fields = ['mesa', 'problema', 'mesa_confirm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mesa'].widget.attrs['tabindex'] = 1
        self.fields['mesa'].widget.attrs['autofocus'] = True
        self.fields['problema'].widget.attrs['tabindex'] = 99


    def clean_mesa(self):
        numero = self.cleaned_data['mesa']
        if not numero:
            return numero
        try:
            mesa = Mesa.objects.get(numero=numero, eleccion__id=1)
        except Mesa.DoesNotExist:
            raise forms.ValidationError('No existe una mesa con este numéro')
        return mesa


    def clean(self):
        cleaned_data = super().clean()
        problema = cleaned_data.get('problema')
        mesa = cleaned_data.get('mesa')
        mesa_confirm = cleaned_data.get('mesa_confirm')

        if not mesa and not problema:
            self.add_error(
                'mesa', 'Indicá la mesa o reportá un problema'
            )

        elif problema and mesa:
            cleaned_data['mesa'] = None
            self.add_error(
                'problema', 'Dejá el número en blanco si hay un problema'
            )

        if mesa and Attachment.objects.filter(mesa=mesa).exists() and mesa.numero != mesa_confirm:
            self.data._mutable = True
            self.data['mesa_confirm'] = mesa.numero
            self.data._mutable = False
            self.add_error(
                'mesa', 'Esta mesa ya tiene imagen adjunta. Revisá y guardá de nuevo para confirmar'
            )

        return cleaned_data


class SubirAttachmentModelForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['foto']