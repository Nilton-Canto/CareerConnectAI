"""
Serviço de integração com modelos LLM (Gemini e OpenAI)
"""
import json
import google.generativeai as genai
from django.conf import settings
from openai import OpenAI


class LLMService:
    """
    Serviço para geração de trilhas personalizadas usando LLM
    Suporta Google Gemini e OpenAI
    """
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa o cliente LLM de acordo com o provider configurado"""
        if self.provider == 'gemini':
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                raise ValueError("GEMINI_API_KEY não configurada. Configure no settings.py ou variável de ambiente.")
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-pro')
        
        elif self.provider == 'openai':
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                raise ValueError("OPENAI_API_KEY não configurada. Configure no settings.py ou variável de ambiente.")
            self.client = OpenAI(api_key=api_key)
        
        else:
            raise ValueError(f"Provider '{self.provider}' não suportado. Use 'gemini' ou 'openai'.")
    
    def gerar_trilha_personalizada(self, area_interesse, objetivos_usuario, experiencia_anterior=None):
        """
        Gera uma trilha personalizada baseada nos inputs do usuário
        
        Args:
            area_interesse: Área de carreira de interesse (ex: "Desenvolvimento Web")
            objetivos_usuario: Objetivos profissionais do usuário
            experiencia_anterior: Experiência anterior (opcional)
        
        Returns:
            dict: Trilha estruturada com título, descrição e etapas
        """
        
        # Template de prompt para o LLM
        prompt = self._criar_prompt_trilha(area_interesse, objetivos_usuario, experiencia_anterior)
        
        try:
            if self.provider == 'gemini':
                response = self.client.generate_content(prompt)
                resposta_texto = response.text
            
            elif self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um especialista em carreiras e planejamento profissional."},
                        {"role": "user", "content": prompt}
                    ]
                )
                resposta_texto = response.choices[0].message.content
            
            # Tenta parsear a resposta como JSON
            # Se não for JSON válido, retorna a resposta como texto
            try:
                trilha = json.loads(resposta_texto)
            except json.JSONDecodeError:
                trilha = self._parsear_resposta_texto(resposta_texto, area_interesse)
            
            return trilha
            
        except Exception as e:
            return {
                'erro': str(e),
                'trilha_adicional': {
                    'titulo': f'Trilha em {area_interesse}',
                    'descricao': 'Trilha gerada automaticamente. Personalize conforme necessário.',
                    'etapas': self._gerar_etapas_padrao(area_interesse)
                }
            }
    
    def _criar_prompt_trilha(self, area, objetivos, experiencia=None):
        """Cria o prompt estruturado para o LLM"""
        
        prompt = f"""Você é um especialista em planejamento de carreira. Crie uma trilha de aprendizado 
personalizada no formato JSON com a seguinte estrutura:

{{
    "titulo": "Título da Trilha",
    "descricao": "Descrição geral da trilha",
    "etapas": [
        {{
            "titulo": "Nome da Etapa",
            "descricao": "Descrição detalhada da etapa",
            "ordem": 1
        }}
    ]
}}

REQUISITOS:
- Área de Interesse: {area}
- Objetivos: {objetivos}
- Experiência anterior: {experiencia or 'Iniciante'}
- Crie entre 5 a 10 etapas progressivas
- Cada etapa deve ser específica e acionável
- Ordene as etapas do básico ao avançado

Retorne APENAS o JSON, sem texto adicional."""
        
        return prompt
    
    def _parsear_resposta_texto(self, texto, area):
        """Parseia uma resposta em texto para estrutura de trilha"""
        # Método auxiliar caso o LLM não retorne JSON válido
        linhas = texto.split('\n')
        etapas = []
        etapa_atual = None
        ordem = 1
        
        for linha in linhas:
            linha = linha.strip()
            if linha and not linha.startswith('#'):
                if linha.startswith('**') or linha.startswith('-'):
                    if etapa_atual:
                        etapas.append(etapa_atual)
                    titulo = linha.replace('**', '').replace('-', '').strip()
                    etapa_atual = {
                        'titulo': titulo,
                        'descricao': '',
                        'ordem': ordem
                    }
                    ordem += 1
                elif etapa_atual and linha:
                    etapa_atual['descricao'] += ' ' + linha
        
        if etapa_atual:
            etapas.append(etapa_atual)
        
        return {
            'titulo': f'Trilha em {area}',
            'descricao': f'Trilha personalizada para {area} com {len(etapas)} etapas',
            'etapas': etapas or self._gerar_etapas_padrao(area)
        }
    
    def _gerar_etapas_padrao(self, area):
        """Gera etapas padrão caso o LLM falhe"""
        return [
            {'titulo': f'Fundamentos de {area}', 'descricao': 'Aprenda os conceitos básicos', 'ordem': 1},
            {'titulo': f'Prática em {area}', 'descricao': 'Coloque em prática os conceitos', 'ordem': 2},
            {'titulo': f'Avançado em {area}', 'descricao': 'Nível avançado e especializações', 'ordem': 3}
        ]

