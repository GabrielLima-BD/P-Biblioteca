import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import requests
import json

# Configurações globais de tema e aparência
ctk.set_appearance_mode("light")  # Força tema claro pra consistência
ctk.set_default_color_theme("blue")

after_ids = []  # Lista para armazenar os IDs de after
# Lista dos gêneros disponíveis
Generos = [
    (1, 'Aventura'),
    (2, 'Romance'),
    (3, 'Ficção Científica'),
    (4, 'Fantasia'),
    (5, 'Terror'),
    (6, 'Suspense'),
    (7, 'Mistério'),
    (8, 'Biografia'),
    (9, 'História'),
    (10, 'Autoajuda'),
    (11, 'Drama'),
    (12, 'Poesia'),
    (13, 'Humor'),
    (14, 'Infantil'),
    (15, 'Didático')
]

class CustomCTk(ctk.CTk):  # Classe base para janelas que sobrescreve destroy
    def destroy(self):
        global after_ids
        for id in after_ids:
            try:
                self.after_cancel(id)
            except:
                pass
        after_ids.clear()
        super().destroy()

# ____________________________________Janelas Python_________________________________________ #

def tela1():  # Tela Inicial para o Funcionario
    tela1 = CustomCTk(fg_color="#3C4C34")
    tela1.title("Inicio")
    tela1.geometry("250x420")

    textprincipal = ctk.CTkLabel(tela1, text="Seja Bem Vindo!")
    textprincipal.place(y=45, x=80)

    textopcoes = ctk.CTkLabel(tela1, text="Escolha uma opção:")
    textopcoes.place(y=115, x=70)

    btConsulta = ctk.CTkButton(tela1, text="Consulta", fg_color="black",
                               hover_color="#9CAD84", command=lambda: pri_consulta(tela1))
    btConsulta.place(y=150, x=60)

    btCadastro = ctk.CTkButton(tela1, text="Cadastro", fg_color="black",
                               hover_color="#B36A5E", command=lambda: pri_cadastro(tela1))
    btCadastro.place(y=185, x=60)

    btReservas = ctk.CTkButton(tela1, text="Reservas", fg_color="black",
                               hover_color="#5F8D96", command=lambda: pri_reserva(tela1))
    btReservas.place(y=220, x=60)

    btExclusao = ctk.CTkButton(tela1, text="Exclusão", fg_color="black",
                               hover_color="#7C5E67", command=lambda: pri_exclusao(tela1))
    btExclusao.place(y=255, x=60)

    btSair = ctk.CTkButton(tela1, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=tela1.destroy)
    btSair.place(y=385, x=105)

    tela1.mainloop()

def voltar_tela1(tela_atual):  # Função para voltar a tela inicial
    tela_atual.destroy()
    tela1()

# _____________________________________CONSULTAS_____________________________________________ #

def pri_consulta(tela1):  # Tela Pri das Consultas
    tela1.destroy()

    telaConsulta = CustomCTk(fg_color="#6D7B74")
    telaConsulta.title("Consulta")
    telaConsulta.geometry("250x420")

    opcao = ctk.CTkLabel(
        telaConsulta, text="Escolha uma opção:", text_color="black")
    opcao.place(y=110, x=70)

    btConsultaNomeUsuario = ctk.CTkButton(telaConsulta, text="Nome Usuário", fg_color="black",
                                         hover_color="#5F8D96", command=lambda: sec_consulta_nomeusuario(telaConsulta))
    btConsultaNomeUsuario.place(y=140, x=60)

    btConsultaEstado = ctk.CTkButton(telaConsulta, text="Por Estado", fg_color="black",
                                     hover_color="#9CAD84", command=lambda: sec_consulta_estado(telaConsulta))
    btConsultaEstado.place(y=170, x=60)

    btConsultaNomeLivro = ctk.CTkButton(
        telaConsulta, text="Nome Livro", fg_color="black", hover_color="#B36A5E", command=lambda: sec_consulta_nomelivro(telaConsulta))
    btConsultaNomeLivro.place(y=200, x=60)

    btConsultaNomeAutor = ctk.CTkButton(
        telaConsulta, text="Nome Autor", fg_color="black", hover_color="#7C5E67", command=lambda: sec_consulta_nomeAutor(telaConsulta))
    btConsultaNomeAutor.place(y=230, x=60)

    btConsultaGenero = ctk.CTkButton(
        telaConsulta, text="Por Gênero", fg_color="black", hover_color="#ADA584", command=lambda: sec_consulta_genero(telaConsulta))
    btConsultaGenero.place(y=260, x=60)

    btVoltar = ctk.CTkButton(telaConsulta, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", command=lambda: voltar_tela1(telaConsulta), font=("Arial", 14, "underline"))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsulta, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaConsulta.destroy)
    btSair.place(y=380, x=105)

    telaConsulta.mainloop()

def sec_consulta_nomeusuario(telaConsulta):  # Tela Sec de Consulta aos Usuários pelo nome
    telaConsulta.destroy()

    telaConsultaUsuario = CustomCTk(fg_color="#6D7B74")
    telaConsultaUsuario.title("Consulta")
    telaConsultaUsuario.geometry("330x250")

    def procura_usuario():
        nome_digitado = entry_nomeusuario.get().strip()
        if not nome_digitado:
            messagebox.showwarning("Atenção", "Digite um nome válido.")
            return

        try:
            response = requests.get(
                "http://localhost:3000/cliente", params={"Nome": nome_digitado})
            response.raise_for_status()
            dados = response.json()
            clientes = dados.get("data", [])

            if clientes:
                ter_resultadonome(clientes, telaConsultaUsuario)
            else:
                messagebox.showinfo("Resultado", "Nenhum cliente encontrado.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {e}")

    NomeUsuario = ctk.CTkLabel(
        telaConsultaUsuario, text="Digite o Nome do Usuário que deseja Buscar")
    NomeUsuario.place(y=65, x=40)
    entry_nomeusuario = ctk.CTkEntry(
        telaConsultaUsuario, width=250, height=30, justify="center")
    entry_nomeusuario.place(y=95, x=40)

    btProcurar = ctk.CTkButton(
        telaConsultaUsuario, text="Procurar", command=procura_usuario)
    btProcurar.place(y=145, x=95)

    btVoltar = ctk.CTkButton(telaConsultaUsuario, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", font=("Arial", 14, "underline"), command=lambda: voltar_tela1(telaConsultaUsuario))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsultaUsuario, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaConsultaUsuario.destroy)
    btSair.place(y=220, x=95)

    telaConsultaUsuario.mainloop()

def ter_resultadonome(dados, telaConsultaUsuario):  # Tela Ter onde mostra os dados do Usuário Puxado
    telaResultadoNome = ctk.CTkToplevel(fg_color="#000000")
    telaResultadoNome.title("Resultado da Busca")
    telaResultadoNome.geometry("1200x600")
    telaResultadoNome.configure(bg="black")
    telaResultadoNome.resizable(False, False)

    def voltar():
        telaResultadoNome.destroy()
        telaConsultaUsuario()

    btVoltar = ctk.CTkButton(telaResultadoNome, text="Voltar ao Menu Anterior", text_color="white", fg_color="#000000",
                             hover_color="#575757", font=("Arial", 14, "underline"), command=voltar)
    btVoltar.place(y=10, x=10)

    frame = tk.Frame(telaResultadoNome, bg="black", width=1100, height=500)
    frame.place(relx=0.5, rely=0.55, anchor="center")
    frame.grid_propagate(False)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    font=("Arial", 12),
                    background="black",
                    foreground="white",
                    fieldbackground="black",
                    rowheight=30,
                    borderwidth=1)

    style.configure("Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#78368E",
                    foreground="white",
                    relief="flat")

    style.map("Treeview",
              background=[('selected', '#347083')],
              foreground=[('selected', 'white')])

    tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
    tree_scroll_y.grid(row=0, column=1, sticky="ns")

    tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
    tree_scroll_x.grid(row=1, column=0, sticky="ew")

    colunas = (
        "Nome", "Sobrenome", "CPF", "DataNascimento", "DataAfiliacao",
        "QntdLivrosReservados", "QntdPendencias", "CEP",
        "Numero", "Bairro", "Cidade", "Estado", "Complemento"
    )

    tree = ttk.Treeview(
        frame,
        columns=colunas,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set
    )
    tree.grid(row=0, column=0, sticky="nsew")

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150, stretch=True)

    tree.tag_configure('oddrow', background="#1a1a1a")
    tree.tag_configure('evenrow', background="#2a2a2a")

    for i, cliente in enumerate(dados):
        endereco = cliente.get("endereco", {})
        valores = (
            cliente.get("Nome", "Não informado"),
            cliente.get("Sobrenome", "Não informado"),
            cliente.get("CPF", "Não informado"),
            cliente.get("DataNascimento", "Não informado"),
            cliente.get("DataAfiliacao", "Não informado"),
            cliente.get("QuantidadeLivrosReservados", 0),
            cliente.get("QuantidadePendencias", 0),
            endereco.get("CEP", "Não informado"),
            endereco.get("Numero", "Não informado"),
            endereco.get("Bairro", "Não informado"),
            endereco.get("Cidade", "Não informado"),
            endereco.get("Estado", "Não informado"),
            endereco.get("Complemento", "Não informado")
        )
        tree.insert("", "end", values=valores, tags=(
            'oddrow' if i % 2 == 0 else 'evenrow',))

    telaResultadoNome.tk.call('tk', 'scaling', 1.0)

def sec_consulta_estado(telaConsulta):  # Tela Sec de Consulta aos Usuários pelo estado
    telaConsulta.destroy()

    telaConsultaEstado = CustomCTk(fg_color="#6D7B74")
    telaConsultaEstado.title("Consulta")
    telaConsultaEstado.geometry("330x250")

    def procura_estado():
        nome_estado = entry_nomeestado.get().strip()
        if not nome_estado:
            messagebox.showwarning("Atenção", "Digite um estado válido.")
            return

        try:
            response = requests.get(
                "http://localhost:3000/endereco", params={"Estado": nome_estado})
            response.raise_for_status()
            dados = response.json()
            clientes = dados.get("data", [])

            if clientes:
                ter_consultaestado(clientes, telaConsultaEstado)
            else:
                messagebox.showinfo("Resultado", "Nenhum cliente encontrado.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {e}")

    NomeUsuario = ctk.CTkLabel(
        telaConsultaEstado, text="Digite o Nome do Estado que deseja Buscar")
    NomeUsuario.place(y=65, x=40)
    entry_nomeestado = ctk.CTkEntry(
        telaConsultaEstado, width=250, height=30, justify="center")
    entry_nomeestado.place(y=95, x=40)

    btProcurar = ctk.CTkButton(
        telaConsultaEstado, text="Procurar", command=procura_estado)
    btProcurar.place(y=145, x=95)

    btVoltar = ctk.CTkButton(telaConsultaEstado, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", font=("Arial", 14, "underline"), command=lambda: voltar_tela1(telaConsultaEstado))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsultaEstado, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaConsultaEstado.destroy)
    btSair.place(y=220, x=95)

    telaConsultaEstado.mainloop()

def ter_consultaestado(dados, telaConsultaEstado):  # Tela Ter onde mostra os dados do Usuário Puxado por estado
    telaResultadoEstado = ctk.CTkToplevel(fg_color="#000000")
    telaResultadoEstado.title("Resultado da Busca")
    telaResultadoEstado.geometry("1200x600")
    telaResultadoEstado.configure(bg="black")
    telaResultadoEstado.resizable(False, False)

    def voltar():
        telaResultadoEstado.destroy()
        telaConsultaEstado()

    btVoltar = ctk.CTkButton(telaResultadoEstado, text="Voltar ao Menu Anterior", text_color="white", fg_color="#000000",
                             hover_color="#575757", font=("Arial", 14, "underline"), command=voltar)
    btVoltar.place(y=10, x=10)

    frame = tk.Frame(telaResultadoEstado, bg="black", width=1100, height=500)
    frame.place(relx=0.5, rely=0.55, anchor="center")
    frame.grid_propagate(False)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    font=("Arial", 12),
                    background="black",
                    foreground="white",
                    fieldbackground="black",
                    rowheight=30,
                    borderwidth=1)

    style.configure("Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#78368E",
                    foreground="white",
                    relief="flat")

    style.map("Treeview",
              background=[('selected', '#347083')],
              foreground=[('selected', 'white')])

    tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
    tree_scroll_y.grid(row=0, column=1, sticky="ns")

    tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
    tree_scroll_x.grid(row=1, column=0, sticky="ew")

    colunas = (
        "Nome", "Sobrenome", "CPF", "DataNascimento", "DataAfiliacao",
        "QntdLivrosReservados", "QntdPendencias", "CEP",
        "Numero", "Bairro", "Cidade", "Estado", "Complemento"
    )

    tree = ttk.Treeview(
        frame,
        columns=colunas,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set
    )
    tree.grid(row=0, column=0, sticky="nsew")

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150, stretch=True)

    tree.tag_configure('oddrow', background="#1a1a1a")
    tree.tag_configure('evenrow', background="#2a2a2a")

    for i, cliente in enumerate(dados):
        endereco = cliente.get("endereco", {})
        valores = (
            cliente.get("Nome", "Não informado"),
            cliente.get("Sobrenome", "Não informado"),
            cliente.get("CPF", "Não informado"),
            cliente.get("DataNascimento", "Não informado"),
            cliente.get("DataAfiliacao", "Não informado"),
            cliente.get("QuantidadeLivrosReservados", 0),
            cliente.get("QuantidadePendencias", 0),
            endereco.get("CEP", "Não informado"),
            endereco.get("Numero", "Não informado"),
            endereco.get("Bairro", "Não informado"),
            endereco.get("Cidade", "Não informado"),
            endereco.get("Estado", "Não informado"),
            endereco.get("Complemento", "Não informado")
        )
        tree.insert("", "end", values=valores, tags=('evenrow' if i % 2 == 0 else 'oddrow'))

    telaResultadoEstado.tk.call('tk', 'scaling', 1.0)

def sec_consulta_nomelivro(telaConsulta):  # Tela Sec de Consulta aos livros
    telaConsulta.destroy()

    telaConsultaLivro = CustomCTk(fg_color="#6D7B74")
    telaConsultaLivro.title("Consulta")
    telaConsultaLivro.geometry("330x250")

    def procura_livro():
        livro_digitado = entry_nomelivro.get().strip()
        if not livro_digitado:
            messagebox.showwarning("Atenção", "Digite um livro válido.")
            return

        try:
            response = requests.get(
                "http://localhost:3000/livro", params={"NomeLivro": livro_digitado})
            response.raise_for_status()
            dados = response.json()
            livros = dados.get("data", [])

            if livros:
                ter_resultadolivro(livros, telaConsultaLivro)
            else:
                messagebox.showinfo("Resultado", "Nenhum livro encontrado.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao buscar livro: {e}")

    NomeLivro = ctk.CTkLabel(
        telaConsultaLivro, text="Digite o Nome do Livro que deseja Buscar")
    NomeLivro.place(y=65, x=40)
    entry_nomelivro = ctk.CTkEntry(
        telaConsultaLivro, width=250, height=30, justify="center")
    entry_nomelivro.place(y=95, x=40)

    btProcurar = ctk.CTkButton(
        telaConsultaLivro, text="Procurar", command=procura_livro)
    btProcurar.place(y=145, x=95)

    btVoltar = ctk.CTkButton(telaConsultaLivro, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", font=("Arial", 14, "underline"), command=lambda: voltar_tela1(telaConsultaLivro))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsultaLivro, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaConsultaLivro.destroy)
    btSair.place(y=220, x=95)

    telaConsultaLivro.mainloop()

def ter_resultadolivro(dados, telaConsultaLivro):  # Tela Ter onde mostra os dados do livro
    telaResultadoLivro = ctk.CTkToplevel(fg_color="#000000")
    telaResultadoLivro.title("Resultado da Busca")
    telaResultadoLivro.geometry("1200x600")
    telaResultadoLivro.configure(bg="black")
    telaResultadoLivro.resizable(False, False)

    def voltar():
        telaResultadoLivro.destroy()
        telaConsultaLivro()

    btVoltar = ctk.CTkButton(telaResultadoLivro, text="Voltar ao Menu Anterior", text_color="white", fg_color="#000000",
                             hover_color="#575757", font=("Arial", 14, "underline"), command=voltar)
    btVoltar.place(y=10, x=10)

    frame = tk.Frame(telaResultadoLivro, bg="black", width=1100, height=500)
    frame.place(relx=0.5, rely=0.55, anchor="center")
    frame.grid_propagate(False)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    font=("Arial", 12),
                    background="black",
                    foreground="white",
                    fieldbackground="black",
                    rowheight=30,
                    borderwidth=1)

    style.configure("Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#78368E",
                    foreground="white",
                    relief="flat")

    style.map("Treeview",
              background=[('selected', '#347083')],
              foreground=[('selected', 'white')])

    tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
    tree_scroll_y.grid(row=0, column=1, sticky="ns")

    tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
    tree_scroll_x.grid(row=1, column=0, sticky="ew")

    colunas = (
        "Autor", "NomeLivro", "Genero", "Idioma", "QntdPagina",
        "Editora", "DataPublicacao", "QntdDisponivel"
    )

    tree = ttk.Treeview(
        frame,
        columns=colunas,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set
    )
    tree.grid(row=0, column=0, sticky="nsew")

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150, stretch=True)

    tree.tag_configure('oddrow', background="#1a1a1a")
    tree.tag_configure('evenrow', background="#2a2a2a")

    for i, livro in enumerate(dados):
        Autor = livro.get('Autor', 'Não informado')
        NomeLivro = livro.get('NomeLivro', 'Não informado')
        Genero = livro.get('genero', {}).get('NomeGenero', 'Gênero não encontrado')
        Idioma = livro.get('Idioma', 'Não informado')
        QntdPagina = livro.get('QuantidadePaginas', 'Não informado')
        Editora = livro.get('Editora', 'Não informado')
        DataPublicacao = livro.get('DataPublicacao', 'Não informado')
        QntdDisponivel = livro.get('QuantidadeDisponivel', 'Não informado')

        tree.insert("", "end", values=(
            Autor, NomeLivro, Genero, Idioma, QntdPagina,
            Editora, DataPublicacao, QntdDisponivel
        ), tags=('evenrow' if i % 2 == 0 else 'oddrow'))

    telaResultadoLivro.tk.call('tk', 'scaling', 1.0)

def sec_consulta_nomeAutor(telaConsulta):  # Tela Sec de Consulta aos Livros pelo Autor
    telaConsulta.destroy()

    telaConsultaAutor = CustomCTk(fg_color="#6D7B74")
    telaConsultaAutor.title("Consulta")
    telaConsultaAutor.geometry("330x250")

    def procura_autor():
        autor_digitado = entry_nomeAutor.get().strip()
        if not autor_digitado:
            messagebox.showwarning("Atenção", "Digite um autor válido.")
            return

        try:
            url = f"http://localhost:3000/livro/autor?NomeAutor={autor_digitado}"
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()
            livros = dados.get("data", [])

            if livros:
                ter_resultadolivro(livros, telaConsultaAutor)
            else:
                messagebox.showinfo("Resultado", "Nenhum autor encontrado.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao buscar livro: {e}")

    NomeAutor = ctk.CTkLabel(
        telaConsultaAutor, text="Digite o Nome do Autor que deseja Buscar")
    NomeAutor.place(y=65, x=40)
    entry_nomeAutor = ctk.CTkEntry(
        telaConsultaAutor, width=250, height=30, justify="center")
    entry_nomeAutor.place(y=95, x=40)

    btProcurar = ctk.CTkButton(
        telaConsultaAutor, text="Procurar", command=procura_autor)
    btProcurar.place(y=145, x=95)

    btVoltar = ctk.CTkButton(telaConsultaAutor, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", font=("Arial", 14, "underline"), command=lambda: voltar_tela1(telaConsultaAutor))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsultaAutor, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaConsultaAutor.destroy)
    btSair.place(y=220, x=95)

    telaConsultaAutor.mainloop()

def sec_consulta_genero(telaConsulta):
    telaConsulta.destroy()

    telaConsultaGenero = CustomCTk(fg_color="#6D7B74")
    telaConsultaGenero.title("Consulta por Gênero")
    telaConsultaGenero.geometry("330x250")

    def procura_genero():
        genero_digitado = entry_nomeGenero.get().strip()
        if not genero_digitado:
            messagebox.showwarning("Atenção", "Digite um gênero válido.")
            return

        try:
            print(f"Enviando requisição para http://localhost:3000/genero?NomeGenero={genero_digitado}")
            response = requests.get(
                "http://localhost:3000/genero", params={"NomeGenero": genero_digitado})
            response.raise_for_status()
            dados = response.json()
            print(f"Resposta da API: {json.dumps(dados, indent=2)}")
            livros = dados.get("data", [])

            if livros:
                # Filtrar livros com gênero correspondente
                livros_filtrados = [
                    livro for livro in livros 
                    if livro.get('genero') and livro['genero'].get('NomeGenero') == genero_digitado
                ]
                print(f"{len(livros_filtrados)} livro(s) encontrado(s) para o gênero {genero_digitado}")
                if livros_filtrados:
                    ter_resultadogenero(livros_filtrados, telaConsultaGenero, genero_digitado)
                else:
                    print(f"Nenhum livro com gênero {genero_digitado} encontrado após filtragem")
                    messagebox.showinfo("Resultado", f"Nenhum livro encontrado para o gênero {genero_digitado}.")
            else:
                print(f"Nenhum livro encontrado para o gênero {genero_digitado}")
                messagebox.showinfo("Resultado", f"Nenhum livro encontrado para o gênero {genero_digitado}.")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar gênero: {e}")
            messagebox.showerror("Erro", f"Erro ao buscar gênero: {e}")

    NomeGenero = ctk.CTkLabel(
        telaConsultaGenero, text="Digite o Nome do Gênero que deseja Buscar")
    NomeGenero.place(y=65, x=40)
    entry_nomeGenero = ctk.CTkEntry(
        telaConsultaGenero, width=250, height=30, justify="center")
    entry_nomeGenero.place(y=95, x=40)

    btProcurar = ctk.CTkButton(
        telaConsultaGenero, text="Procurar", command=procura_genero)
    btProcurar.place(y=145, x=95)

    btVoltar = ctk.CTkButton(telaConsultaGenero, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", font=("Arial", 14, "underline"), command=lambda: voltar_tela1(telaConsultaGenero))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsultaGenero, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaConsultaGenero.destroy)
    btSair.place(y=220, x=95)

    telaConsultaGenero.mainloop()

def ter_resultadogenero(dados, telaConsultaGenero, genero_digitado):
    print(f"Processando {len(dados)} livro(s) na função ter_resultadogenero para o gênero {genero_digitado}")
    
    if not dados or not all('Autor' in livro and 'NomeLivro' in livro for livro in dados):
        print("Erro: Dados recebidos não contêm informações de livros")
        messagebox.showerror("Erro", "Os dados retornados não contêm informações de livros. Verifique a API.")
        return

    telaResultadoGenero = ctk.CTkToplevel(fg_color="#000000")
    telaResultadoGenero.title(f"Resultado da Busca por Gênero: {genero_digitado}")
    telaResultadoGenero.geometry("1200x600")
    telaResultadoGenero.configure(bg="black")
    telaResultadoGenero.resizable(False, False)

    def voltar():
        telaResultadoGenero.destroy()
        telaConsultaGenero()

    btVoltar = ctk.CTkButton(telaResultadoGenero, text="Voltar ao Menu Anterior", text_color="white", fg_color="#000000",
                             hover_color="#575757", font=("Arial", 14, "underline"), command=voltar)
    btVoltar.place(y=10, x=10)

    frame = tk.Frame(telaResultadoGenero, bg="black", width=1100, height=500)
    frame.place(relx=0.5, rely=0.55, anchor="center")
    frame.grid_propagate(False)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    font=("Arial", 12),
                    background="black",
                    foreground="white",
                    fieldbackground="black",
                    rowheight=30,
                    borderwidth=1)

    style.configure("Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#78368E",
                    foreground="white",
                    relief="flat")

    style.map("Treeview",
              background=[('selected', '#347083')],
              foreground=[('selected', 'white')])

    tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
    tree_scroll_y.grid(row=0, column=1, sticky="ns")

    tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
    tree_scroll_x.grid(row=1, column=0, sticky="ew")

    colunas = (
        "Autor", "NomeLivro", "Genero", "Idioma", "QntdPagina",
        "Editora", "DataPublicacao", "QntdDisponivel"
    )

    tree = ttk.Treeview(
        frame,
        columns=colunas,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set
    )
    tree.grid(row=0, column=0, sticky="nsew")

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150, stretch=True)

    tree.tag_configure('oddrow', background="#1a1a1a")
    tree.tag_configure('evenrow', background="#2a2a2a")

    for i, livro in enumerate(dados):
        print(f"Livro {i+1}: {json.dumps(livro, indent=2)}")
        Autor = livro.get('Autor', 'Não informado')
        NomeLivro = livro.get('NomeLivro', 'Não informado')
        Genero = livro.get('genero', {}).get('NomeGenero', 'Gênero não encontrado') if livro.get('genero') is not None else 'Gênero não encontrado'
        Idioma = livro.get('Idioma', 'Não informado')
        QntdPagina = livro.get('QuantidadePaginas', 'Não informado')
        Editora = livro.get('Editora', 'Não informado')
        DataPublicacao = livro.get('DataPublicacao', 'Não informado')
        QntdDisponivel = livro.get('QuantidadeDisponivel', 'Não informado')

        tree.insert("", "end", values=(
            Autor, NomeLivro, Genero, Idioma, QntdPagina,
            Editora, DataPublicacao, QntdDisponivel
        ), tags=('evenrow' if i % 2 == 0 else 'oddrow'))

    telaResultadoGenero.tk.call('tk', 'scaling', 1.0)

# __________________________________CADASTROS________________________________________________ #


def pri_cadastro(tela1):  # Tela Pri de Cadastro, escolhendo o que cadastrar
    tela1.destroy()
    telaCadastro = CustomCTk(fg_color="#6D7B74")
    telaCadastro.title("Cadastro")
    telaCadastro.geometry("250x420")

    opcao = ctk.CTkLabel(
        telaCadastro, text="Escolha uma opção:", text_color="black")
    opcao.place(y=120, x=70)

    btCadastroLivro = ctk.CTkButton(telaCadastro, text="Cadastro Cliente", fg_color="black",
                                    hover_color="#5F8D96", command=lambda: sec_cadastroUsuario(telaCadastro))
    btCadastroLivro.place(y=150, x=60)

    btCadastroLivro = ctk.CTkButton(telaCadastro, text="Cadastro Livro", fg_color="black",
                                    hover_color="#9CAD84", command=lambda: sec_cadastroLivro(telaCadastro))
    btCadastroLivro.place(y=185, x=60)

    btVoltar = ctk.CTkButton(telaCadastro, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", command=lambda: voltar_tela1(telaCadastro), font=("Arial", 14, "underline"))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaCadastro, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaCadastro.destroy)
    btSair.place(y=380, x=105)

    telaCadastro.mainloop()


def sec_cadastroLivro(telaCadastro):  # Tela  Sec de Cadastro do Livro

    # Fecha a tela anterior
    telaCadastro.destroy()

    telaCadastroLivro = CustomCTk(fg_color="#4E5D63")
    telaCadastroLivro.title("Cadastro")
    telaCadastroLivro.geometry("720x480")
    data_var = tk.StringVar(master=telaCadastroLivro)

    # Função onde formata o campo de Data, para adicionar o / entre os campos
    def formatar_data(event):
        entrada = entry_datapub._entry
        valor = entrada.get()
        numeros = ''.join(filter(str.isdigit, valor))

        novo_valor = ""
        if len(numeros) >= 2:
            novo_valor += numeros[:2]
        if len(numeros) >= 4:
            novo_valor += "/" + numeros[2:4]
        if len(numeros) >= 8:
            novo_valor += "/" + numeros[4:8]

        entrada.delete(0, tk.END)
        entrada.insert(0, novo_valor)

        try:
            if len(novo_valor) == 10:
                datetime.strptime(novo_valor, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Data inválida", "Digite uma data válida no formato DD/MM/AAAA.")

    # Função onde Formata os Campos que a utilizam para somente NUMEROS INTEIROS
    def somente_inteiros(valor):
        return valor.isdigit() or valor == ""

    validacao_cmd = telaCadastroLivro.register(somente_inteiros)

    # Parte Autor do Livro Sendo Cadastrado
    autor = ctk.CTkLabel(telaCadastroLivro, text="Digite o Autor/a:")
    autor.place(y=100, x=130)
    entry_autor = ctk.CTkEntry(telaCadastroLivro, width=400, height=15)
    entry_autor.place(y=100, x=230)

    # Parte Nome do Livro Sendo Cadastrado
    Nomelivro = ctk.CTkLabel(
        telaCadastroLivro, text="Digite o Nome do Livro:")
    Nomelivro.place(y=130, x=90)
    entry_nomelivro = ctk.CTkEntry(telaCadastroLivro, width=400, height=15)
    entry_nomelivro.place(y=130, x=230)

    # Parte Editora do Livro Sendo Cadastrado
    NomeEditora = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a Editora:")
    NomeEditora.place(y=160, x=133)
    entry_nomeeditora = ctk.CTkEntry(telaCadastroLivro, width=400, height=15)
    entry_nomeeditora.place(y=160, x=230)

    # Parte Data da Publicação  do Livro Sendo Cadastrado
    DataPub = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a Data Publicada:")
    DataPub.place(y=190, x=85)
    entry_datapub = ctk.CTkEntry(telaCadastroLivro, textvariable=data_var,
                                 placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_datapub.place(y=190, x=230)
    entry_datapub._entry.bind("<FocusOut>", formatar_data)

    # Parte do Genero do Livro Sendo Cadastrado
    Genero = ctk.CTkLabel(
        telaCadastroLivro, text="Selecione o Gênero:")
    Genero.place(y=220, x=110)
    combo_genero = ctk.CTkComboBox(telaCadastroLivro, values=[
                                   nome for _, nome in Generos], width=400, height=15)
    combo_genero.place(y=220, x=230)

    # Parte dos Numeros de Paginas do Livro Sendo Cadastrado
    NmrPag = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a quantidade de Paginas:")
    NmrPag.place(y=250, x=42)
    entry_numeropag = ctk.CTkEntry(telaCadastroLivro, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entry_numeropag.place(y=250, x=230)

    # Parte da Quantidade do Livro Sendo Cadastrado
    Quantidade = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a Quantidade:")
    Quantidade.place(y=280, x=108)
    entry_quantidade = ctk.CTkEntry(telaCadastroLivro, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entry_quantidade.place(y=280, x=230)

    # Parte do Idioma do Livro Sendo Cadastrado
    Idioma = ctk.CTkLabel(
        telaCadastroLivro, text="Digite o Idioma:")
    Idioma.place(y=310, x=135)
    entry_idioma = ctk.CTkEntry(telaCadastroLivro, width=100, height=15)
    entry_idioma.place(y=310, x=230)

    # Botao onde Cadastra o Livro
    cad_livro = ctk.CTkButton(telaCadastroLivro, text="Cadastrar")
    cad_livro.place(y=350, x=300)

    # Botão pra voltar a tela anterior
    btVoltar = ctk.CTkButton(telaCadastroLivro, text="Voltar ao Menu Anterior", fg_color="#4E5D63",
                             hover_color="#3B484D", command=lambda: voltar_tela1(telaCadastroLivro), font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    # Botão pra fechar a tela atual e encerrar o programa
    btfechar = ctk.CTkButton(telaCadastroLivro, text="Fechar", fg_color="black",
                             hover_color="#8B2F2F", command=telaCadastroLivro.destroy)
    btfechar.place(y=430, x=280)

    telaCadastroLivro.mainloop()

def sec_cadastroUsuario(telaCadastro):  # Tela Sec de Cadastro do Usuario
    telaCadastro.destroy()
    telacadastroUsuario = CustomCTk(fg_color="#4A5C63")
    telacadastroUsuario.title("Cadastro")
    telacadastroUsuario.geometry("720x480")

    def cadastro_usuario():
        dados = {
            "Nome": entry_nome.get(),
            "Sobrenome": entry_sobrenome.get(),
            "CPF": entry_cpf.get(),
            "DataNascimento": entry_datanascimento.get(),
            "DataAfiliacao": entry_dataafiliacao.get(),
            "CEP": entry_cep.get(),
            "Rua": entry_rua.get(),
            "Numero": entry_numero.get(),
            "Bairro": entry_bairro.get(),
            "Cidade": entry_cidade.get(),
            "Estado": entry_estado.get(),
            "Complemento": entry_complemento.get()
        }

        try:
            resposta = requests.post(
                "http://localhost:3000/cliente", json=dados)
            if resposta.status_code == 201 or resposta.status_code == 200:
                messagebox.showinfo(
                    "Sucesso", "Usuário cadastrado com sucesso!")
            else:
                messagebox.showerror(
                    "Erro", f"Erro ao cadastrar: {resposta.status_code}")
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao conectar com a API:\n{str(e)}")

    data_nascimento_var = tk.StringVar(master=telacadastroUsuario)
    data_afiliacao_var = tk.StringVar(master=telacadastroUsuario)

    # formata a data para APENAS o campo do Usuario | Nao tem relação com a que formata para o BANCO
    def formatar_data(event):
        entrada = event.widget
        valor = entrada.get()
        numeros = ''.join(filter(str.isdigit, valor))

        novo_valor = ""
        if len(numeros) >= 2:
            novo_valor += numeros[:2]
        if len(numeros) >= 4:
            novo_valor += "/" + numeros[2:4]
        if len(numeros) >= 8:
            novo_valor += "/" + numeros[4:8]

        entrada.delete(0, tk.END)
        entrada.insert(0, novo_valor)

        try:
            if len(novo_valor) == 10:
                datetime.strptime(novo_valor, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Data inválida", "Digite uma data válida no formato DD/MM/AAAA.")

    # Função onde Formata os Campos que a utilizam para somente NUMEROS INTEIROS
    def somente_inteiros(valor):
        return valor.isdigit() or valor == ""

    validacao_cmd = telacadastroUsuario.register(somente_inteiros)

    # Nome do usuario
    Nome = ctk.CTkLabel(telacadastroUsuario, text="Digite o Nome:")
    Nome.place(y=50, x=135)
    entry_nome = ctk.CTkEntry(telacadastroUsuario, width=400, height=15)
    entry_nome.place(y=50, x=230)

    # Sobrenome do usuario
    Sobrenome = ctk.CTkLabel(telacadastroUsuario, text="Digite o Sobrenome:")
    Sobrenome.place(y=80, x=105)
    entry_sobrenome = ctk.CTkEntry(telacadastroUsuario, width=400, height=15)
    entry_sobrenome.place(y=80, x=230)

    # CpF do usuario
    Cpf = ctk.CTkLabel(telacadastroUsuario, text="Digite o CPF:")
    Cpf.place(y=110, x=145)
    entry_cpf = ctk.CTkEntry(telacadastroUsuario, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=120, height=15)
    entry_cpf.place(y=110, x=230)

    # Data de Nascimento do usuario
    DataNascimento = ctk.CTkLabel(
        telacadastroUsuario, text="Digite a Data de Nascimento:")
    DataNascimento.place(y=140, x=53)
    entry_datanascimento = ctk.CTkEntry(telacadastroUsuario, textvariable=data_nascimento_var,
                                        placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_datanascimento.place(y=140, x=230)
    entry_datanascimento._entry.bind("<FocusOut>", formatar_data)

    # Data que o usurao foi afiliado a biblioteca
    DataAfiliacao = ctk.CTkLabel(
        telacadastroUsuario, text="Digite a Data de Afiliação:")
    DataAfiliacao.place(y=170, x=70)
    entry_dataafiliacao = ctk.CTkEntry(telacadastroUsuario, textvariable=data_afiliacao_var,
                                       placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_dataafiliacao.place(y=170, x=230)
    entry_dataafiliacao._entry.bind("<FocusOut>", formatar_data)

    # Cep do usuario
    Cep = ctk.CTkLabel(telacadastroUsuario, text="Digite o Cep:")
    Cep.place(y=200, x=147)
    entry_cep = ctk.CTkEntry(telacadastroUsuario, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=100, height=15, justify="center")
    entry_cep.place(y=200, x=230)

    # Rua do usuario
    Rua = ctk.CTkLabel(telacadastroUsuario, text="Digite a Rua:")
    Rua.place(y=230, x=147)
    entry_rua = ctk.CTkEntry(telacadastroUsuario, width=250, height=15)
    entry_rua.place(y=230, x=230)

    # Numero da casa do usuario
    Numero = ctk.CTkLabel(telacadastroUsuario, text="Digite o Número:")
    Numero.place(y=260, x=125)
    entry_numero = ctk.CTkEntry(telacadastroUsuario, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entry_numero.place(y=260, x=230)

    # Bairro do usuario
    Bairro = ctk.CTkLabel(telacadastroUsuario, text="Digite o Bairro:")
    Bairro.place(y=290, x=135)
    entry_bairro = ctk.CTkEntry(telacadastroUsuario, width=250, height=15)
    entry_bairro.place(y=290, x=230)

    # Cidade do usuario
    Cidade = ctk.CTkLabel(telacadastroUsuario, text="Digite a Cidade:")
    Cidade.place(y=320, x=130)
    entry_cidade = ctk.CTkEntry(telacadastroUsuario, width=250, height=15)
    entry_cidade.place(y=320, x=230)

    # Estado do usuario
    Estado = ctk.CTkLabel(telacadastroUsuario, text="Digite o Estado:")
    Estado.place(y=350, x=130)
    entry_estado = ctk.CTkEntry(telacadastroUsuario, width=250, height=15)
    entry_estado.place(y=350, x=230)

    # Complemento da casa do usuario
    Complemento = ctk.CTkLabel(
        telacadastroUsuario, text="Digite o Complemento ( Se Tiver):")
    Complemento.place(y=380, x=30)
    entry_complemento = ctk.CTkEntry(telacadastroUsuario, width=250, height=15)
    entry_complemento.place(y=380, x=230)

    # Botao onde Cadastra o Usuario
    cad_usuario = ctk.CTkButton(
        telacadastroUsuario, text="Cadastrar", command=cadastro_usuario)
    cad_usuario.place(y=425, x=200)

    # Botao de Voltar a twla anterior
    btVoltar = ctk.CTkButton(telacadastroUsuario, text="Voltar ao Menu Anterior", fg_color="#4A5C63",
                             hover_color="#3C474D", command=lambda: voltar_tela1(telacadastroUsuario), font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    # Botao para fechar a tela atual
    btfechar = ctk.CTkButton(telacadastroUsuario, text="Fechar", fg_color="black",
                             hover_color="#8B2F2F", command=telacadastroUsuario.destroy)
    btfechar.place(y=425, x=360)

    telacadastroUsuario.mainloop()
# __________________________________RESERVAS_________________________________________________ #


def pri_reserva(tela1):  # Tela Pri de Reservas, escolhendo o que fazer
    tela1.destroy()
    telaReservas = CustomCTk(fg_color="#B89778")
    telaReservas.title("reservas")
    telaReservas.geometry("250x420")

    opcao = ctk.CTkLabel(
        telaReservas, text="Escolha uma opção:", text_color="black")
    opcao.place(y=120, x=70)

    btConsultaReserva = ctk.CTkButton(
        telaReservas, text="Consultar Reservas", fg_color="black", hover_color="#1B263B")
    btConsultaReserva.place(y=150, x=60)

    btNewReserva = ctk.CTkButton(telaReservas, text="Nova Reserva", fg_color="black",
                                 hover_color="#A0522D", command=lambda: sec_nova_reserva(telaReservas))
    btNewReserva.place(y=185, x=60)

    btVoltar = ctk.CTkButton(telaReservas, text="Voltar ao Menu Anterior", text_color="black", fg_color="#B89778",
                             hover_color="#A0522D", command=lambda: voltar_tela1(telaReservas), font=("Arial", 14, "underline"))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaReservas, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaReservas.destroy)
    btSair.place(y=385, x=105)

    telaReservas.mainloop()


def sec_nova_reserva(reserva):  # Tela Sec de Nova Reserva
    reserva.destroy()
    telaNovaReserva = CustomCTk(fg_color="#2B2B2B")
    telaNovaReserva.title("Nova Reserva")
    telaNovaReserva.geometry("720x480")

    def cadastro_novareserva():
        dados = {
            "CPFReserva": entry_cpfreserva.get(),
            "NomeLivro": entry_nomelivro.get(),
            "QntdLivro": entry_qntdlivro.get(),
            "DataRetirada": entry_dataretirada.get(),
            "DataVolta": entry_datavolta.get(),
            "Entrega": entry_retirada.get(),
            "Observacao": entry_observacao.get()
        }

        try:
            resposta = requests.post(
                "http://localhost:3000/reservas", json=dados)
            if resposta.status_code == 201 or resposta.status_code == 200:
                messagebox.showinfo(
                    "Sucesso", "Reserva cadastrada com sucesso!")
            else:
                messagebox.showerror(
                    "Erro", f"Erro ao cadastrar: {resposta.status_code}")
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao conectar com a API:\n{str(e)}")

    data_retirada_var = tk.StringVar(master=telaNovaReserva)
    data_volta_var = tk.StringVar(master=telaNovaReserva)

    def formatar_data(event):
        entrada = event.widget
        valor = entrada.get()
        numeros = ''.join(filter(str.isdigit, valor))

        novo_valor = ""
        if len(numeros) >= 2:
            novo_valor += numeros[:2]
        if len(numeros) >= 4:
            novo_valor += "/" + numeros[2:4]
        if len(numeros) >= 8:
            novo_valor += "/" + numeros[4:8]

        entrada.delete(0, tk.END)
        entrada.insert(0, novo_valor)

        try:
            if len(novo_valor) == 10:
                datetime.strptime(novo_valor, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Data inválida", "Digite uma data válida no formato DD/MM/AAAA.")

    def somente_inteiros(valor):
        return valor.isdigit() or valor == ""

    validacao_cmd = telaNovaReserva.register(somente_inteiros)

    # CPF do usuario que vai ficar reservado
    CpfReserva = ctk.CTkLabel(telaNovaReserva, text="Digite o CPF:")
    CpfReserva.place(y=100, x=120)
    entry_cpfreserva = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entry_cpfreserva.place(y=100, x=230)

    # Nome do Livro que vai ser reservado
    Nomelivro = ctk.CTkLabel(telaNovaReserva, text="Digite o Nome do Livro:")
    Nomelivro.place(y=130, x=90)
    entry_nomelivro = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entry_nomelivro.place(y=130, x=230)

    # Qunantidade que vai ser reservada
    qntdLivros = ctk.CTkLabel(telaNovaReserva, text="Digite a Quantidade:")
    qntdLivros.place(y=160, x=105)
    entry_qntdlivro = ctk.CTkEntry(telaNovaReserva, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entry_qntdlivro.place(y=160, x=230)

    # Data que esta sendo retirada o livro
    dataRetirada = ctk.CTkLabel(
        telaNovaReserva, text="Digite a Data da Retirada:")
    dataRetirada.place(y=190, x=77)
    entry_dataretirada = ctk.CTkEntry(telaNovaReserva, textvariable=data_retirada_var,
                                      placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_dataretirada.place(y=190, x=230)
    entry_dataretirada._entry.bind("<FocusOut>", formatar_data)

    # Data prevista para que o Livro for devolvido
    dataVolta = ctk.CTkLabel(
        telaNovaReserva, text="Digite a Data Prevista para Volta:")
    dataVolta.place(y=220, x=35)
    entry_datavolta = ctk.CTkEntry(telaNovaReserva, textvariable=data_volta_var,
                                   placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_datavolta.place(y=220, x=230)
    entry_datavolta._entry.bind("<FocusOut>", formatar_data)

    entrega = ctk.CTkLabel(telaNovaReserva, text="Digite a forma de retirada:")
    entrega.place(y=250, x=75)
    entry_retirada = ctk.CTkEntry(telaNovaReserva, width=100, height=15)
    entry_retirada.place(y=250, x=230)

    # OBS
    observacao = ctk.CTkLabel(telaNovaReserva, text="Observaçãa da Reserva:")
    observacao.place(y=280, x=115)
    entry_observacao = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entry_observacao.place(y=280, x=230)

    btVoltar = ctk.CTkButton(telaNovaReserva, text="Voltar ao Menu Anterior", fg_color="#2B2B2B",
                             hover_color="#121212", command=lambda: pri_reserva(telaNovaReserva), font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    btfechar = ctk.CTkButton(telaNovaReserva, text="Fechar", fg_color="black",
                             hover_color="#8B2F2F", command=telaNovaReserva.destroy)
    btfechar.place(y=430, x=280)

    btReservar = ctk.CTkButton(
        telaNovaReserva, text="Reservar", fg_color="#1E5128", hover_color="#4E9F3D", command=cadastro_novareserva)
    btReservar.place(y=430, x=400)

    telaNovaReserva.mainloop()

# ______________________________________EXCLUSÃO______________________________________________ #


def pri_exclusao(tela1):  # Tela Primaria de Exclusão, escolhendo o que fazer
    tela1.destroy()
    telaExclusão = CustomCTk()
    telaExclusão.title("Exclusão de Livros")
    telaExclusão.geometry("1080x720")

    btSair = ctk.CTkButton(telaExclusão, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=lambda: voltar_tela1(telaExclusão))
    btSair.place(y=385, x=105)

    telaExclusão.mainloop()


if __name__ == "__main__":
    tela1()
