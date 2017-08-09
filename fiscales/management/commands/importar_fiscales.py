from csv import DictReader
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from nameparser import HumanName
from elecciones.models import LugarVotacion, Mesa
from fiscales.models import Fiscal, AsignacionFiscalGeneral
from prensa.forms import DatoDeContactoModelForm





def apellido_nombres(nombre, apellido):
    raw = f'{nombre} {apellido}'.strip()
    nombre = HumanName(raw)
    apellido = nombre.last
    nombres = f'{nombre.first}'
    if nombre.middle:
        nombres += f' {nombre.middle}'
    return apellido, nombres




class Command(BaseCommand):
    help = "importar fiscales generales"


    def add_arguments(self, parser):
        parser.add_argument('csv')


    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def warning(self, msg):
        self.stdout.write(self.style.WARNING(msg))


    def add_telefono(self, objeto, telefono):
        ct = ContentType.objects.get(app_label='fiscales', model=type(objeto).__name__.lower())
        d = DatoDeContactoModelForm({
            'tipo': 'teléfono',
            'valor': telefono,
            'content_type': ct.id,
            'object_id': objeto.id
        })
        if d.is_valid():
            dato = d.save()
            self.success(f'Importado {dato} para {objeto}')
        else:
            self.warning(f'Ignorado {d.errors}')




    def handle(self, *args, **options):
        path = options['csv']
        try:
            data = DictReader(open(path))
        except Exception as e:
            raise CommandError(f'Archivo no válido\n {e}')

        for row in data:
            if not row['Nombres']:
                continue

            if not row['DNI']:
                self.warning(f"{row['Nombre']} fiscal sin dni")
                continue
            apellido, nombres = apellido_nombres(row['Nombres'], row['Apellidos'])
            tipo = 'general' if row['mesa_hasta'] else 'de_mesa'

            fiscal, created = Fiscal.objects.get_or_create(dni=row['DNI'], defaults={
                'nombres': nombres,
                'apellido': apellido
            })
            if created:
                self.success(f'creado {fiscal}')
                self.add_telefono(fiscal, row['Telefono'])
            else:
                self.warning(f'{fiscal} existente (dni {fiscal.dni})')


            if row['mesa_hasta']:
                try:
                    escuela = LugarVotacion.objects.filter(mesas__numero=row['mesa_desde']).get(mesas__numero=row['mesa_hasta'])

                except LugarVotacion.DoesNotExist:
                    self.warning(f"No se encontró escuela para row['mesa_desde'] - row['mesa_hasta']")
                    continue

                asignacion, created = AsignacionFiscalGeneral.objects.get_or_create(fiscal=fiscal, lugar_votacion=escuela)
                if created:
                    self.success(f'creado {asignacion}')
                else:
                    self.warning(f'{asignacion} ya existia')


            else:
                try:
                    mesa = Mesa.objects.get(numero=row['mesas_desde'])
                except Mesa.DoesNotExist:
                    self.warning(f"No se encontró mesa row['mesas_desde']")
                    continue

                asignacion, created = AsignacionDeMesa.objects.get_or_create(fiscal=fiscal, mesa=mesa)
                if created:
                    self.success(f'creado {asignacion}')
                else:
                    self.warning(f'{asignacion} ya existia')

