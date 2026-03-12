from enums.unidade_medidaEnum import UnidadeMedida
from enums.categoriaRegistry import Categoria
from models.produtos import Produto
from repositories.produto_repository import ProdutoRepository

class ProdutoService:
        @staticmethod
        def cadastrar_produto(nome: str, categoria_id: str, descricao: str, unidade:UnidadeMedida, estoque_minimo: int, categoria: str):
                """Cadastra um novo produto"""
                if not nome or not nome.strip():
                        raise ValueError("Nome do produto é obrigatório")
                if not categoria_id or not categoria_id.strip():
                        raise ValueError("Categoria do produto é obrigatória")
                if not descricao or not descricao.strip():
                        raise ValueError("Descrição do produto é obrigatória")
                if not isinstance(unidade, UnidadeMedida):
                        raise ValueError("Unidade de medida inválida")
                if estoque_minimo < 0:
                        raise ValueError("Estoque mínimo não pode ser negativo")
                
                categoria_obj = Categoria.buscar_por_id(categoria_id)
                if not categoria_obj:
                        raise ValueError("Categoria não encontrada")
                
                return Produto(nome=nome.strip(), categoria_id=categoria_id, descricao=descricao.strip(), unidade=unidade, estoque_minimo=estoque_minimo)
        @staticmethod
        def listar_produtos():
                return ProdutoRepository.listar()
        @staticmethod
        def buscar_por_id(id: str):
                produto = ProdutoRepository.buscar_por_id(id)
                if not produto:
                        raise ValueError("Produto não encontrado")
                return produto
        @staticmethod
        def buscar_por_nome(nome: str):
                produto = ProdutoRepository.buscar_por_nome(nome)
                if not produto:
                        raise ValueError("Produto não encontrado")
                return produto
        @staticmethod
        def atualizar_produto(id_produto, nome=None, descricao=None, estoque_minimo = None):
                produto = ProdutoRepository.buscar_por_id(id_produto)
                if not produto:
                        raise ValueError("Produto não encontrado")
                else: 
                        if nome:
                                produto.nome = nome
                        if descricao:
                                produto.descricao = descricao
                        if estoque_minimo:
                                produto.estoque_minimo = estoque_minimo
                        ProdutoRepository.atualizar(produto)
                        return produto
        @staticmethod
        def ativar_produto(id_produto):
                produto = ProdutoRepository.buscar_por_id(id)
                if not produto:
                        raise ValueError("Produto não encontrado")
                produto.ativar()
                ProdutoRepository.atualizar(produto)
        @staticmethod
        def desativar_produto(id_produto):
                produto = ProdutoRepository.buscar_por_id(id)
                if not produto:
                        raise ValueError("Produto não encontrado")
                produto.desativar()
                ProdutoRepository.atualizar(produto)
        @staticmethod
        def verificar_produto_existente(nome: str, categoria: str):
                produtos = ProdutoRepository.listar()
                for produto in produtos:
                        if produto.nome.lower() == nome.lower() and produto.nome_categoria.lower() == categoria.lower():
                                return True
                return False
        @staticmethod
        def listar_produtos_ativos():
                produtos = ProdutoRepository.listar()
                produtos_ativos = []
                for p in produtos:
                        if p.ativo:
                                produtos_ativos.append(p)
                return produtos_ativos
        @staticmethod
        def listar_produtos_ativos():
                produtos = ProdutoRepository.listar()
                produtos_ativos = []
                for p in produtos:
                        if p.ativo:
                                produtos_ativos.append(p)
                return produtos_ativos
        @staticmethod
        def listar_produtos_inativos():
                produtos = ProdutoRepository.listar()
                produtos_inativos = []
                for p in produtos:
                        if p.ativo:
                                produtos_inativos.append(p)
                return produtos_inativos
        @staticmethod
        def listar_estoque_baixo():
                produtos = ProdutoRepository.listar()
                estoque_baixo = []
                for p in produtos:
                        if p.quantidade_atual <= p.estoque_minimo:
                                estoque_baixo.append(p)
                return estoque_baixo
        @staticmethod
        def listar_sem_estoque():
                produtos = ProdutoRepository.listar()
                sem_estoque = []
                for p in produtos:
                        if p.quantidade_atual == 0:
                                sem_estoque.append(p)
                return sem_estoque
        
                
        
                                
        
                                
        
                        
               
                
                                