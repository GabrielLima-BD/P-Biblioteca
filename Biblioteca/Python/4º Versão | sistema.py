import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import requests


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

def tela1():  # Tela Inical para o Funcionario

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

    opcao = ctk.CTkLabel(telaConsulta, text="Escolha uma opção:", text_color="black")
    opcao.place(y=110, x=70)

    btConsultaINomesuario = ctk.CTkButton(telaConsulta, text="Nome Usuario", fg_color="black",hover_color="#5F8D96", command=lambda: sec_consulta_nomeusuario(telaConsulta))
    btConsultaINomesuario.place(y=140, x=60)

    btConsultaEstado = ctk.CTkButton(telaConsulta, text="Por Estado", fg_color="black",hover_color="#9CAD84")
    btConsultaEstado.place(y=170, x=60)

    btConsultaNomeLivro = ctk.CTkButton(telaConsulta, text="Nome Livro", fg_color="black",hover_color="#B36A5E")
    btConsultaNomeLivro.place(y=200, x=60)

    btConsultaNomeAutor = ctk.CTkButton(telaConsulta, text="Nome Autor", fg_color="black",hover_color="#7C5E67")
    btConsultaNomeAutor.place(y=230, x=60)

    btConsultaNomeLivro = ctk.CTkButton(telaConsulta, text="Por Genero", fg_color="black",hover_color="#ADA584")
    btConsultaNomeLivro.place(y=260, x=60)


    btVoltar = ctk.CTkButton(telaConsulta, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",hover_color="#55635C", command=lambda: voltar_tela1(telaConsulta), font=("Arial", 14, "underline"))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsulta, text="Sair", fg_color="black",hover_color="#8B2F2F", command=telaConsulta.destroy)
    btSair.place(y=380, x=105)

    telaConsulta.mainloop()

def sec_consulta_nomeusuario(telaConsulta): # Tela Sec de Consulta aos Usuarios pelo nome
    telaConsulta.destroy()
    
    telaConsultaUsuario = CustomCTk(fg_color="#6D7B74")
    telaConsultaUsuario.title("Consulta")
    telaConsultaUsuario.geometry("330x250")
    
    # pega o Nome digitado e Busca atraves da API
    def procura_usuario():
        nome_digitado = entry_nomeusuario.get().strip() 
        if not nome_digitado:
            print("Digite um nome válido.")
            return

        try:
            response = requests.get("http://localhost:3000/cliente", params={"Nome": nome_digitado})
            response.raise_for_status()
            dados = response.json()
            # Extrai o array de clientes do JSON
            clientes = dados.get("data", [])
            
            if clientes:
                ter_resultadonome(clientes,telaConsultaUsuario)  # chama a função que mostra a tabela
            else:
                print("Nenhum cliente encontrado.")
        except requests.exceptions.RequestException as e:
            print("Erro ao buscar usuário:", e)

    NomeUsuario = ctk.CTkLabel(telaConsultaUsuario, text="Digite o Nome do Usuario que deseja Buscar")
    NomeUsuario.place(y=65, x=40)
    entry_nomeusuario = ctk.CTkEntry(telaConsultaUsuario, width=250, height=30, justify="center")
    entry_nomeusuario.place(y=95, x=40)    

    btProcurar = ctk.CTkButton(telaConsultaUsuario, text="Procurar", command=procura_usuario)
    btProcurar.place(y=145, x=95)

    btVoltar = ctk.CTkButton(telaConsultaUsuario, text="Voltar ao Menu Anterior", text_color="black", fg_color="#6D7B74",
                             hover_color="#55635C", font=("Arial", 14, "underline"), command=lambda: voltar_tela1(telaConsultaUsuario))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaConsultaUsuario, text="Sair", fg_color="black",hover_color="#8B2F2F", command=telaConsultaUsuario.destroy)
    btSair.place(y=220, x=95)
    
    telaConsultaUsuario.mainloop()

def ter_resultadonome(dados,telaConsultaUsuario): # Tela Ter onde mostra os dados do Usuario Puxado   
    telaResultadoNome = ctk.CTkToplevel(fg_color="#000000")
    telaResultadoNome.title("Resultado da Busca")
    telaResultadoNome.geometry("750x420")
    telaResultadoNome.configure(bg="black")
    telaResultadoNome.resizable(False, False) 
    
    def voltar():
        telaResultadoNome.destroy() 
        telaConsultaUsuario()  
    
    btVoltar = ctk.CTkButton(telaResultadoNome, text="Voltar ao Menu Anterior", text_color="white", fg_color="#000000",
                             hover_color="#575757", font=("Arial", 14, "underline"), command=voltar)
    btVoltar.place(y=10, x=10)

    # === Frame da tabela ===
    frame = tk.Frame(telaResultadoNome, bg="black", width=900, height=450)
    frame.place(relx=0.5, rely=0.55, anchor="center")
    frame.grid_propagate(False) 

    # === Estilo visual ===
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

    # === Scrollbars ===
    tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
    tree_scroll_y.grid(row=0, column=1, sticky="ns")

    tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
    tree_scroll_x.grid(row=1, column=0, sticky="ew")

    # === Colunas da Tabela ===
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

    # === Conectar os scrollbars à tabela ===
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    # === Redimensionamento automático no grid ===
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # === Configurações das colunas ===
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120, stretch=True)

    # === Linhas alternadas ===
    tree.tag_configure('oddrow', background="#1a1a1a")
    tree.tag_configure('evenrow', background="#2a2a2a")

    # === Inserção de dados ===
    for i, cliente in enumerate(dados):
        endereco = cliente["endereco"]
        valores = (
            cliente["Nome"], cliente["Sobrenome"], cliente["CPF"], cliente["DataNascimento"],
            cliente["DataAfiliacao"], cliente["QuantidadeLivrosReservados"], cliente["QuantidadePendencias"],
            endereco["CEP"], endereco["Numero"], endereco["Bairro"], endereco["Cidade"],
            endereco["Estado"], endereco["Complemento"]
        )
        tree.insert("", "end", values=valores, tags=('oddrow' if i % 2 == 0 else 'evenrow',))

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
        telaNovaReserva, text="Reservar", fg_color="#1E5128", hover_color="#4E9F3D", command= cadastro_novareserva)
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


tela1()
