import anthropic
import json
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
from config.settings import settings
from utils.cache import CacheManager

class CloneManager:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.cache = CacheManager()
        self.clones = self._carregar_clones()
        self.conversations = {}  # user_id -> lista de mensagens
    
    def _carregar_clones(self) -> Dict:
        """Carrega todos os clones do sistema"""
        from clones import STEVE_JOBS, ELON_MUSK
        
        return {
            "steve_jobs": {
                "name": "Steve Jobs",
                "system_prompt": STEVE_JOBS,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "elon_musk": {
                "name": "Elon Musk", 
                "system_prompt": ELON_MUSK,
                "temperature": 0.6,
                "max_tokens": 2500
            }
        }
    
    def _gerar_cache_key(self, clone_name: str, messages: List) -> str:
        """Gera chave única para cache baseada na conversa"""
        conversation_hash = hashlib.md5(
            json.dumps(messages, sort_keys=True).encode()
        ).hexdigest()
        return f"{clone_name}:{conversation_hash}"
    
    def consultar_clone(self, user_id: str, clone_name: str, pergunta: str) -> Dict:
        """
        Consulta um clone específico e retorna resposta estruturada
        """
        if clone_name not in self.clones:
            return {
                "error": f"Clone '{clone_name}' não encontrado",
                "available_clones": list(self.clones.keys())
            }
        
        # Recuperar ou inicializar histórico
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        historico = self.conversations[user_id]
        
        # Construir mensagens para API
        messages = historico + [{"role": "user", "content": pergunta}]
        
        # Verificar cache
        cache_key = self._gerar_cache_key(clone_name, messages)
        cached_response = self.cache.get(cache_key)
        
        if cached_response:
            resposta = cached_response
            from_cache = True
        else:
            # Chamar API Claude
            clone_config = self.clones[clone_name]
            
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=clone_config["max_tokens"],
                    temperature=clone_config["temperature"],
                    system=clone_config["system_prompt"],
                    messages=messages
                )
                
                resposta = response.content[0].text
                from_cache = False
                
                # Salvar no cache (24 horas)
                self.cache.set(cache_key, resposta, expire=86400)
                
            except Exception as e:
                return {
                    "error": f"Erro na API: {str(e)}",
                    "clone": clone_name,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Atualizar histórico
        nova_mensagem_user = {"role": "user", "content": pergunta}
        nova_mensagem_assistant = {"role": "assistant", "content": resposta}
        
        self.conversations[user_id].extend([nova_mensagem_user, nova_mensagem_assistant])
        
        # Manter histórico limitado (últimas 10 trocas)
        if len(self.conversations[user_id]) > 20:
            self.conversations[user_id] = self.conversations[user_id][-20:]
        
        return {
            "clone": clone_name,
            "clone_name": self.clones[clone_name]["name"],
            "resposta": resposta,
            "from_cache": from_cache,
            "timestamp": datetime.now().isoformat(),
            "tokens_estimados": len(resposta.split()) * 1.3  # Estimativa grosseira
        }
    
    def criar_novo_clone(self, nome: str, config: Dict) -> bool:
        """
        Adiciona novo clone ao sistema
        """
        try:
            self.clones[nome] = config
            return True
        except Exception as e:
            print(f"Erro ao criar clone: {e}")
            return False
    
    def listar_clones(self) -> List[Dict]:
        """Lista todos os clones disponíveis com metadata"""
        return [
            {
                "id": clone_id,
                "name": config["name"],
                "config": {
                    "temperature": config["temperature"],
                    "max_tokens": config["max_tokens"]
                }
            }
            for clone_id, config in self.clones.items()
        ]
    
    def limpar_historico(self, user_id: str) -> bool:
        """Limpa histórico de conversa de um usuário"""
        if user_id in self.conversations:
            del self.conversations[user_id]
            return True
        return False
    
    def estatisticas_uso(self) -> Dict:
        """Retorna estatísticas de uso do sistema"""
        return {
            "total_clones": len(self.clones),
            "usuarios_ativos": len(self.conversations),
            "clones_disponiveis": list(self.clones.keys())
        }