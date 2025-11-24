import json
import google.generativeai as genai
from django.conf import settings
from openai import OpenAI

class LLMService:
    """
    Serviço para geração de trilhas personalizadas usando LLM.
    Suporta Google Gemini e OpenAI.
    """

    # --- TAREFA #20: TEMPLATE DE PROMPT (Engenharia de Prompt) ---
    # Definimos a "personalidade" e as regras estritas para a IA aqui no topo.
    PROMPT_TEMPLATE = """
    Atue como um Mentor de Carreira Sênior e Especialista em Educação Tecnológica.
    
    SEU OBJETIVO:
    Criar uma trilha de aprendizado personalizada, prática e detalhada baseada no perfil do usuário.
    
    PERFIL DO USUÁRIO:
    - Área de Interesse: {area}
    - Objetivos Profissionais: {objetivos}
    - Nível de Experiência Atual: {experiencia}
    
    FORMATO DE SAÍDA OBRIGATÓRIO (JSON):
    Você deve retornar APENAS um objeto JSON válido. Não inclua markdown (```json), não inclua explicações antes ou depois.
    O JSON deve seguir estritamente esta estrutura:
    {{
        "titulo": "Um título atrativo para a trilha",
        "descricao": "Um resumo motivador do que o usuário vai aprender",
        "etapas": [
            {{
                "titulo": "Título da Etapa (Ex: Fundamentos, Ferramentas, Projetos)",
                "descricao": "O que estudar especificamente nesta etapa e por que.",
                "ordem": 1
            }}
        ]
    }}
    
    REGRAS DE CONTEÚDO:
    1. Crie entre 5 a 7 etapas lógicas e progressivas.
    2. O idioma deve ser Português do Brasil (PT-BR).
    3. Seja específico: cite tecnologias reais e modernas.
    4. Ordene do básico ao avançado.
    """
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa o cliente LLM de acordo com o provider configurado"""
        if self.provider == 'gemini':
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                raise ValueError("GEMINI_API_KEY não configurada.")
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-pro')
        
        elif self.provider == 'openai':
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                raise ValueError("OPENAI_API_KEY não configurada.")
            self.client = OpenAI(api_key=api_key)
        
        else:
            raise ValueError(f"Provider '{self.provider}' não suportado.")
    
    def gerar_trilha_personalizada(self, area_interesse, objetivos_usuario, experiencia_anterior=None):
        """Gera uma trilha personalizada formatando o template com os dados do usuário"""
        
        # Preenche o template com os dados reais recebidos da API
        prompt = self.PROMPT_TEMPLATE.format(
            area=area_interesse,
            objetivos=objetivos_usuario,
            experiencia=experiencia_anterior or 'Iniciante'
        )
        
        try:
            if self.provider == 'gemini':
                response = self.client.generate_content(prompt)
                resposta_texto = response.text
            
            elif self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um assistente útil que gera saídas apenas em JSON."},
                        {"role": "user", "content": prompt}
                    ]
                )
                resposta_texto = response.choices[0].message.content
            
            # Limpeza e Parse do JSON
            # Remove possíveis blocos de código Markdown que as IAs gostam de colocar
            resposta_limpa = resposta_texto.replace('```json', '').replace('```', '').strip()
            
            trilha = json.loads(resposta_limpa)
            return trilha
            
        except Exception as e:
            # Fallback robusto em caso de falha da IA
            print(f"Erro no LLM: {e}")
            return {
                'erro': str(e),
                'trilha_adicional': {
                    'titulo': f'Trilha Básica em {area_interesse}',
                    'descricao': 'Não foi possível gerar a trilha personalizada no momento. Aqui está uma sugestão padrão.',
                    'etapas': [
                        {'titulo': 'Fundamentos', 'descricao': 'Conceitos base.', 'ordem': 1},
                        {'titulo': 'Prática', 'descricao': 'Exercícios práticos.', 'ordem': 2}
                    ]
                }
            }