import re
from typing import List

def extrair_citacoes(texto: str) -> List[str]:
    """Extrai citações marcadas com > do texto"""
    citacoes = re.findall(r'^>\s*(.+)$', texto, re.MULTILINE)
    return citacoes

def calcular_custo_tokens(texto: str, tipo: str = "output") -> float:
    """Calcula custo estimado em dólares"""
    tokens = len(texto.split()) * 1.3  # Estimativa conservadora
    
    if tipo == "input":
        return tokens * 3.00 / 1_000_000  # $3.00/million input tokens
    else:
        return tokens * 15.00 / 1_000_000  # $15.00/million output tokens

def validar_nome_clone(nome: str) -> bool:
    """Valida se nome do clone é válido"""
    return bool(re.match(r'^[a-z0-9_]+$', nome)) and len(nome) <= 50