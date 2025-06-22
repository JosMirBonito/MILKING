from django.core.management.base import BaseCommand
from django.utils import timezone
from Cliente.pedidos.models import Pedido

class Command(BaseCommand):
    help = 'Actualiza pedidos de "Registrado" a "Aceptado" después de 2 horas'

    def handle(self, *args, **kwargs):
        limite = timezone.now() - timezone.timedelta(seconds=10)  # Cambia a 10 segundos para pruebas
        pedidos = Pedido.objects.filter(estado_envio='Registrado', fecha__lte=limite)
        for pedido in pedidos:
            pedido.estado_envio = 'Aceptado'
            pedido.save()
            self.stdout.write(self.style.SUCCESS(f'Pedido {pedido.id_pedido} aceptado'))