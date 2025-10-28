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
        
        # --- ETAPA CRÍTICA: Abrir o Modal ---
        # Você precisa de um elemento (botão/link) na sua página para abrir o modal.
        # Substitua 'id-do-seu-botao-trigger' pelo ID ou seletor real.
        
        # Exemplo (descomente e ajuste quando tiver o botão):
        # try:
        #     feedback_trigger = self.driver.find_element(By.ID, 'id-do-seu-botao-trigger')
        #     feedback_trigger.click()
        # except Exception as e:
        #     print("AVISO: Não foi possível encontrar o gatilho do modal de feedback. "
        #           "O teste pode falhar se o modal não estiver visível.", e)
        
        # Para o teste passar sem um gatilho, você pode forçar a abertura do modal via JS
        # (Não é o ideal, mas funciona se o gatilho não existir)
        self.driver.execute_script("document.getElementById('feedback-modal').style.display = 'block';")

        # Aguarda o modal (e o formulário dentro dele) ficar visível
        #
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'feedback-form'))
        )
        
        # Preenche os campos do formulário de feedback
        # Os IDs vêm dos widgets definidos em FeedbackForm
        self.driver.find_element(By.ID, 'id_feedback_nome').send_keys('Testador Selenium')
        self.driver.find_element(By.ID, 'id_feedback_email').send_keys('selenium@teste.com')
        self.driver.find_element(By.ID, 'id_feedback_mensagem').send_keys('Isso é uma mensagem de teste automatizado.')
        
        # Envia o formulário
        #
        self.driver.find_element(By.ID, 'feedback-submit-btn').click()
        
        # O formulário é enviado via AJAX
        # Precisamos esperar a mensagem de sucesso aparecer
        #
        success_message_div = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'feedback-success-message'))
        )
        
        # Verifica a mensagem de sucesso
        self.assertIn('Feedback enviado com sucesso! Obrigado.', success_message_div.text)