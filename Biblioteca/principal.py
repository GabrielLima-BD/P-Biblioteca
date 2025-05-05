import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import datetime



def tela1():                                 # tela1 é a inical, o primeiro contato com o usuario
    tela1 = ctk.CTk(fg_color="#3C4C34")
    tela1.title("Inicio")
    tela1.geometry("250x420")

    textprincipal = ctk.CTkLabel(tela1, text="Seja Bem Vindo!")
    textprincipal.place(y=45, x=80)

    textopcoes = ctk.CTkLabel(tela1, text="Escolha uma opção:")
    textopcoes.place(y=115, x=70)

    btConsulta = ctk.CTkButton(tela1, text="Consulta", fg_color="black",hover_color="#1B263B", command=lambda: pri_consulta(tela1))
    btConsulta.place(y=150, x=60)

    btCadastro = ctk.CTkButton(tela1, text="Cadastro", fg_color="black", hover_color="#A0522D", command=lambda: pri_cadastro(tela1))
    btCadastro.place(y=185, x=60)

    btReservas = ctk.CTkButton(tela1, text="Reservas", fg_color="black",hover_color="#B89778", command=lambda: pri_reserva(tela1))
    btReservas.place(y=220, x=60)

    btExclusao = ctk.CTkButton(tela1, text="Exclusão", fg_color="black",hover_color="#4A7043", command=lambda: pri_exclusao(tela1))
    btExclusao.place(y=255, x=60)

    btSair = ctk.CTkButton(tela1, text="Sair", fg_color="black",hover_color="#8B2F2F", command=tela1.destroy)
    btSair.place(y=385, x=105)

    tela1.mainloop()
def voltar_tela1(tela_atual):                # função para voltar a tela1 e fechar a atual
    tela_atual.destroy()
    tela1()

#__________________________________________________________________________________________________________________________#

def pri_consulta(tela1):                     # telas primaria das consultas, ver os livros ja existentes dentro da biblioteca
    # fechando a tela principal para fins de organização
    tela1.destroy()

    telaConsulta = ctk.CTk()
    telaConsulta.title("Consulta")
    telaConsulta.geometry("1080x720")

    btSair = ctk.CTkButton(telaConsulta, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=lambda: voltar_tela1(telaConsulta))
    btSair.place(y=385, x=105)

    telaConsulta.mainloop()

#__________________________________________________________________________________________________________________________#

def pri_cadastro(tela1):                     # tela primaria de cadastro dos livros
    # fechando a tela principal para fins de organização
    tela1.destroy()

    telaCadastro = ctk.CTk(fg_color="#E1A480")
    telaCadastro.title("Cadastro")
    telaCadastro.geometry("720x480")

    # Criação de data_var antes de usá-la
    data_var = tk.StringVar(master=telaCadastro)

    # Função que formata a data
    def formatar_data(event):
        entrada = entrada_DataPub._entry
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
                datetime.datetime.strptime(novo_valor, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Data inválida", "Digite uma data válida no formato DD/MM/AAAA.")
    # Função onde verica oque o usuario digita par apenas aceitar numeros inteiros

    def somente_inteiros(valor):
        return valor.isdigit() or valor == ""
    # faz parte da função de apenas numeros
    validacao_cmd = telaCadastro.register(somente_inteiros)

    # autor
    autor = ctk.CTkLabel(telaCadastro, text="Digite o Autor/a:",text_color="black")
    autor.place(y=100, x=130)
    entrada_autor = ctk.CTkEntry(telaCadastro, width=400, height=15)
    entrada_autor.place(y=100, x=230)

    # Nome do Livro
    Nomelivro = ctk.CTkLabel(telaCadastro, text="Digite o Nome do Livro:",text_color="black")
    Nomelivro.place(y=130, x=90)
    entrada_Nomelivro = ctk.CTkEntry(telaCadastro, width=400, height=15)
    entrada_Nomelivro.place(y=130, x=230)

    # Nome da Editora
    NomeEditora = ctk.CTkLabel(telaCadastro, text="Digite a Editora:",text_color="black")
    NomeEditora.place(y=160, x=133)
    entrada_NomeEditora = ctk.CTkEntry(telaCadastro, width=400, height=15)
    entrada_NomeEditora.place(y=160, x=230)

    # Data da Publicação
    DataPub = ctk.CTkLabel(telaCadastro, text="Digite a Data Publicada:",text_color="black")
    DataPub.place(y=190, x=85)
    entrada_DataPub = ctk.CTkEntry(telaCadastro, textvariable=data_var,placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entrada_DataPub.place(y=190, x=230)
    entrada_DataPub._entry.bind("<FocusOut>", formatar_data)

    # Genero do livro
    Genero = ctk.CTkLabel(telaCadastro, text="Digite o Gênero:",text_color="black")
    Genero.place(y=220, x=132)
    entrada_Genero = ctk.CTkEntry(telaCadastro, width=150, height=15)
    entrada_Genero.place(y=220, x=230)

    # Numeros de paginas
    NmrPag = ctk.CTkLabel(telaCadastro, text="Digite a quantidade de Paginas:",text_color="black")
    NmrPag.place(y=250, x=42)
    entrada_NmrPag = ctk.CTkEntry(telaCadastro, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entrada_NmrPag.place(y=250, x=230)

    # Quantidade Disponiveis
    Quantidade = ctk.CTkLabel(telaCadastro, text="Digite a Quantidade:",text_color="black")
    Quantidade.place(y=280, x=108)
    entrada_Quantidade = ctk.CTkEntry(telaCadastro, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entrada_Quantidade.place(y=280, x=230)

    # Idioma do livro
    Idioma = ctk.CTkLabel(telaCadastro, text="Digite o Idioma:",text_color="black")
    Idioma.place(y=310, x=135)
    entrada_Idioma = ctk.CTkEntry(telaCadastro, width=100, height=15)
    entrada_Idioma.place(y=310, x=230)

    # voltar ao menu anterior
    btVoltar = ctk.CTkButton(telaCadastro, text="Voltar ao Menu Anterior", text_color="black", fg_color="#E1A480" ,hover_color="#C4744F", command=lambda: voltar_tela1(telaCadastro), font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    # fechar tela
    btfechar = ctk.CTkButton(telaCadastro, text="Fechar", fg_color="black", hover_color="#8B2F2F", command=telaCadastro.destroy)
    btfechar.place(y=430, x=280)

    telaCadastro.mainloop()

#__________________________________________________________________________________________________________________________#

def pri_reserva(tela1):                      # tela primaria das reservas dos livros, onde tem as reservas ja feitas e criar novas reservas
    # fechando a tela principal para fins de organização
    tela1.destroy()

    telaReservas = ctk.CTk(fg_color="#B89778")
    telaReservas.title("reservas")
    telaReservas.geometry("250x420")

    opcao = ctk.CTkLabel(telaReservas, text="Escolha uma opção:", text_color="black")
    opcao.place(y=120,x=70)

    btConsultaReserva = ctk.CTkButton( telaReservas, text="Consultar Reservas", fg_color="black", hover_color="#1B263B")
    btConsultaReserva.place(y=150, x=60)

    btNewReserva = ctk.CTkButton( telaReservas, text="Nova Reserva", fg_color="black", hover_color="#A0522D",command=lambda: sec_nova_reserva(telaReservas))
    btNewReserva.place(y=185, x=60)

    # voltar ao menu anterior
    btVoltar = ctk.CTkButton(telaReservas, text="Voltar ao Menu Anterior", text_color="black", fg_color="#B89778", hover_color="#A0522D", command=lambda: voltar_tela1(telaReservas), font=("Arial", 14, "underline"))
    btVoltar.place(y=5, x=5)

    btSair = ctk.CTkButton(telaReservas, text="Sair", fg_color="black", hover_color="#8B2F2F", command=telaReservas.destroy)
    btSair.place(y=385, x=105)

    telaReservas.mainloop()
def sec_nova_reserva(reserva):               # tela secundaria da de reservas, onde fica a função de criar uma nova reserva
    # fecha a janela anterior para fins de organização
    reserva.destroy()
    
    telaNovaReserva = ctk.CTk(fg_color="#2B2B2B")
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
                datetime.datetime.strptime(novo_valor, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Data inválida", "Digite uma data válida no formato DD/MM/AAAA.")

    def somente_inteiros(valor):
        return valor.isdigit() or valor == ""
    validacao_cmd = telaNovaReserva.register(somente_inteiros)

    
    # nome da pessoa que vai reservaar o livro
    NomeReserva = ctk.CTkLabel(telaNovaReserva, text="Nome da Reserva:")
    NomeReserva.place(y=100, x=120)
    entradaNomeReserva = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entradaNomeReserva.place(y=100, x=230)

    # nome do livro a ser reservado
    Nomelivro = ctk.CTkLabel(telaNovaReserva, text="Digite o Nome do Livro:")
    Nomelivro.place(y=130, x=90)
    entrada_Nomelivro = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entrada_Nomelivro.place(y=130, x=230)

    # genero do livro a ser reservado
    generoLivro = ctk.CTkLabel(telaNovaReserva, text="Digite o Gênero do livro:")
    generoLivro.place(y=160, x=87)
    entrada_generoLivro = ctk.CTkEntry(telaNovaReserva, width=400, height=15)
    entrada_generoLivro.place(y=160, x=230)

    # idioma do livro a ser reservado
    Idioma = ctk.CTkLabel(telaNovaReserva, text="Digite o Idioma:")
    Idioma.place(y=190, x=132)
    entrada_Idioma = ctk.CTkEntry(telaNovaReserva, width=100, height=15)
    entrada_Idioma.place(y=190, x=230)
    
    # quantidade de livros reservados
    qntdLivros = ctk.CTkLabel(telaNovaReserva, text="Digite a Quantidade:")
    qntdLivros.place(y=220, x=105)
    entrada_qntdLivros = ctk.CTkEntry(telaNovaReserva, validate="key", validatecommand=(
        validacao_cmd, "%P"), width=60, height=15, justify="center")
    entrada_qntdLivros.place(y=220, x=230)
    
    # data da retirada do livro
    dataRetirada = ctk.CTkLabel(telaNovaReserva, text="Digite a Data da Retirada:")
    dataRetirada.place(y=250, x=77)
    entrada_data_retirada = ctk.CTkEntry(telaNovaReserva, textvariable=data_retirada_var,placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entrada_data_retirada.place(y=250, x=230)
    entrada_data_retirada._entry.bind("<FocusOut>", formatar_data)

    # provisao de volta do livro
    dataVolta = ctk.CTkLabel(telaNovaReserva, text="Digite a Data Prevista para Volta:")
    dataVolta.place(y=280, x=35)
    entrada_data_volta = ctk.CTkEntry(telaNovaReserva, textvariable=data_volta_var, placeholder_text="DD/MM/AAAA", width=85, height=15, justify="center")
    entrada_data_volta.place(y=280, x=230)
    entrada_data_volta._entry.bind("<FocusOut>", formatar_data)
    
    # metodo de entrega do livro
    entrega = ctk.CTkLabel(telaNovaReserva, text="Digite a forma de retirada:")
    entrega.place(y=310, x=75)
    entrada_entrega = ctk.CTkEntry(telaNovaReserva, width=100, height=15)
    entrada_entrega.place(y=310, x=230)
    

    btVoltar = ctk.CTkButton(
        telaNovaReserva, text="Voltar ao Menu Anterior", fg_color="#2B2B2B", hover_color="#121212",
        command=lambda: pri_reserva(telaNovaReserva),font=("Arial", 14, "underline"))
    btVoltar.place(y=15, x=15)

    btfechar = ctk.CTkButton(
        telaNovaReserva, text="Fechar", fg_color="black",
        hover_color="#8B2F2F", command=telaNovaReserva.destroy)
    btfechar.place(y=430,x=280
    )

    telaNovaReserva.mainloop()

#__________________________________________________________________________________________________________________________#
def pri_exclusao(tela1):                     # tela primaria onde vai ser feito a exclusao de livros da biblioteca
    # fechando a tela principal para fins de organização
    tela1.destroy()

    telaExclusão = ctk.CTk()
    telaExclusão.title("Exclusão de Livros")
    telaExclusão.geometry("1080x720")

    btSair = ctk.CTkButton(telaExclusão, text="Sair", fg_color="black",
                           hover_color="#8B2F2F", command=lambda: voltar_tela1(telaExclusão))
    btSair.place(y=385, x=105)

    telaExclusão.mainloop()

#__________________________________________________________________________________________________________________________#



tela1()                                      # chamando a tela 1 para o cod em si funcionar

