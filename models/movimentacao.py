from datetime import datetime
from utils import id_generator
from enums import tipo
from produtos import Produto

class Movimentacao:
    def __init__(self,id_produto, id_usuario, quantidade,tipo, data=None, id = None, observacao = ""):
        self.id = id if id else id_generator.gerar_id()
        self.id_produto = id_produto
        self.id_usuario = id_usuario
        self.quantidade = quantidade
        self.data = data if data else datetime.now()
        self.tipo = tipo
        self.observacao = observacao
        
    def to_dict(self):
        """Método para transformar o objeto em JSON para persistência de dados"""
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "id_produto" : self.id_produto,
            "quantidade": self.quantidade,
            "tipo": self.tipo,
            "data": self.data.isoformat(),
            "observacoes": self.observacao
        }
    @classmethod    
    def from_dict(cls, data):
        """Método de classe para transformar JSON em objeto"""
        return cls(
            id = data["id"],
            id_produto = data["id_produto"],
            id_usuario = data["id_usuario"],
            quantidade = data["quantidade"],
            data = datetime.fromisoformatdata(data["data"])
        )

            
    
    
        