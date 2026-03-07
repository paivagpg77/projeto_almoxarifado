class Produto: 
    def __init__(self, id, nome, descricao, unidade, estoque_minimo, id_categoria, quantidade_atual = 0, ativo=True):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.unidade = unidade
        self.estoque_minimo = estoque_minimo
        self.id_categoria = id_categoria
        self.ativo = ativo
        self.quantidade_atual = quantidade_atual
        