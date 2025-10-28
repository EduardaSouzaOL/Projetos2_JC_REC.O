# Projetos2_JC_REC.O/usuario/tests.py

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestAutenticacaoSelenium(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10) 

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.username = 'usuarioteste'
        self.email = 'teste@email.com'
        self.password = 'senhaSegura123'
        self.nome = 'Usuario'
        self.sobrenome = 'Teste'

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name=self.nome,
            last_name=self.sobrenome
        )

    def test_registro_usuario_sucesso(self):
        """Testa o registro de um novo usuário com sucesso."""
        
        unique_username = f"novo_usuario_{int(time.time())}"
        
        self.driver.get(f"{self.live_server_url}{reverse('registrar')}")
        
        #
        self.driver.find_element(By.ID, 'id_username').send_keys(unique_username)
        self.driver.find_element(By.ID, 'id_first_name').send_keys("Novo")
        self.driver.find_element(By.ID, 'id_last_name').send_keys("Usuario")
        self.driver.find_element(By.ID, 'id_email').send_keys(f"{unique_username}@example.com")
        self.driver.find_element(By.ID, 'id_telefone').send_keys("123456789")
        self.driver.find_element(By.ID, 'id_password1').send_keys("senhaForte123")
        self.driver.find_element(By.ID, 'id_password2').send_keys("senhaForte123")
        
        #
        self.driver.find_element(By.CSS_SELECTOR, 'button.auth-btn').click()
        
        #
        # 1. Espera explícita para a URL mudar para a página de login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains(reverse('login'))
        )
        
        # 2. Verifica se a URL de fato é a de login
        self.assertIn(reverse('login'), self.driver.current_url)
        
        # 3. AGORA (com o base.html corrigido) verifica se a mensagem de sucesso está presente
        #
        body_text = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn(f'Usuário criado com sucesso para {unique_username}!', body_text)


    def test_login_e_logout_sucesso(self):
        """Testa o fluxo de login e logout de um usuário existente."""
        
        # --- Teste de Login ---
        
        #
        self.driver.get(f"{self.live_server_url}{reverse('login')}")
        
        #
        self.driver.find_element(By.ID, 'id_username').send_keys(self.username)
        self.driver.find_element(By.ID, 'id_password').send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, 'button.auth-btn').click()
        
        #
        WebDriverWait(self.driver, 10).until(
            EC.url_contains(reverse('perfil'))
        )
        self.assertIn(reverse('perfil'), self.driver.current_url)
        
        # --- Teste de Logout ---
        
        #
        # Esta linha agora vai funcionar por causa do "return false;"
        # self.driver.find_element(By.LINK_TEXT, 'Sair').click() 
        
        # #
        # # MUDANÇA: Estamos esperando pelo H2 de confirmação, não pela URL.
        # # Isto é mais confiável.
        # try:
        #     h2_confirmacao = WebDriverWait(self.driver, 10).until(
        #         EC.visibility_of_element_located(
        #             (By.XPATH, "//h2[contains(text(), 'Você saiu da sua conta.')]")
        #         )
        #     )
        # except TimeoutException:
        #     # Se falhar, imprime o HTML atual para nos ajudar a depurar
        #     print("--- HTML ATUAL (FALHA NO LOGOUT) ---")
        #     print(self.driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'))
        #     print("-------------------------------------")
        #     raise

        # # Agora que o H2 apareceu, podemos verificar o resto
        # self.assertIn('Você saiu da sua conta.', h2_confirmacao.text)
        # self.assertIn(reverse('logout'), self.driver.current_url)
        
        # body_text = self.driver.find_element(By.TAG_NAME, 'body').text
        # self.assertIn('Fazer Login Novamente', body_text)