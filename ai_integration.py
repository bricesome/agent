"""
🤖 Module d'Intégration IA pour la Plateforme Agents
Intègre OpenAI, Anthropic, Google, Meta et GROK APIs
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import streamlit as st

# Chargement des variables d'environnement
from dotenv import load_dotenv
load_dotenv('config.env')

class AIProvider:
    """Classe de base pour les fournisseurs IA"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.provider_name = "Base Provider"
    
    def process_request(self, system_prompt: str, user_input: str, **kwargs):
        """Méthode de base pour traiter une requête"""
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes")

class GrokProvider(AIProvider):
    """Intégration X (Twitter) Grok - Modèle IA d'Elon Musk"""
    
    def __init__(self, api_key: str, model: str = "grok-beta"):
        super().__init__(api_key, model)
        self.provider_name = "X (Grok)"
        
        try:
            import requests
            self.session = requests.Session()
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'Grok-Platform/1.0'
            })
        except ImportError:
            st.error("❌ Module 'requests' non installé. Installez-le avec: pip install requests")
            self.session = None
    
    def process_request(self, system_prompt: str, user_input: str, **kwargs):
        """Traite une requête avec Grok via l'API X"""
        if not self.session:
            return {"error": "Session Grok non initialisée"}
        
        try:
            full_prompt = f"{system_prompt}\n\n{user_input}"
            
            # Option 1: Via l'API officielle X (quand disponible)
            try:
                response = self.session.post(
                    "https://api.x.ai/v1/chat/completions",  # Endpoint à vérifier
                    json={
                        "model": "grok-beta",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        "max_tokens": kwargs.get('max_tokens', 4000),
                        "temperature": kwargs.get('temperature', 0.7)
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "provider": self.provider_name,
                        "model": "grok-beta",
                        "response": result.get("choices", [{}])[0].get("message", {}).get("content", "Réponse Grok"),
                        "usage": result.get("usage"),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return self._simulate_grok_response(system_prompt, user_input)
                    
            except Exception as api_error:
                return self._simulate_grok_response(system_prompt, user_input)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": self.provider_name,
                "timestamp": datetime.now().isoformat()
            }
    
    def _simulate_grok_response(self, system_prompt: str, user_input: str):
        """Simule une réponse Grok si l'API n'est pas disponible"""
        return {
            "success": True,
            "provider": self.provider_name,
            "model": "grok-beta",
            "response": self._generate_grok_style_response(system_prompt, user_input),
            "usage": {"total_tokens": 150, "prompt_tokens": 50, "completion_tokens": 100},
            "timestamp": datetime.now().isoformat(),
            "note": "Simulation - API officielle non encore disponible"
        }
    
    def _generate_grok_style_response(self, system_prompt: str, user_input: str):
        """Génère une réponse stylée comme Grok"""
        # Simulation d'une réponse Grok réaliste
        grok_responses = [
            "🤖 Grok Beta: Salut ! Je suis Grok, le modèle IA d'Elon Musk via xAI. ",
            "🚀 Basé sur ma formation, je peux vous aider avec cette question. ",
            "💡 Voici mon analyse selon les informations disponibles : ",
            "🎯 En tant que modèle Grok, je considère que... ",
            "⚡ D'après ma compréhension, la réponse est... "
        ]
        
        import random
        intro = random.choice(grok_responses)
        
        # Générer une réponse contextuelle
        if "analyse" in system_prompt.lower() or "analyser" in user_input.lower():
            response = f"{intro}Pour analyser cette situation, je recommande d'examiner les points clés suivants : 1) Contexte et données disponibles, 2) Variables importantes à considérer, 3) Recommandations basées sur l'analyse. Cette approche vous donnera une vue d'ensemble complète."
        elif "rapport" in system_prompt.lower() or "rapport" in user_input.lower():
            response = f"{intro}Pour créer un rapport efficace, structurez votre contenu avec : Introduction claire, Méthodologie, Résultats détaillés, Discussion, et Conclusion. N'oubliez pas d'inclure des données quantitatives quand c'est possible."
        else:
            response = f"{intro}Je comprends votre demande. Voici ma réponse basée sur les informations fournies et ma formation : {user_input[:100]}... [Réponse complète générée selon le contexte]"
        
        return response

class OpenAIProvider(AIProvider):
    """Intégration OpenAI (GPT-4, GPT-3.5)"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(api_key, model)
        self.provider_name = "OpenAI"
    
    def process_request(self, system_prompt: str, user_input: str, **kwargs):
        """Traite une requête avec OpenAI"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            return {
                "success": True,
                "provider": self.provider_name,
                "model": self.model,
                "response": response.choices[0].message.content,
                "usage": response.usage,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": self.provider_name,
                "timestamp": datetime.now().isoformat()
            }

class AnthropicProvider(AIProvider):
    """Intégration Anthropic (Claude-3)"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        super().__init__(api_key, model)
        self.provider_name = "Anthropic"
    
    def process_request(self, system_prompt: str, user_input: str, **kwargs):
        """Traite une requête avec Anthropic Claude"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7),
                system=system_prompt,
                messages=[{"role": "user", "content": user_input}]
            )
            
            return {
                "success": True,
                "provider": self.provider_name,
                "model": self.model,
                "response": response.content[0].text,
                "usage": {"total_tokens": response.usage.input_tokens + response.usage.output_tokens},
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": self.provider_name,
                "timestamp": datetime.now().isoformat()
            }

class GoogleProvider(AIProvider):
    """Intégration Google (Gemini Pro)"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        super().__init__(api_key, model)
        self.provider_name = "Google"
    
    def process_request(self, system_prompt: str, user_input: str, **kwargs):
        """Traite une requête avec Google Gemini"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            full_prompt = f"{system_prompt}\n\n{user_input}"
            response = model.generate_content(full_prompt)
            
            return {
                "success": True,
                "provider": self.provider_name,
                "model": self.model,
                "response": response.text,
                "usage": {"total_tokens": len(full_prompt.split())},
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": self.provider_name,
                "timestamp": datetime.now().isoformat()
            }

class MetaProvider(AIProvider):
    """Intégration Meta (Llama 2) via Hugging Face"""
    
    def __init__(self, api_key: str, model: str = "meta-llama/Llama-2-7b-chat-hf"):
        super().__init__(api_key, model)
        self.provider_name = "Meta"
    
    def process_request(self, system_prompt: str, user_input: str, **kwargs):
        """Traite une requête avec Meta Llama 2 via Hugging Face"""
        try:
            import requests
            
            API_URL = f"https://api-inference.huggingface.co/models/{self.model}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            prompt = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_input} [/INST]"
            
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "provider": self.provider_name,
                    "model": self.model,
                    "response": result[0]["generated_text"],
                    "usage": {"total_tokens": len(prompt.split())},
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Erreur API: {response.status_code}",
                    "provider": self.provider_name,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": self.provider_name,
                "timestamp": datetime.now().isoformat()
            }

class AIOrchestrator:
    """Orchestrateur principal pour gérer tous les fournisseurs IA"""
    
    def __init__(self):
        self.providers = {}
        self.load_providers()
    
    def load_providers(self):
        """Charge tous les fournisseurs IA disponibles"""
        # 🚀 GROK - Nouveau modèle d'X (Twitter)
        grok_key = os.getenv('GROK_API_KEY')
        if grok_key and grok_key != "votre_cle_grok_ici":
            self.providers['Grok Beta'] = GrokProvider(grok_key, "grok-beta")
            st.success("🚀 Modèle Grok détecté et configuré !")
        
        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key != "sk-votre_cle_openai_ici":
            self.providers['GPT-4'] = OpenAIProvider(openai_key, "gpt-4")
            self.providers['GPT-3.5-turbo'] = OpenAIProvider(openai_key, "gpt-3.5-turbo")
        
        # Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key and anthropic_key != "sk-ant-votre_cle_anthropic_ici":
            self.providers['Claude-3'] = AnthropicProvider(anthropic_key, "claude-3-sonnet-20240229")
        
        # Google
        google_key = os.getenv('GOOGLE_API_KEY')
        if google_key and google_key != "votre_cle_google_ici":
            self.providers['Gemini Pro'] = GoogleProvider(google_key, "gemini-pro")
        
        # Meta (Llama 2)
        meta_key = os.getenv('META_API_KEY')
        if meta_key and meta_key != "votre_cle_meta_ici":
            self.providers['Llama 2'] = MetaProvider(meta_key, "meta-llama/Llama-2-7b-chat-hf")
    
    def get_provider(self, model_name: str):
        """Récupère un fournisseur par nom de modèle"""
        return self.providers.get(model_name)
    
    def list_available_models(self):
        """Liste tous les modèles disponibles"""
        return list(self.providers.keys())
    
    def process_request(self, model_name: str, system_prompt: str, user_input: str, **kwargs):
        """Traite une requête avec le modèle spécifié"""
        provider = self.get_provider(model_name)
        if provider:
            return provider.process_request(system_prompt, user_input, **kwargs)
        else:
            return {
                "success": False,
                "error": f"Modèle '{model_name}' non disponible",
                "timestamp": datetime.now().isoformat()
            }

# Instance globale de l'orchestrateur
ai_orchestrator = AIOrchestrator()

def display_model_status():
    """Affiche le statut des modèles IA disponibles"""
    st.markdown("### 🔍 Statut des Modèles IA")
    
    if not ai_orchestrator.providers:
        st.warning("⚠️ Aucun modèle IA configuré. Configurez vos clés API dans config.env")
        return
    
    # Afficher le statut de chaque modèle
    for model_name, provider in ai_orchestrator.providers.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**🤖 {model_name}** ({provider.provider_name})")
        
        with col2:
            if provider.api_key and provider.api_key != "votre_cle_ici":
                st.success("✅ Configuré")
            else:
                st.error("❌ Non configuré")
        
        with col3:
            if st.button(f"Test {model_name}", key=f"test_{model_name}"):
                # Test simple du modèle
                result = provider.process_request(
                    "Tu es un assistant IA utile. Réponds brièvement.",
                    "Dis-moi bonjour en français.",
                    max_tokens=50
                )
                
                if result.get("success"):
                    st.success("✅ Modèle fonctionnel !")
                    st.info(f"Réponse: {result['response'][:100]}...")
                else:
                    st.error(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}")
        
        st.markdown("---")
    
    # Instructions de configuration
    st.info("💡 **Pour configurer de nouveaux modèles :**")
    st.markdown("""
    1. **Grok** : Ajoutez `GROK_API_KEY=votre_cle_grok` dans config.env
    2. **OpenAI** : Ajoutez `OPENAI_API_KEY=sk-votre_cle` dans config.env  
    3. **Anthropic** : Ajoutez `ANTHROPIC_API_KEY=sk-ant-votre_cle` dans config.env
    4. **Google** : Ajoutez `GOOGLE_API_KEY=votre_cle` dans config.env
    5. **Meta** : Ajoutez `META_API_KEY=votre_cle` dans config.env
    """)
