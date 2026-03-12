import streamlit as st
import json
import os

# ---------------- CONFIGURAÇÃO DE ARQUIVOS ----------------
DATA_DIR = "data"
PRODUTOS_FILE = os.path.join(DATA_DIR, "produtos.json")
CATEGORIAS_FILE = os.path.join(DATA_DIR, "categorias.json")
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------- FUNÇÕES ----------------
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------------- LOGIN ----------------
def login_page():
    st.title("Login")
    usuario = st.text_input("Usuário", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")
    
    if st.button("Entrar"):
        usuarios = load_json(USUARIOS_FILE)
        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                st.session_state["logged_in"] = True
                st.session_state["usuario"] = usuario
                st.session_state["page"] = "dashboard"
                st.success(f"Bem-vindo {usuario}!")
                return
        st.error("Usuário ou senha inválidos")
    
    if st.button("Criar conta"):
        st.session_state["page"] = "register"

# ---------------- REGISTRO ----------------
def register_page():
    st.title("Criar Conta")
    nome = st.text_input("Nome", key="reg_nome")
    usuario = st.text_input("Usuário", key="reg_usuario")
    senha = st.text_input("Senha", type="password", key="reg_senha")
    confirma = st.text_input("Confirmar Senha", type="password", key="reg_confirma")
    
    if st.button("Cadastrar"):
        if not nome or not usuario or not senha:
            st.error("Preencha todos os campos")
        elif senha != confirma:
            st.error("Senhas não coincidem")
        else:
            usuarios = load_json(USUARIOS_FILE)
            if any(u["usuario"] == usuario for u in usuarios):
                st.error("Usuário já existe")
            else:
                usuarios.append({"nome": nome, "usuario": usuario, "senha": senha})
                save_json(USUARIOS_FILE, usuarios)
                st.success("Usuário cadastrado!")
    
    if st.button("Voltar para Login"):
        st.session_state["page"] = "login"

# ---------------- DASHBOARD ----------------
def dashboard():
    st.sidebar.title(f"Olá, {st.session_state['usuario']}!")
    menu = ["Produtos", "Categorias", "Logout"]
    choice = st.sidebar.radio("Menu", menu)
    
    if choice == "Produtos":
        produtos_page()
    elif choice == "Categorias":
        categorias_page()
    elif choice == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"
        st.experimental_rerun()

# ---------------- PÁGINAS ----------------
def produtos_page():
    st.header("Produtos")
    produtos = load_json(PRODUTOS_FILE)
    
    with st.expander("Adicionar / Editar Produto"):
        nome = st.text_input("Nome do Produto", key="prod_nome")
        qtd = st.number_input("Quantidade", min_value=0, step=1, key="prod_qtd")
        editar_idx = st.session_state.get("editar_produto_idx", None)
        
        if st.button("Salvar Produto"):
            if not nome:
                st.error("Nome obrigatório")
            else:
                if editar_idx is not None:
                    produtos[editar_idx] = {"nome": nome, "quantidade": qtd}
                    st.session_state["editar_produto_idx"] = None
                else:
                    produtos.append({"nome": nome, "quantidade": qtd})
                save_json(PRODUTOS_FILE, produtos)
                st.success("Produto salvo!")

    if produtos:
        for idx, p in enumerate(produtos):
            col1, col2, col3, col4 = st.columns([3,1,1,1])
            col1.write(p["nome"])
            col2.write(p["quantidade"])
            if col3.button("Editar", key=f"edit_prod_{idx}"):
                st.session_state["prod_nome"] = p["nome"]
                st.session_state["prod_qtd"] = p["quantidade"]
                st.session_state["editar_produto_idx"] = idx
            if col4.button("Excluir", key=f"del_prod_{idx}"):
                produtos.pop(idx)
                save_json(PRODUTOS_FILE, produtos)
                st.success("Produto excluído!")

def categorias_page():
    st.header("Categorias")
    categorias = load_json(CATEGORIAS_FILE)
    
    with st.expander("Adicionar / Editar Categoria"):
        nome = st.text_input("Nome da Categoria", key="cat_nome")
        desc = st.text_input("Descrição", key="cat_desc")
        editar_idx = st.session_state.get("editar_cat_idx", None)
        
        if st.button("Salvar Categoria"):
            if not nome:
                st.error("Nome obrigatório")
            else:
                if editar_idx is not None:
                    categorias[editar_idx] = {"nome": nome, "descricao": desc}
                    st.session_state["editar_cat_idx"] = None
                else:
                    categorias.append({"nome": nome, "descricao": desc})
                save_json(CATEGORIAS_FILE, categorias)
                st.success("Categoria salva!")

    if categorias:
        for idx, c in enumerate(categorias):
            col1, col2, col3, col4 = st.columns([3,3,1,1])
            col1.write(c["nome"])
            col2.write(c["descricao"])
            if col3.button("Editar", key=f"edit_cat_{idx}"):
                st.session_state["cat_nome"] = c["nome"]
                st.session_state["cat_desc"] = c["descricao"]
                st.session_state["editar_cat_idx"] = idx
            if col4.button("Excluir", key=f"del_cat_{idx}"):
                categorias.pop(idx)
                save_json(CATEGORIAS_FILE, categorias)
                st.success("Categoria excluída!")

# ---------------- INICIAL ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if not st.session_state["logged_in"]:
    if st.session_state["page"] == "login":
        login_page()
    else:
        register_page()
else:
    dashboard()