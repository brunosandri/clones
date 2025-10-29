import pytest
from core.manager import CloneManager

class TestCloneManager:
    def setup_method(self):
        self.manager = CloneManager()
    
    def test_listar_clones(self):
        clones = self.manager.listar_clones()
        assert isinstance(clones, list)
        assert len(clones) > 0
    
    def test_consultar_clone_valido(self):
        resultado = self.manager.consultar_clone(
            "test_user", 
            "steve_jobs",
            "Qual é a importância do design?"
        )
        
        assert "resposta" in resultado
        assert resultado["clone"] == "steve_jobs"
        assert len(resultado["resposta"]) > 0
    
    def test_consultar_clone_invalido(self):
        resultado = self.manager.consultar_clone(
            "test_user",
            "clone_inexistente", 
            "Teste"
        )
        
        assert "error" in resultado
        assert "available_clones" in resultado
    
    def test_limpar_historico(self):
        # Primeiro cria algum histórico
        self.manager.consultar_clone("test_user", "steve_jobs", "Teste")
        
        # Limpa histórico
        sucesso = self.manager.limpar_historico("test_user")
        assert sucesso == True
        
        # Verifica se foi limpo
        assert "test_user" not in self.manager.conversations