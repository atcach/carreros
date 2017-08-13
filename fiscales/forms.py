from django import forms
from django.forms.models import modelform_factory
from django.forms import modelformset_factory, BaseModelFormSet
from material import Layout, Row
from .models import Fiscal
from elecciones.models import Mesa, VotoMesaReportado, Eleccion
from localflavor.ar.forms import ARDNIField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


OPCION_CANTIDAD_DE_SOBRES = 22
OPCION_HAN_VOTADO = 21
OPCION_DIFERENCIA = 23
OPCION_TOTAL_VOTOS = 20


class AuthenticationFormCustomError(AuthenticationForm):
    error_messages = {
        'invalid_login': "Por favor introduzca un nombre de usuario y una contraseña correctos. Prueba tu DNI o teléfono sin puntos, guiones ni espacios",
        'inactive': _("This account is inactive."),
    }



def opciones_actuales():
    try:
        return Eleccion.opciones_actuales().count()
    except:
        return 0


class FiscalForm(forms.ModelForm):

    dni = ARDNIField(required=False)

    class Meta:
        model = Fiscal
        exclude = []


class MisDatosForm(FiscalForm):
    class Meta:
        model = Fiscal
        fields = [
            'nombres', 'apellido',
            'direccion', 'localidad',
            'barrio',
            'tipo_dni', 'dni',
            'organizacion'
        ]


class FiscalFormSimple(FiscalForm):

    class Meta:
        model = Fiscal
        fields = [
            'nombres', 'apellido',
            'dni',
        ]



class VotoMesaModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['opcion'].label = ''
        self.fields['votos'].label = ''
        self.fields['votos'].required = False

        # self.fields['opcion'].widget.attrs['disabled'] = 'disabled'

    # layout = Layout(Row('opcion', 'votos'))

    class Meta:
        model = VotoMesaReportado
        fields = ('opcion', 'votos')


class BaseVotoMesaReportadoFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.warnings = []


    def clean(self):
        super().clean()
        suma = 0
        for form in self.forms:
            opcion = form.cleaned_data['opcion']
            if opcion.id == OPCION_CANTIDAD_DE_SOBRES:
                cantidad_sobres = form.cleaned_data.get('votos') or 0
            elif opcion.id == OPCION_HAN_VOTADO:
                han_votado = form.cleaned_data.get('votos') or 0
            elif opcion.id == OPCION_DIFERENCIA:
                diferencia = form.cleaned_data.get('votos') or 0
                form_opcion_dif = form
            elif opcion.id == OPCION_TOTAL_VOTOS:
                form_opcion_total = form
                total_en_acta = form.cleaned_data.get('votos') or 0
            else:
                suma += form.cleaned_data.get('votos') or 0

        if abs(diferencia) != abs(cantidad_sobres - han_votado):

            # form_opcion_dif.add_error('votos', 'Diferencia no válida')
            self.warnings.append((form_opcion_dif, 'votos', 'Diferencia no valida'))

        if suma != total_en_acta:
            #form_opcion_total.add_error(
            #    'votos', 'La sumatoria no se corresponde con el total'
            #)
            self.warnings.append((form_opcion_total, 'votos', 'La sumatoria no se corresponde con el total'))

        if cantidad_sobres != total_en_acta:
            # form_opcion_total.add_error(
            #    'votos', 'El total no corresponde a la cantidad de sobres'
            # )
            self.warnings.append((form_opcion_total, 'votos', 'El total no corresponde a la cantidad de sobres'))


VotoMesaReportadoFormset = modelformset_factory(
    VotoMesaReportado, form=VotoMesaModelForm,
    formset=BaseVotoMesaReportadoFormSet,
    min_num=opciones_actuales(), extra=0, can_delete=False
)


EstadoMesaModelForm = modelform_factory(
    Mesa,
    fields=['estado'],
    widgets={"estado": forms.HiddenInput}
)


ActaMesaModelForm = modelform_factory(
    Mesa,
    fields=['foto_del_acta'],
)
