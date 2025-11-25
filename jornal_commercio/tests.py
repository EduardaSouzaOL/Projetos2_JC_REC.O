from django.test import TestCase

# Create your tests here.

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestFeedbackSelenium(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_envio_feedback_sucesso(self):
        """Testa o envio do formulário de feedback via AJAX."""
        
        # Navega para a home page
        self.driver.get(f"{self.live_server_url}{reverse('home')}")
        
        # 1. Abrir o Modal (Clicando no botão real em vez de usar JS)
        botao_abrir_modal = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'open-feedback-modal'))
        )
        botao_abrir_modal.click()

        # 2. Aguarda o modal ficar visível
        # O ID no base.html é 'feedback-modal-overlay'
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'feedback-modal-overlay'))
        )
        
        # 3. Preenche os campos
        # Nota: No seu base.html apenas Email e Mensagem aparecem.
        # Usando seletores CSS pelo 'name' para ser mais robusto caso o ID mude.
        
        # Se o campo nome realmente não existir no template base.html, remova esta linha:
        # self.driver.find_element(By.NAME, 'nome').send_keys('Testador Selenium') 
        
        self.driver.find_element(By.NAME, 'email').send_keys('selenium@teste.com')
        self.driver.find_element(By.NAME, 'mensagem').send_keys('Isso é uma mensagem de teste automatizado.')
        
        # 4. Envia o formulário
        # O botão não tem ID, então buscamos pelo tipo dentro do formulário correto
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, '#modal-feedback-form button[type="submit"]')
        submit_btn.click()
        
        # 5. Espera a mensagem de sucesso
        # O ID no base.html é 'form-message-box'
        success_message_div = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'form-message-box'))
        )
        
        # Verifica o texto
        self.assertIn('Feedback enviado com sucesso', success_message_div.text)
        