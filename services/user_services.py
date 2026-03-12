from utils.verify_email import verify_in_json
from models.users import Usuario
from repositories.usuario_repository import UsuarioRepository 
from utils.hash_generator import _gerar_hash
class ProdutoService():
    @staticmethod
    def cadastrar_usuario(nome: str, email : str, senha: str):
        if verify_in_json(email):
            raise ValueError("Email já cadastrado")
        usuario = Usuario(
            id = None,
            nome = nome,
            email = email,
            senha = senha
        )
        UsuarioRepository.adicionar(usuario)
        return usuario
    @staticmethod
    def autenticar_usuario(email, senha):
        usuario = UsuarioRepository.buscar_por_email()
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        if not usuario.ativo:
            raise ValueError("Usuário inativo")
        
        if not usuario.validar_senha(senha):
            raise ValueError("Senha inválida")
        
        return usuario
    @staticmethod
    def listar_usuarios():
        return UsuarioRepository.listar()
    
    @staticmethod
    def buscar_por_id(id):
        usuario = UsuarioRepository.buscar_por_id(id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        return usuario
    
    @staticmethod
    def buscar_por_email(email):
        usuario = UsuarioRepository.buscar_por_email(email)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        return usuario
    @staticmethod
    def atualizar_usuario(id, nome = None, email = None):
        usuario = UsuarioRepository.buscar_por_id(id)
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        UsuarioRepository.atualizar(usuario)
        return usuario
    @staticmethod
    def alterar_senha(email, nova_senha):
        usuario = UsuarioRepository.buscar_por_email(email)
        usuario.senha = _gerar_hash(nova_senha)
        UsuarioRepository.atualizar(usuario)
    @staticmethod
    def ativar_usuario(id):
        usuario = UsuarioRepository.buscar_por_id(id)
        if usuario.ativo:
            raise Exception("Usuário ativo")
        usuario.ativar_user()
        UsuarioRepository.atualizar(usuario)
    @staticmethod
    def desativar_user(id):
        usuario = UsuarioRepository.buscar_por_id(id)
        if not usuario.ativo:
            raise Exception("Usuário inativo")
        usuario.desativar_user()
        UsuarioRepository.atualizar(usuario)
    @staticmethod
    def verificar_email_existente(email: str):
        usuarios = UsuarioRepository.listar()
        for u in usuarios:
            if u.email == email.lower():
                return True
        return False

    
        
    
        
            
        