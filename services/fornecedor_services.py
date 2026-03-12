from repositories.fornecedor_repository import FornecedorRepository
from models.fornecedores import Fornecedor
class FornecedorService:
    @staticmethod
    def cadastrar_fornecedor(nome, cnpj, telefone, email):
        if FornecedorRepository.buscar_por_cnpj(cnpj):
            raise ValueError("Fornecedor já cadastrado")
        fornecedor = Fornecedor(
            nome = nome,
            cnpj = cnpj,
            telefone = telefone,
            email = email
        )
        FornecedorRepository.adicionar(fornecedor)
        return fornecedor
    @staticmethod
    def listar_fornecedores():
        return FornecedorRepository.listar()
    @staticmethod
    def buscar_por_id(id):
        fornecedor = FornecedorRepository.buscar_por_id(id)
        if not fornecedor:
            raise ValueError("Fornecedor não encontrado")
        return fornecedor
    @staticmethod
    def buscar_por_cnpj(cnpj):
        fornecedor = FornecedorRepository.buscar_por_cnpj(cnpj)
        if not fornecedor:
            raise ValueError("Fornecedor não encontrado")
        return fornecedor
    @staticmethod
    def atualizar_fornecedor(id_fornecedor, nome=None, telefone=None, email=None):

        fornecedor = FornecedorRepository.buscar_por_id(id_fornecedor)

        if nome:
            fornecedor.nome = nome

        if telefone:
            fornecedor.telefone = telefone

        if email:
            fornecedor.set_email(email)

        FornecedorRepository.atualizar(fornecedor)

        return fornecedor

    @staticmethod
    def ativar_fornecedor(id_fornecedor):

        fornecedor = FornecedorRepository.buscar_por_id(id_fornecedor)

        fornecedor.ativar()

        FornecedorRepository.atualizar(fornecedor)
    @staticmethod
    def desativar_fornecedor(id_fornecedor):

        fornecedor = FornecedorRepository.buscar_por_id(id_fornecedor)

        fornecedor.desativar()

        FornecedorRepository.atualizar(fornecedor)


    def verificar_cnpj_existente(self, cnpj):

        fornecedores = FornecedorRepository.listar()

        for fornecedor in fornecedores:

            if fornecedor.cnpj == cnpj:
                return True

        return False
            
            
    