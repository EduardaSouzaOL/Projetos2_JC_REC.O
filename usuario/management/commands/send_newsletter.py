import datetime
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

from jornal_commercio.models import Noticia
from usuario.models import AssinanteNewsletter

class Command(BaseCommand):
    help = 'Envia a newsletter diária para todos os assinantes ativos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Iniciando envio da newsletter..."))

        hoje = datetime.date.today()
    
        noticias = Noticia.objects.filter(data_publicacao__date=hoje)

        if not noticias.exists():
            self.stdout.write(self.style.WARNING("Nenhuma notícia publicada hoje. Saindo."))
            return

        assinantes = AssinanteNewsletter.objects.filter(is_active=True)

        if not assinantes.exists():
            self.stdout.write(self.style.WARNING("Nenhum assinante ativo. Saindo."))
            return

        assunto = f"Seu Resumo Diário de Notícias - {hoje.strftime('%d/%m/%Y')}"
        host_url = settings.DEFAULT_DOMAIN

        contexto_base = {
            'noticias': noticias,
            'host_url': host_url,
            'static_url': settings.STATIC_URL, 
            'edicao_do_dia_url': host_url + '/',
        }
        
        total_enviados = 0
        total_falhas = 0
        
        for assinante in assinantes:
            try:
                unsubscribe_link = host_url + reverse('usuario:unsubscribe_newsletter', 
                                                     kwargs={'token': assinante.unsubscribe_token})

                contexto_assinante = {
                    'noticias': noticias,
                    'host_url': host_url,
                    'unsubscribe_link': unsubscribe_link,
                }
                
                corpo_texto = render_to_string('jornal_commercio/newsletter/email_diario.txt', contexto_assinante)
                corpo_html = render_to_string('jornal_commercio/newsletter/email_diario.html', contexto_assinante)

                send_mail(
                    subject=assunto,
                    message=corpo_texto,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[assinante.email],
                    fail_silently=False,
                    html_message=corpo_html
                )
                
                total_enviados += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao enviar para {assinante.email}: {e}"))
                total_falhas += 1

        self.stdout.write(self.style.SUCCESS(f"Newsletter enviada com sucesso para {total_enviados} assinante(s)."))
        if total_falhas > 0:
            self.stdout.write(self.style.ERROR(f"Falha ao enviar para {total_falhas} assinante(s)."))