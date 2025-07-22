Seja Bem Vindo!
 
 Este é um projeto feito baseado em um sistema interno de uma Biblioteca,constando em um APP para os funcionarios, voltado a inserção, remoção e consultas tanto de livros quanto de leitores.
A ideia para o projeto surgiu de um trabalho da Faculdade, onde precisamos criar um mini sistema de Biblioteca em Python, onde a saida era mesmo pelo Terminal, porém na entrag do mesmo, fiquei pensando
sobre a ideia e me surgiu a vontade de criar um sistema realmente funcional, pratico e simples.

 O APP foi desenvolvido por Python e durante o desenvolvimento, foi utilzado diversas bibliotecas até chegar nas que realmente atenderam o intuito do projeto, foram as seguintes: TkInter, CustomTkInter,
DateTime, Resquest e Json.
 Junto ao APP, foi desenvolvido uma API em JavaScript, assim fazendo a integração ao Banco de Dados que foi hospedado ao Supabase. Algumas regras de negócio implantada na API:R
Resevas, quando é feito uma reserva abate no numero de estoque do livro, e quando volta, acrescenta novamente. 
Multas, onde quando ultrapassa a data de entrega fornecedia pelo usuario na hora de reservar algum livro, acrescenta o valor de R$1,50 a tabela de multas, sendo assim, sempre q se der 00:00 e o funcionario não confirmar a volta do livro,
sera aumentado o valor, e o usuario recebera uma notificação via e-mail. 

O Banco de Dados foi criado através do SupaBase, utilizando o PostgreSQL, tendo 6 tabelas
ao total, todas em perfeita sincronia trabalhando juntas.

No APP, o funcionario terá as seguintes opções:

1- Consulta, podendo consultar de 4 formar diferentes:
    Consulta por Nome de Clinte | Consulta por Estado | Consulta por Nome de Livro Cadastrado | Consulta por Editora | Consulta por Genero dos Livros.

2- Cadastro:
    Cadastro de Cliente, onde será cadastrado todos os dados pessoais e de endereço do mesmo.
    Cadastro de Livro, onde será cadastrados todos os dados relevantes do livro.

3- Reservas:
    Nova reserva, onde podera ser realizada junto com os dados do cliente junto com os do livro, tendo adicional de multa, caso passe a data prevista para volta do livro.
    Reservas, onde podera consultar as reservas que estão em aberto no momento.

4- Exclusão:
    Exclusão por ClienteID, onde sera pego atraves da opção Consulta.
    Exclusão por LivroID, onde tambem sera pego atraves da Consulta.


