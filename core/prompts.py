def criar_prompt_analise_fonte(titulo: str, conteudo: str) -> str:
    """
    Cria prompt para análise estruturada de fontes
    """
    return f"""
Analise o seguinte material de {titulo} e extraia padrões cognitivos usando o framework EXTRACT:

{conteudo}

## EXTRACT Framework:
**E**xperiências Formativas: Eventos que moldaram visão de mundo
**X**adrez Mental: Padrões de tomada de decisão e estratégia  
**T**erminologia Própria: Vocabulário específico e conceitos recorrentes
**R**aciocínio Típico: Estruturas de argumentação e lógica
**A**xiomas Pessoais: Princípios e verdades fundamentais
**C**ontextos de Especialidade: Áreas de maior proficiência
**T**écnicas e Métodos: Abordagens práticas características

Forneça análise estruturada em formato JSON.
"""