# Projetos2_JC_REC.O/usuario/tests.py

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Interesse, AssinanteNewsletter
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

class UsuarioSeleniumTests(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        nomes = ['Política', 'Segurança', 'Saúde', 'Educação', 'Esporte', 'Entretenimento']
        for nome in nomes:
            Interesse.objects.get_or_create(nome=nome)

    def test_login_usuario_existente(self):
        """
        Testa o fluxo de login usando os IDs específicos do seu HTML (login.html)
        """
        
        senha = 'SenhaForte123!'
        user = User.objects.create_user(username='teste@jc.com', email='teste@jc.com', password=senha)
        
        self.selenium.get(f'{self.live_server_url}/usuario/login/')
        
        campo_email = self.selenium.find_element(By.ID, 'id_username')
        campo_senha = self.selenium.find_element(By.ID, 'id_password')
        
        campo_email.send_keys('teste@jc.com')
        campo_senha.send_keys(senha)
        
        btn_entrar = self.selenium.find_element(By.CSS_SELECTOR, 'button.btn-login-submit')
        btn_entrar.click()
        
        self.assertNotEqual(self.selenium.current_url, f'{self.live_server_url}/usuario/login/')

    def test_wizard_registro_completo(self):
        """
        Testa Passo a Passo: Dados -> Senha -> Frequência -> Interesses -> Sucesso
        """
        # ================= PASSO 1: DADOS PESSOAIS =================
        self.selenium.get(f'{self.live_server_url}/usuario/registrar/')
        
        self.selenium.find_element(By.NAME, 'nome_completo').send_keys('Novo Assinante Selenium')
        self.selenium.find_element(By.NAME, 'email').send_keys('novo@selenium.com')
        
        self.selenium.find_element(By.NAME, 'data_nascimento').send_keys('01011995')
        
        self.selenium.find_element(By.NAME, 'cidade').send_keys('Recife')
        self.selenium.find_element(By.NAME, 'estado').send_keys('Pernambuco')
        
        self.selenium.find_element(By.CSS_SELECTOR, 'button.btn-login-submit').click()

        WebDriverWait(self.selenium, 10).until(EC.url_contains('/registrar/senha/'))
        
        self.selenium.find_element(By.NAME, 'senha').send_keys('SenhaForte123!')
        self.selenium.find_element(By.NAME, 'confirme_a_senha').send_keys('SenhaForte123!')
        
        self.selenium.find_element(By.CSS_SELECTOR, 'button.btn-login-submit').click()

        WebDriverWait(self.selenium, 10).until(EC.url_contains('/registrar/frequencia/'))
        
        radio_btn = self.selenium.find_element(By.CSS_SELECTOR, "input[name='frequencia'][value='uma_vez']")
        self.selenium.execute_script("arguments[0].click();", radio_btn)
        
        self.selenium.find_element(By.CSS_SELECTOR, 'button.btn-login-submit').click()

        WebDriverWait(self.selenium, 10).until(EC.url_contains('/registrar/interesses/'))
        
        chk_esporte = self.selenium.find_element(By.CSS_SELECTOR, "input[name='interesses'][value='esporte']")
        chk_politica = self.selenium.find_element(By.CSS_SELECTOR, "input[name='interesses'][value='politica']")
        
        self.selenium.execute_script("arguments[0].click();", chk_esporte)
        self.selenium.execute_script("arguments[0].click();", chk_politica)
        
        self.selenium.find_element(By.CSS_SELECTOR, 'button.btn-login-submit').click()

        WebDriverWait(self.selenium, 10).until(EC.url_contains('/registrar/sucesso/'))
        
        body_text = self.selenium.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Cadastro feito com sucesso', body_text)
        
        usuario_criado = User.objects.filter(email='novo@selenium.com').exists()
        self.assertTrue(usuario_criado, "O usuário deveria ter sido criado no banco de dados")
        
        user_db = User.objects.get(email='novo@selenium.com')
        interesses_db = user_db.perfil.interesses.values_list('nome', flat=True)
        self.assertIn('Esporte', interesses_db)
        self.assertIn('Política', interesses_db)
        
class NewsletterSeleniumTests(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(5) 

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_cenario_1_inscricao_newsletter(self):

        email_teste = "novo.leitor@teste.com"

        url_pagina = self.live_server_url + reverse('usuario:newsletter_page')
        self.selenium.get(url_pagina)

        campo_email = self.selenium.find_element(By.NAME, 'email')
        campo_email.clear()
        campo_email.send_keys(email_teste)

        botao_inscrever = self.selenium.find_element(By.CSS_SELECTOR, '.newsletter-button')
        botao_inscrever.click()

        WebDriverWait(self.selenium, 10, ignored_exceptions=[StaleElementReferenceException]).until(
            lambda driver: "sucesso" in driver.find_element(By.TAG_NAME, "body").text.lower()
        )

        body_text = self.selenium.find_element(By.TAG_NAME, 'body').text
        self.assertIn("sucesso", body_text.lower(), "A mensagem de sucesso não apareceu na tela.")

        assinante = AssinanteNewsletter.objects.get(email=email_teste)
        self.assertTrue(assinante.is_active, "O usuário deveria estar ativo no banco.")

    def test_cenario_3_cancelamento_newsletter(self):

        email_cancelar = "quero.sair@teste.com"
        assinante = AssinanteNewsletter.objects.create(email=email_cancelar, is_active=True)
        
        url_cancelamento = self.live_server_url + reverse('usuario:unsubscribe_newsletter', args=[assinante.unsubscribe_token])
        self.selenium.get(url_cancelamento)

        titulo = self.selenium.find_element(By.TAG_NAME, 'h2').text
        self.assertEqual(titulo, "Inscrição Cancelada")
        
        email_na_tela = self.selenium.find_element(By.TAG_NAME, 'strong').text
        self.assertEqual(email_na_tela, email_cancelar)

        assinante.refresh_from_db()
        self.assertFalse(assinante.is_active, "O status do usuário deveria ser False após cancelar.")