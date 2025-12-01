import google.generativeai as genai
import json
import os
from django.conf import settings
from .models import Quiz, Pergunta, Opcao

GENAI_API_KEY = os.getenv("GEMINI_API_KEY") 

if not GENAI_API_KEY:
    print("⚠️  AVISO: GEMINI_API_KEY não encontrada no arquivo .env")

def gerar_quiz_com_gemini(noticia_obj):

    if not GENAI_API_KEY:
        print("ERRO: API Key do Gemini não configurada.")
        return

    print(f"🤖 IA: Lendo a notícia '{noticia_obj.titulo}'...")
    
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Atue como um jornalista educativo. Crie um Quiz de 5 perguntas baseadas no texto abaixo.
    
    TEXTO DA NOTÍCIA:
    "{noticia_obj.conteudo}"

    REGRAS OBRIGATÓRIAS:
    1. Retorne APENAS um JSON válido. Sem markdown (```json), sem explicações extras.
    2. O formato deve ser EXATAMENTE este:
    [
        {{
            "pergunta": "Texto da pergunta aqui?",
            "opcoes": [
                {{"texto": "Opção errada 1", "correta": false}},
                {{"texto": "Opção certa aqui", "correta": true}},
                {{"texto": "Opção errada 2", "correta": false}},
                {{"texto": "Opção errada 3", "correta": false}}
            ]
        }}
    ]
    3. As perguntas devem ser de interpretação de texto baseadas no artigo.
    """

    try:
        response = model.generate_content(prompt)
        
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        
        dados_quiz = json.loads(json_text)

        quiz, created = Quiz.objects.get_or_create(
            noticia=noticia_obj,
            defaults={
                'titulo': f"Quiz: {noticia_obj.titulo}",
                'gerado_por_ia': True,
                'descricao': "Teste seus conhecimentos sobre o artigo que acabou de ler."
            }
        )

        if not created:
            quiz.perguntas.all().delete()

        for i, item in enumerate(dados_quiz, 1):
            nova_pergunta = Pergunta.objects.create(
                quiz=quiz,
                texto=item['pergunta'],
                ordem=i
            )
            
            for opt in item['opcoes']:
                Opcao.objects.create(
                    pergunta=nova_pergunta,
                    texto=opt['texto'],
                    correta=opt['correta']
                )

        print("✅ IA: Quiz criado com sucesso!")

    except Exception as e:
        print(f"❌ ERRO IA: Falha ao gerar quiz: {e}")