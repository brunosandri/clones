from fastapi import FastAPI
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sistema de Clones Cognitivos")

# Configurar cliente Anthropic
try:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
except Exception as e:
    print(f"❌ Erro ao configurar cliente Anthropic: {e}")
    client = None

# Clone do Steve Jobs
STEVE_JOBS_PROMPT = """
<identity>
Você é Steve Jobs em 2010. Pensa, fala e age como Steve Jobs faria.
</identity>

**Filosofia**: Simplicidade, inovação, perfeição
**Valores**: "Stay hungry, stay foolish", pensar diferente
**Estilo**: Frases curtas e impactantes
"""

@app.get("/")
async def home():
    return {
        "message": "🚀 Sistema de Clones Cognitivos Online!",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api_configured": client is not None}

@app.get("/clones")
async def list_clones():
    return {
        "clones_disponiveis": ["steve_jobs", "elon_musk"],
        "total": 2
    }

@app.get("/consultar/{clone_name}")
async def consultar_clone(clone_name: str, pergunta: str):
    if not client:
        return {"error": "API não configurada - verifique ANTHROPIC_API_KEY"}
    
    if clone_name != "steve_jobs":
        return {"error": f"Clone '{clone_name}' não disponível"}
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system=STEVE_JOBS_PROMPT,
            messages=[{"role": "user", "content": pergunta}]
        )
        
        return {
            "clone": clone_name,
            "pergunta": pergunta,
            "resposta": response.content[0].text,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Erro na consulta: {str(e)}"}

# Para desenvolvimento local
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)