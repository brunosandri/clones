from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.manager import CloneManager

app = FastAPI(title="Sistema de Clones Cognitivos", version="1.0.0")
manager = CloneManager()

class ConsultaRequest(BaseModel):
    user_id: str
    clone_name: str
    pergunta: str

class CriarCloneRequest(BaseModel):
    nome: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 2000

@app.get("/")
async def root():
    return {
        "message": "Sistema de Clones Cognitivos API",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/clones")
async def listar_clones():
    """Lista todos os clones disponíveis"""
    return {
        "clones": manager.listar_clones(),
        "total": len(manager.clones)
    }

@app.post("/consultar")
async def consultar_clone(consulta: ConsultaRequest):
    """Consulta um clone específico"""
    try:
        resultado = manager.consultar_clone(
            consulta.user_id,
            consulta.clone_name,
            consulta.pergunta
        )
        if "error" in resultado:
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return resultado
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/clones/novo")
async def criar_novo_clone(clone_request: CriarCloneRequest):
    """Cria um novo clone no sistema"""
    try:
        config = {
            "name": clone_request.nome.title(),
            "system_prompt": clone_request.system_prompt,
            "temperature": clone_request.temperature,
            "max_tokens": clone_request.max_tokens
        }
        
        sucesso = manager.criar_novo_clone(clone_request.nome.lower(), config)
        
        if sucesso:
            return {
                "message": f"Clone '{clone_request.nome}' criado com sucesso",
                "clone_id": clone_request.nome.lower()
            }
        else:
            raise HTTPException(status_code=400, detail="Erro ao criar clone")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/usuarios/{user_id}/historico")
async def limpar_historico(user_id: str):
    """Limpa histórico de conversa de um usuário"""
    sucesso = manager.limpar_historico(user_id)
    
    if sucesso:
        return {"message": f"Histórico do usuário {user_id} limpo com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/estatisticas")
async def obter_estatisticas():
    """Retorna estatísticas de uso do sistema"""
    return manager.estatisticas_uso()

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "clones_ativos": len(manager.clones)
    }