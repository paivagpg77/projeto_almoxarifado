from utils import id_generator

class Categoria:
    def __init__(self, nome, descricao = "", id = None, ativo = True):
        if not nome:
            raise ValueError ("Nome obrigátorio")
        self.nome = nome
        self.descricao = descricao
        self.id = id if id else id_generator.gerar_id()
        self.ativo = ativo
        
    def ativar(self):
        self.ativo = True
        
    def desativar(self):
        self.ativo = False

    def verificar_existencia(self, nome: str) -> bool:
        """Método para verificar se a categoria já está cadastrada, comparando nome."""
        return self.nome == nome  
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "id": self.id,
            "ativo": self.ativo
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data["id"],
            nome = data["nome"],
            descricao = data["descricao"],
            ativo = data["ativo"]
        )
    
        
        