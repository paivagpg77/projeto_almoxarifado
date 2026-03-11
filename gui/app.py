import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------------- CONFIGURAÇÃO DE ARQUIVOS ----------------
DATA_DIR = "data"
PRODUTOS_FILE = os.path.join(DATA_DIR, "produtos.json")
CATEGORIAS_FILE = os.path.join(DATA_DIR, "categorias.json")

os.makedirs(DATA_DIR, exist_ok=True)

# ---------------- FUNÇÕES AUXILIARES JSON ----------------
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------------- APLICATIVO PRINCIPAL ----------------
class AlmoxarifadoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Almoxarifado")
        self.geometry("900x600")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # CORREÇÃO PARA CENTRALIZAÇÃO
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, Dashboard, ProdutosPage, CategoriasPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# ---------------- TELA DE LOGIN ----------------
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg="#f0f2f5")

        central_frame = tk.Frame(self, bg="white", bd=2, relief="ridge", width=350, height=250)
        central_frame.place(relx=0.5, rely=0.5, anchor="center")
        central_frame.pack_propagate(False)

        padding_x = 30
        padding_y = 20

        tk.Label(
            central_frame,
            text="Login",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333"
        ).pack(pady=(padding_y, 10))

        tk.Label(
            central_frame,
            text="Usuário",
            font=("Arial", 12),
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=padding_x)

        self.user = tk.Entry(
            central_frame,
            font=("Arial", 12),
            width=30,
            bd=1,
            relief="solid"
        )
        self.user.pack(padx=padding_x, pady=(0, 10))

        tk.Label(
            central_frame,
            text="Senha",
            font=("Arial", 12),
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=padding_x)

        self.password = tk.Entry(
            central_frame,
            font=("Arial", 12),
            width=30,
            bd=1,
            relief="solid",
            show="*"
        )
        self.password.pack(padx=padding_x, pady=(0, 20))

        tk.Button(
            central_frame,
            text="Entrar",
            font=("Arial", 12, "bold"),
            bg="#4a90e2",
            fg="white",
            activebackground="#357ab8",
            activeforeground="white",
            width=20,
            bd=0,
            command=self.login
        ).pack(pady=(0, padding_y))

    def login(self):
        user = self.user.get()
        password = self.password.get()

        if user == "admin" and password == "admin":
            self.controller.show_frame(Dashboard)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

# ---------------- DASHBOARD ----------------
class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Dashboard", font=("Arial", 24)).pack(pady=20)

        tk.Button(
            self,
            text="Gerenciar Produtos",
            width=25,
            command=lambda: controller.show_frame(ProdutosPage)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Gerenciar Categorias",
            width=25,
            command=lambda: controller.show_frame(CategoriasPage)
        ).pack(pady=10)

# ---------------- PÁGINA DE CATEGORIAS ----------------
class CategoriasPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        tk.Label(self, text="Categorias", font=("Arial", 20)).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Nome").grid(row=0, column=0)
        self.nome = tk.Entry(form)
        self.nome.grid(row=0, column=1)

        tk.Label(form, text="Descrição").grid(row=1, column=0)
        self.desc = tk.Entry(form)
        self.desc.grid(row=1, column=1)

        tk.Button(form, text="Cadastrar", command=self.add_categoria).grid(row=2, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("nome", "descricao"), show="headings")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.pack(fill="both", expand=True, pady=10)

        tk.Button(self, text="Voltar", command=lambda: controller.show_frame(Dashboard)).pack(pady=10)

        self.refresh()

    def add_categoria(self):
        nome = self.nome.get()
        desc = self.desc.get()

        if not nome:
            messagebox.showerror("Erro", "Nome obrigatório")
            return

        categorias = load_json(CATEGORIAS_FILE)
        categorias.append({"nome": nome, "descricao": desc})
        save_json(CATEGORIAS_FILE, categorias)

        self.nome.delete(0, tk.END)
        self.desc.delete(0, tk.END)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for c in load_json(CATEGORIAS_FILE):
            self.tree.insert("", "end", values=(c["nome"], c["descricao"]))

# ---------------- PÁGINA DE PRODUTOS ----------------
class ProdutosPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        tk.Label(self, text="Produtos", font=("Arial", 20)).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Nome").grid(row=0, column=0)
        self.nome = tk.Entry(form)
        self.nome.grid(row=0, column=1)

        tk.Label(form, text="Quantidade").grid(row=1, column=0)
        self.qtd = tk.Entry(form)
        self.qtd.grid(row=1, column=1)

        tk.Button(form, text="Cadastrar", command=self.add_produto).grid(row=2, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("nome", "qtd"), show="headings")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("qtd", text="Quantidade")
        self.tree.pack(fill="both", expand=True, pady=10)

        tk.Button(self, text="Voltar", command=lambda: controller.show_frame(Dashboard)).pack(pady=10)

        self.refresh()

    def add_produto(self):
        nome = self.nome.get()
        qtd = self.qtd.get()

        if not nome or not qtd.isdigit():
            messagebox.showerror("Erro", "Dados inválidos")
            return

        produtos = load_json(PRODUTOS_FILE)
        produtos.append({"nome": nome, "quantidade": int(qtd)})
        save_json(PRODUTOS_FILE, produtos)

        self.nome.delete(0, tk.END)
        self.qtd.delete(0, tk.END)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in load_json(PRODUTOS_FILE):
            self.tree.insert("", "end", values=(p["nome"], p["quantidade"]))

# ---------------- EXECUÇÃO ----------------
if __name__ == "__main__":
    app = AlmoxarifadoApp()
    app.mainloop()