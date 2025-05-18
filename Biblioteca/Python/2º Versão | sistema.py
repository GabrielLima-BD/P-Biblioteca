import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import datetime
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Configuração do banco
Host = {
    "host": "localhost",
    "user": "root",
    "password": "7505",
    "database": "biblioteca"
}
# Lista para rastrear IDs de after
after_ids = []
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

# ________________________________________________________________________________ #

# Função Responsavel por conectar ao banco para mandar os dados


def conectar():
    try:
        conexao = mysql.connector.connect(**Host)
        if conexao.is_connected():
            print("Conexão ao MySQL bem-sucedida!")
            db_info = conexao.server_info
            print(f"Versão do servidor MySQL: {db_info}")
            cursor = conexao.cursor()
            cursor.execute("SELECT DATABASE();")
            banco = cursor.fetchone()
            print(f"Banco de dados conectado: {banco[0]}")
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# ________________________________________________________________________________ #


def cadastro_livro(Autor, NomeLivro, GeneroID, Idioma, QuantidadePaginas, Editora, DataPublicacao, QuantidadeDisponivel):
    conexao = conectar()
    if conexao:
        cursor = None
        try:
            cursor = conexao.cursor()
            sql = """
                INSERT INTO livro (Autor, NomeLivro, GeneroID, Idioma, QuantidadePaginas, Editora, DataPublicacao, QuantidadeDisponivel)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (Autor, NomeLivro, GeneroID, Idioma, QuantidadePaginas,
                       Editora, DataPublicacao, QuantidadeDisponivel)
            cursor.execute(sql, valores)
            conexao.commit()
            print(f"Livro inserido com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao inserir livro: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if conexao.is_connected():
                conexao.close()
                print("Conexão ao MySQL encerrada.")
    return False

# ________________________________________________________________________________ #

# Classe base para janelas que sobrescreve destroy


class CustomCTk(ctk.CTk):
    def destroy(self):
        global after_ids
        for id in after_ids:
            try:
                self.after_cancel(id)
            except:
                pass
        after_ids.clear()
        super().destroy()

# ________________________________________________________________________________ #


def tela1():
    global after_ids
    tela1 = CustomCTk(fg_color="#3C4C34")
    tela1.title("Inicio")
    tela1.geometry("250x420")

    textprincipal = ctk.CTkLabel(tela1, text="Seja Bem Vindo!")
    textprincipal.place(y=45, x=80)

    textopcoes = ctk.CTkLabel(tela1, text="Escolha uma opção:")
    textopcoes.place(y=115, x=70)

    btConsulta = ctk.CTkButton(tela1, text="Consulta", fg_color="black",
                               hover_color="#1B263B", command=lambda: pri_consulta(tela1))
    btConsulta.place(y=150, x=60)

    btCadastro = ctk.CTkButton(tela1, text="Cadastro", fg_color="black",
                               hover_color="#A0522D", command=lambda: pri_cadastro(tela1))
    btCadastro.place(y=185, x=60)

    btReservas = ctk.CTkButton(tela1, text="Reservas", fg_color="black",
                               hover_color="#B89778", command=lambda: pri_reserva(tela1))
    btReservas.place(y=220, x=60)

    btExclusao = ctk.CTkButton(tela1, text="Exclusão", fg_color="black",
                               hover_color="#4A7043", command=lambda: pri_exclusao(tela1))
    btExclusao.place(y=255, x=60)

    btSair = ctk.CTkButton(tela1, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=tela1.destroy)
    btSair.place(y=385, x=105)

    tela1.mainloop()


def voltar_tela1(tela_atual):
    tela_atual.destroy()
    tela1()

# ________________________________________________________________________________ #


def pri_consulta(tela1):
    tela1.destroy()
    telaConsulta = CustomCTk()
    telaConsulta.title("Consulta")
    telaConsulta.geometry("1080x720")

    btSair = ctk.CTkButton(telaConsulta, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=lambda: voltar_tela1(telaConsulta))
    btSair.place(y=385, x=105)

    telaConsulta.mainloop()

# ________________________________________________________________________________ #


def pri_cadastro(tela1):
    tela1.destroy()
    telaCadastro = CustomCTk(fg_color="#B89778")
    telaCadastro.title("Cadastro")
    telaCadastro.geometry("250x420")

    opcao = ctk.CTkLabel(
        telaCadastro, text="Escolha uma opção:", text_color="black")
    opcao.place(y=120, x=70)

    btConsultaReserva = ctk.CTkButton(telaCadastro, text="Cadastro Cliente", fg_color="black",
                                      hover_color="#1B263B", command=lambda: sec_cadastroUsuario(telaCadastro))
    btConsultaReserva.place(y=150, x=60)

    btCadastroLivro = ctk.CTkButton(telaCadastro, text="Cadastro Livro", fg_color="black",
                                    hover_color="#A0522D", command=lambda: sec_cadastroLivro(telaCadastro))
    btCadastroLivro.place(y=185, x=60)

    btVoltar = ctk.CTkButton(telaCadastro, text="Voltar ao Menu Anterior", text_color="black", fg_color="#B89778",
                             hover_color="#A0522D", command=lambda: voltar_tela1(telaCadastro), font=("Arial", 14, "underline"))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaCadastro, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=telaCadastro.destroy)
    btSair.place(y=385, x=105)

    telaCadastro.mainloop()


def sec_cadastroLivro(telaCadastro):

    # Fecha a tela anterior
    telaCadastro.destroy()

    telaCadastroLivro = CustomCTk(fg_color="#E1A480")
    telaCadastroLivro.title("Cadastro")
    telaCadastroLivro.geometry("720x480")

    # Função onde chama o Cadastro dos Livros
    def chamar_cadastro():
        # Pega os dados inseridos nos campos com o GET.()
        Autor = entry_autor.get()
        NomeLivro = entry_nomelivro.get()
        GeneroSelecionado = combo_genero.get()
        Idioma = entry_idioma.get()
        QuantidadePaginas = entry_numeropag.get()
        Editora = entry_nomeeditora.get()
        DataPublicacao = entry_datapub.get()
        QuantidadeDisponivel = entry_quantidade.get()

        # Verifica os campos, mandando o usuarios completar todos os que faltaram
        if not Autor or not NomeLivro or not GeneroSelecionado or not QuantidadePaginas or not Editora or not DataPublicacao or not QuantidadeDisponivel:
            messagebox.showerror(
                "Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        # Extrai o GeneroID do gênero selecionado
        GeneroID = None
        for id, nome in Generos:
            if nome == GeneroSelecionado:
                GeneroID = id
                break

        # Verifica o Genero selecionado com os existentes
        if GeneroID is None:
            messagebox.showerror("Erro", "Gênero selecionado inválido.")
            return

        # formata a data colocada para a que o banco suporta, mudando de D/M/A para A/M/D
        try:
            DataPublicacao = datetime.strptime(
                DataPublicacao, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror(
                "Erro", "Data inválida. Use o formato DD/MM/YYYY.")
            return

        # Cadastrando o Livro
        if cadastro_livro(
            Autor,
            NomeLivro,
            GeneroID,
            Idioma,
            QuantidadePaginas,
            Editora,
            DataPublicacao,
            QuantidadeDisponivel
        ):
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        else:
            messagebox.showerror(
                "Erro", "Erro ao cadastrar o livro. Tente novamente.")

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
    autor = ctk.CTkLabel(
        telaCadastroLivro, text="Digite o Autor/a:", text_color="black")
    autor.place(y=100, x=130)
    entry_autor = ctk.CTkEntry(telaCadastroLivro, width=400, height=15)
    entry_autor.place(y=100, x=230)

    # Parte Nome do Livro Sendo Cadastrado
    Nomelivro = ctk.CTkLabel(
        telaCadastroLivro, text="Digite o Nome do Livro:", text_color="black")
    Nomelivro.place(y=130, x=90)
    entry_nomelivro = ctk.CTkEntry(telaCadastroLivro, width=400, height=15)
    entry_nomelivro.place(y=130, x=230)

    # Parte Editora do Livro Sendo Cadastrado
    NomeEditora = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a Editora:", text_color="black")
    NomeEditora.place(y=160, x=133)
    entry_nomeeditora = ctk.CTkEntry(telaCadastroLivro, width=400, height=15)
    entry_nomeeditora.place(y=160, x=230)

    # Parte Data da Publicação  do Livro Sendo Cadastrado
    DataPub = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a Data Publicada:", text_color="black")
    DataPub.place(y=190, x=85)
    entry_datapub = ctk.CTkEntry(telaCadastroLivro, textvariable=data_var,
                                 placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_datapub.place(y=190, x=230)
    entry_datapub._entry.bind("<FocusOut>", formatar_data)

    # Parte do Genero do Livro Sendo Cadastrado
    Genero = ctk.CTkLabel(
        telaCadastroLivro, text="Selecione o Gênero:", text_color="black")
    Genero.place(y=220, x=110)
    combo_genero = ctk.CTkComboBox(telaCadastroLivro, values=[
                                   nome for _, nome in Generos], width=400, height=15)
    combo_genero.place(y=220, x=230)

    # Parte dos Numeros de Paginas do Livro Sendo Cadastrado
    NmrPag = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a quantidade de Paginas:", text_color="black")
    NmrPag.place(y=250, x=42)
    entry_numeropag = ctk.CTkEntry(telaCadastroLivro, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entry_numeropag.place(y=250, x=230)

    # Parte da Quantidade do Livro Sendo Cadastrado
    Quantidade = ctk.CTkLabel(
        telaCadastroLivro, text="Digite a Quantidade:", text_color="black")
    Quantidade.place(y=280, x=108)
    entry_quantidade = ctk.CTkEntry(telaCadastroLivro, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entry_quantidade.place(y=280, x=230)

    # Parte do Idioma do Livro Sendo Cadastrado
    Idioma = ctk.CTkLabel(
        telaCadastroLivro, text="Digite o Idioma:", text_color="black")
    Idioma.place(y=310, x=135)
    entry_idioma = ctk.CTkEntry(telaCadastroLivro, width=100, height=15)
    entry_idioma.place(y=310, x=230)

    # Parte onde Cadastra o Livro
    cad_livro = ctk.CTkButton(
        telaCadastroLivro, text="Cadastrar", command=chamar_cadastro)
    cad_livro.place(y=350, x=230)

    # Botão pra voltar a tela anterior
    btVoltar = ctk.CTkButton(telaCadastroLivro, text="Voltar ao Menu Anterior", text_color="black", fg_color="#E1A480",
                             hover_color="#C4744F", command=lambda: voltar_tela1(telaCadastroLivro), font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    # Botão pra fechar a tela atual e encerrar o programa
    btfechar = ctk.CTkButton(telaCadastroLivro, text="Fechar", fg_color="black",
                             hover_color="#8B2F2F", command=telaCadastroLivro.destroy)
    btfechar.place(y=430, x=280)

    telaCadastroLivro.mainloop()


def sec_cadastroUsuario(telaCadastro):
    telaCadastro.destroy()
    telacadastroUsuario = CustomCTk(fg_color="#E1A480")
    telacadastroUsuario.title("Cadastro")
    telacadastroUsuario.geometry("720x480")

    data_var = tk.StringVar(master=telacadastroUsuario)

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

    validacao_cmd = telacadastroUsuario.register(somente_inteiros)

    Nome = ctk.CTkLabel(telacadastroUsuario,
                        text="Digite o Nome", text_color="black")
    Nome.place(y=100, x=130)
    entry_nome = ctk.CTkEntry(telacadastroUsuario, width=400, height=15)
    entry_nome.place(y=100, x=230)

    Sobrenome = ctk.CTkLabel(
        telacadastroUsuario, text="Digite o Sobrenome:", text_color="black")
    Sobrenome.place(y=130, x=90)
    entry_sobrenome = ctk.CTkEntry(telacadastroUsuario, width=400, height=15)
    entry_sobrenome.place(y=130, x=230)

    Cpf = ctk.CTkLabel(telacadastroUsuario,
                       text="Digite o CPF:", text_color="black")
    Cpf.place(y=160, x=133)
    entry_cpf = ctk.CTkEntry(telacadastroUsuario, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=250, height=15, justify="center")
    entry_cpf.place(y=160, x=230)

    DataNascimentc = ctk.CTkLabel(
        telacadastroUsuario, text="Digite a Data de Nascimento:", text_color="black")
    DataNascimentc.place(y=190, x=41)
    entry_datanascimento = ctk.CTkEntry(telacadastroUsuario, textvariable=data_var,
                                        placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_datanascimento.place(y=190, x=230)
    entry_datanascimento._entry.bind("<FocusOut>", formatar_data)

    DataAfiliacao = ctk.CTkLabel(
        telacadastroUsuario, text="Digite a Data de Afiliação:", text_color="black")
    DataAfiliacao.place(y=220, x=61)
    entry_dataafiliacao = ctk.CTkEntry(telacadastroUsuario, textvariable=data_var,
                                       placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entry_dataafiliacao.place(y=220, x=230)
    entry_dataafiliacao._entry.bind("<FocusOut>", formatar_data)

    btVoltar = ctk.CTkButton(telacadastroUsuario, text="Voltar ao Menu Anterior", text_color="black", fg_color="#E1A480",
                             hover_color="#C4744F", command=lambda: voltar_tela1(telacadastroUsuario), font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    btfechar = ctk.CTkButton(telacadastroUsuario, text="Fechar", fg_color="black",
                             hover_color="#8B2F2F", command=telacadastroUsuario.destroy)
    btfechar.place(y=430, x=280)

    telacadastroUsuario.mainloop()

# ________________________________________________________________________________ #


def pri_reserva(tela1):
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


def sec_nova_reserva(reserva):
    reserva.destroy()
    telaNovaReserva = CustomCTk(fg_color="#2B2B2B")
    telaNovaReserva.title("Nova Reserva")
    telaNovaReserva.geometry("720x480")

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

    NomeReserva = ctk.CTkLabel(telaNovaReserva, text="Nome da Reserva:")
    NomeReserva.place(y=100, x=120)
    entradaNomeReserva = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entradaNomeReserva.place(y=100, x=230)

    Nomelivro = ctk.CTkLabel(telaNovaReserva, text="Digite o Nome do Livro:")
    Nomelivro.place(y=130, x=90)
    entrada_Nomelivro = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entrada_Nomelivro.place(y=130, x=230)

    generoLivro = ctk.CTkLabel(
        telaNovaReserva, text="Digite o Gênero do livro:")
    generoLivro.place(y=160, x=87)
    entrada_generoLivro = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entrada_generoLivro.place(y=160, x=230)

    Idioma = ctk.CTkLabel(telaNovaReserva, text="Digite o Idioma:")
    Idioma.place(y=190, x=132)
    entrada_Idioma = ctk.CTkEntry(telaNovaReserva, width=100, height=15)
    entrada_Idioma.place(y=190, x=230)

    qntdLivros = ctk.CTkLabel(telaNovaReserva, text="Digite a Quantidade:")
    qntdLivros.place(y=220, x=105)
    entrada_qntdLivros = ctk.CTkEntry(telaNovaReserva, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entrada_qntdLivros.place(y=220, x=230)

    dataRetirada = ctk.CTkLabel(
        telaNovaReserva, text="Digite a Data da Retirada:")
    dataRetirada.place(y=250, x=77)
    entrada_data_retirada = ctk.CTkEntry(telaNovaReserva, textvariable=data_retirada_var,
                                         placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entrada_data_retirada.place(y=250, x=230)
    entrada_data_retirada._entry.bind("<FocusOut>", formatar_data)

    dataVolta = ctk.CTkLabel(
        telaNovaReserva, text="Digite a Data Prevista para Volta:")
    dataVolta.place(y=280, x=35)
    entrada_data_volta = ctk.CTkEntry(telaNovaReserva, textvariable=data_volta_var,
                                      placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entrada_data_volta.place(y=280, x=230)
    entrada_data_volta._entry.bind("<FocusOut>", formatar_data)

    entrega = ctk.CTkLabel(telaNovaReserva, text="Digite a forma de retirada:")
    entrega.place(y=310, x=75)
    entrada_entrega = ctk.CTkEntry(telaNovaReserva, width=100, height=15)
    entrada_entrega.place(y=310, x=230)

    btVoltar = ctk.CTkButton(telaNovaReserva, text="Voltar ao Menu Anterior", fg_color="#2B2B2B",
                             hover_color="#121212", command=lambda: pri_reserva(telaNovaReserva), font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    btfechar = ctk.CTkButton(telaNovaReserva, text="Fechar", fg_color="black",
                             hover_color="#8B2F2F", command=telaNovaReserva.destroy)
    btfechar.place(y=430, x=280)

    telaNovaReserva.mainloop()

# ________________________________________________________________________________ #


def pri_exclusao(tela1):
    tela1.destroy()
    telaExclusão = CustomCTk()
    telaExclusão.title("Exclusão de Livros")
    telaExclusão.geometry("1080x720")

    btSair = ctk.CTkButton(telaExclusão, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=lambda: voltar_tela1(telaExclusão))
    btSair.place(y=385, x=105)

    telaExclusão.mainloop()


tela1()
