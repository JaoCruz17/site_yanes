import json
import requests
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from firebase_admin import credentials, initialize_app, firestore, auth as admin_auth
import firebase_admin

# ---------- Config ----------
with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

API_KEY = CONFIG.get("apiKey")
SERVICE_ACCOUNT_PATH = CONFIG.get("serviceAccountPath", "serviceAccountKey.json")

if not API_KEY:
    raise RuntimeError("Coloque sua apiKey do Firebase em config.json (campo 'apiKey').")
if not SERVICE_ACCOUNT_PATH:
    raise RuntimeError("Coloque o caminho do seu service account em config.json (campo 'serviceAccountPath').")

# Init Firebase Admin
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
if not firebase_admin._apps:
    initialize_app(cred)
db = firestore.client()

# Firebase Auth REST endpoints
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

# ---------- Helper functions for Firebase Auth (REST) ----------
def sign_in_with_email_and_password(email, password):
    """Sign in and return dict with idToken, localId (uid), etc."""
    payload = {"email": email, "password": password, "returnSecureToken": True}
    resp = requests.post(FIREBASE_SIGNIN_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def sign_up_with_email_and_password(email, password):
    """Create user with email/password (client-style) -> returns localId (uid)"""
    payload = {"email": email, "password": password, "returnSecureToken": True}
    resp = requests.post(FIREBASE_SIGNUP_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

# ---------- Tkinter GUI ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Painel Admin - Desktop (Tkinter + Firebase)")
        self.geometry("1000x650")
        self.resizable(True, True)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginFrame, AdminFrame, CadastroProdutoFrame, CadastroUsuarioFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

        # store auth info
        self.id_token = None
        self.local_id = None

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

# ---------------- Login Frame ----------------
class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        title = ttk.Label(self, text="Login Admin", font=("Inter", 20, "bold"))
        title.pack(pady=(10, 20))

        frm = ttk.Frame(self)
        frm.pack(pady=10)

        ttk.Label(frm, text="E-mail:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = ttk.Entry(frm, width=40)
        self.email_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frm, text="Senha:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.pw_entry = ttk.Entry(frm, width=40, show="*")
        self.pw_entry.grid(row=1, column=1, pady=5)

        btn = ttk.Button(self, text="Entrar", command=self.handle_login)
        btn.pack(pady=15)

        note = ttk.Label(self, text="Use um usuário válido do Firebase Auth (será tratado como admin).")
        note.pack(pady=(10,0))

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.pw_entry.get().strip()
        if not email or not password:
            messagebox.showwarning("Preencha", "Informe e-mail e senha.")
            return

        def do_signin():
            try:
                resp = sign_in_with_email_and_password(email, password)
                self.controller.id_token = resp.get("idToken")
                self.controller.local_id = resp.get("localId")
                # opcional: checar se user existe na collection 'usuarios' e se tem permissão de admin
                # aqui, por simplicidade, qualquer usuário autenticado é aceito
                self.controller.show_frame("AdminFrame")
            except requests.HTTPError as e:
                try:
                    data = e.response.json()
                    msg = data.get("error", {}).get("message", str(e))
                except Exception:
                    msg = str(e)
                messagebox.showerror("Erro de Login", f"Não foi possível autenticar: {msg}")

        threading.Thread(target=do_signin, daemon=True).start()

# ---------------- Admin Frame ----------------
class AdminFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        header = ttk.Frame(self)
        header.pack(fill="x")
        ttk.Label(header, text="Painel do Administrador", font=("Inter", 18, "bold")).pack(side="left")
        ttk.Button(header, text="Sair", command=self.logout).pack(side="right")
        ttk.Button(header, text="Gerenciar Usuários", command=lambda: controller.show_frame("CadastroUsuarioFrame")).pack(side="right", padx=8)
        ttk.Button(header, text="Gerenciar Produtos", command=lambda: controller.show_frame("CadastroProdutoFrame")).pack(side="right", padx=8)

        # quick-cards like links
        cards = ttk.Frame(self)
        cards.pack(pady=20, fill="x")
        for text, cmd in [("Cadastrar Usuário", lambda: controller.show_frame("CadastroUsuarioFrame")),
                          ("Cadastrar Produto", lambda: controller.show_frame("CadastroProdutoFrame")),
                          ("Compra & Venda (não implementado)", lambda: messagebox.showinfo("Info","Funcionalidade de compra/venda não implementada nesta versão"))]:
            card = ttk.Button(cards, text=text, command=cmd)
            card.pack(side="left", padx=10, ipadx=12, ipady=12, expand=True, fill="x")

    def logout(self):
        self.controller.id_token = None
        self.controller.local_id = None
        self.controller.show_frame("LoginFrame")

# ---------------- Cadastro Produto Frame ----------------
class CadastroProdutoFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=12)
        self.controller = controller

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0,10))
        ttk.Button(header, text="Voltar", command=lambda: controller.show_frame("AdminFrame")).pack(side="left")
        ttk.Label(header, text="Gerenciamento de Produtos", font=("Inter", 16, "bold")).pack(side="left", padx=10)

        # form
        form = ttk.Frame(self)
        form.pack(fill="x", pady=(0,12))

        self.produto_id = tk.StringVar()
        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_e = ttk.Entry(form, width=30)
        self.nome_e.grid(row=0, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="Código:").grid(row=1, column=0, sticky="w")
        self.codigo_e = ttk.Entry(form, width=30)
        self.codigo_e.grid(row=1, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="Preço:").grid(row=0, column=2, sticky="w")
        self.preco_e = ttk.Entry(form, width=20)
        self.preco_e.grid(row=0, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="Quantidade:").grid(row=1, column=2, sticky="w")
        self.quant_e = ttk.Entry(form, width=20)
        self.quant_e.grid(row=1, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="Descrição:").grid(row=2, column=0, sticky="nw", pady=6)
        self.descricao_t = tk.Text(form, width=70, height=4)
        self.descricao_t.grid(row=2, column=1, columnspan=3, sticky="w", padx=6, pady=4)

        ttk.Button(form, text="Salvar Produto", command=self.salvar_produto).grid(row=3, column=1, columnspan=1, pady=8)

        self.msg = ttk.Label(self, text="", foreground="green")
        self.msg.pack()

        # tabela de produtos
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = ("nome","codigo","preco","quantidade","descricao")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ações
        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=6)
        ttk.Button(actions, text="Editar selecionado", command=self.editar_selecionado).pack(side="left", padx=6)
        ttk.Button(actions, text="Excluir selecionado", command=self.excluir_selecionado).pack(side="left", padx=6)
        ttk.Button(actions, text="Atualizar lista", command=self.carregar_produtos).pack(side="left", padx=6)

        self.carregar_produtos()

    def carregar_produtos(self):
        # limpa
        for i in self.tree.get_children():
            self.tree.delete(i)
        docs = db.collection("produtos").get()
        for d in docs:
            p = d.to_dict()
            self.tree.insert("", "end", iid=d.id, values=(p.get("nome","-"), p.get("codigo","-"), f'R$ {p.get("preco",0):.2f}', p.get("quantidade",0), p.get("descricao","-")))

    def salvar_produto(self):
        nome = self.nome_e.get().strip()
        codigo = self.codigo_e.get().strip()
        try:
            preco = float(self.preco_e.get())
        except:
            preco = 0.0
        try:
            quantidade = int(self.quant_e.get())
        except:
            quantidade = 0
        descricao = self.descricao_t.get("1.0", "end").strip()
        pid = self.produto_id.get()

        if not nome or not codigo:
            messagebox.showwarning("Validação", "Nome e código são obrigatórios.")
            return

        try:
            if pid:
                doc_ref = db.collection("produtos").document(pid)
                doc_ref.update({"nome": nome, "codigo": codigo, "preco": preco, "quantidade": quantidade, "descricao": descricao})
                self.msg.config(text="✅ Produto atualizado com sucesso!")
            else:
                db.collection("produtos").add({"nome": nome, "codigo": codigo, "preco": preco, "quantidade": quantidade, "descricao": descricao})
                self.msg.config(text="✅ Produto cadastrado com sucesso!")
            self.limpar_form()
            self.carregar_produtos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro salvando produto: {e}")

    def limpar_form(self):
        self.produto_id.set("")
        self.nome_e.delete(0, "end")
        self.codigo_e.delete(0, "end")
        self.preco_e.delete(0, "end")
        self.quant_e.delete(0, "end")
        self.descricao_t.delete("1.0","end")

    def editar_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecionar", "Selecione um produto para editar.")
            return
        pid = sel[0]
        doc = db.collection("produtos").document(pid).get()
        if not doc.exists:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
        p = doc.to_dict()
        self.produto_id.set(pid)
        self.nome_e.delete(0,"end"); self.nome_e.insert(0, p.get("nome",""))
        self.codigo_e.delete(0,"end"); self.codigo_e.insert(0, p.get("codigo",""))
        self.preco_e.delete(0,"end"); self.preco_e.insert(0, str(p.get("preco","")))
        self.quant_e.delete(0,"end"); self.quant_e.insert(0, str(p.get("quantidade","")))
        self.descricao_t.delete("1.0","end"); self.descricao_t.insert("1.0", p.get("descricao",""))
        self.msg.config(text="✏️ Editando produto...")

    def excluir_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecionar", "Selecione um produto para excluir.")
            return
        pid = sel[0]
        if not messagebox.askyesno("Confirma", "Deseja excluir o produto selecionado?"):
            return
        try:
            db.collection("produtos").document(pid).delete()
            self.carregar_produtos()
            self.msg.config(text="🗑️ Produto removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

# ---------------- Cadastro Usuario Frame ----------------
class CadastroUsuarioFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=12)
        self.controller = controller

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0,8))
        ttk.Button(header, text="Voltar", command=lambda: controller.show_frame("AdminFrame")).pack(side="left")
        ttk.Label(header, text="Gerenciamento de Usuários", font=("Inter", 16, "bold")).pack(side="left", padx=10)

        # form
        form = ttk.Frame(self)
        form.pack(fill="x", pady=(0,12))

        self.usuario_id = tk.StringVar()
        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_e = ttk.Entry(form, width=30)
        self.nome_e.grid(row=0, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="ID (CPF/Matrícula):").grid(row=1, column=0, sticky="w")
        self.idusuario_e = ttk.Entry(form, width=30)
        self.idusuario_e.grid(row=1, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="E-mail:").grid(row=0, column=2, sticky="w")
        self.email_e = ttk.Entry(form, width=30)
        self.email_e.grid(row=0, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="Telefone:").grid(row=1, column=2, sticky="w")
        self.telefone_e = ttk.Entry(form, width=30)
        self.telefone_e.grid(row=1, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(form, text="Senha (só p/ novo cadastro):").grid(row=2, column=0, sticky="w")
        self.senha_e = ttk.Entry(form, width=30, show="*")
        self.senha_e.grid(row=2, column=1, sticky="w", padx=6, pady=4)

        ttk.Button(form, text="Salvar Usuário", command=self.salvar_usuario).grid(row=3, column=1, pady=8)

        self.msg = ttk.Label(self, text="", foreground="green")
        self.msg.pack()

        # tabela de usuarios
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = ("nome","email","telefone","idusuario")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=6)
        ttk.Button(actions, text="Editar selecionado", command=self.editar_selecionado).pack(side="left", padx=6)
        ttk.Button(actions, text="Excluir selecionado", command=self.excluir_selecionado).pack(side="left", padx=6)
        ttk.Button(actions, text="Atualizar lista", command=self.carregar_usuarios).pack(side="left", padx=6)

        self.carregar_usuarios()

    def carregar_usuarios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        docs = db.collection("usuarios").get()
        for d in docs:
            u = d.to_dict()
            self.tree.insert("", "end", iid=d.id, values=(u.get("nome","-"), u.get("email","-"), u.get("telefone","-"), u.get("idUsuario","-")))

    def salvar_usuario(self):
        nome = self.nome_e.get().strip()
        idUsuario = self.idusuario_e.get().strip()
        email = self.email_e.get().strip()
        telefone = self.telefone_e.get().strip()
        senha = self.senha_e.get().strip()
        uid_doc = self.usuario_id.get()

        if not nome or not idUsuario or not email:
            messagebox.showwarning("Validação", "Nome, ID e E-mail são obrigatórios.")
            return

        try:
            if uid_doc:
                # Atualiza documento Firestore existente (não altera credenciais Auth)
                doc_ref = db.collection("usuarios").document(uid_doc)
                doc_ref.update({"nome": nome, "idUsuario": idUsuario, "email": email, "telefone": telefone})
                self.msg.config(text="✅ Usuário atualizado com sucesso!")
            else:
                # criar no Auth via REST e depois armazenar doc em 'usuarios'
                if not senha:
                    messagebox.showwarning("Senha", "Informe uma senha para novo usuário.")
                    return
                # cria credencial no Firebase Auth via REST
                resp = sign_up_with_email_and_password(email, senha)
                local_id = resp.get("localId")
                db.collection("usuarios").add({"uid": local_id, "nome": nome, "idUsuario": idUsuario, "email": email, "telefone": telefone})
                self.msg.config(text="✅ Usuário cadastrado com sucesso!")
            self.limpar_form()
            self.carregar_usuarios()
        except requests.HTTPError as e:
            try:
                data = e.response.json()
                msg = data.get("error", {}).get("message", str(e))
            except:
                msg = str(e)
            messagebox.showerror("Erro Auth", msg)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_form(self):
        self.usuario_id.set("")
        self.nome_e.delete(0,"end")
        self.idusuario_e.delete(0,"end")
        self.email_e.delete(0,"end")
        self.telefone_e.delete(0,"end")
        self.senha_e.delete(0,"end")

    def editar_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecionar", "Selecione um usuário para editar.")
            return
        doc_id = sel[0]
        doc = db.collection("usuarios").document(doc_id).get()
        if not doc.exists:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return
        u = doc.to_dict()
        self.usuario_id.set(doc_id)
        self.nome_e.delete(0,"end"); self.nome_e.insert(0, u.get("nome",""))
        self.idusuario_e.delete(0,"end"); self.idusuario_e.insert(0, u.get("idUsuario",""))
        self.email_e.delete(0,"end"); self.email_e.insert(0, u.get("email",""))
        self.telefone_e.delete(0,"end"); self.telefone_e.insert(0, u.get("telefone",""))
        self.senha_e.delete(0,"end")
        self.msg.config(text="✏️ Editando usuário...")

    def excluir_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecionar", "Selecione um usuário para excluir.")
            return
        doc_id = sel[0]
        if not messagebox.askyesno("Confirma", "Deseja excluir o usuário selecionado?"):
            return
        try:
            # pega documento e apaga do Auth (se tiver uid) e do Firestore
            doc_snap = db.collection("usuarios").document(doc_id).get()
            if doc_snap.exists:
                u = doc_snap.to_dict()
                uid = u.get("uid")
                if uid:
                    try:
                        admin_auth.delete_user(uid)
                    except Exception as e:
                        # Pode falhar se a conta foi criada via outro mecanismo
                        print("Erro removendo usuário Auth:", e)
                db.collection("usuarios").document(doc_id).delete()
            self.carregar_usuarios()
            self.msg.config(text="🗑️ Usuário removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}")

# ---------- Run ----------
if __name__ == "__main__":
    app = App()
    app.mainloop()
