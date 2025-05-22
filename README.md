Seja Bem Vindo

Este é um projeto feito baseado em um sistema interno e externo de uma Biblioteca, tendo aplicativo para funcionarios internos, e um site responisvo e utilitario
  para os usuarios, onde podera ser realizadas reservas pelo site, ver livros mais acessados e os mais reservados. 
  
  APP interno foi desenvolvido por Python com algumas
  funções do TKInter, mas contendo grande parte grafica do CustomTkinter. Na parte de integração ao banco de dados, foi feita uma API em JavaScript, onde tem toda
  a nossa parte de regra de negocio, alguma delas por exemplo são na parte de resevas, quando é feito uma reserva abate no numero de estoque do livro, e quando 
  volta, acrescenta novamente. Outra regra de exemplo que exerce na API, é a de multas, onde quando ultrapassa a data de entrega fornecedia pelo usuario na hora
  de reservar algum livro, acrescenta o valor de R$1,50 a tabela de multas, sendo assim, sempre q se der 00:00 e o funcionario nao confirmar a volta do livro,
  sera aumentado o valor, e o usuario recebera uma notificação via e-mail. O Banco de Dados foi criado através do SupaBase, utilizando o PostgreSQL, tendo 6 tabelas
  ao total, todas se interligando


Aplicação interna para os fucionarios terá 4 areas principas, sendo elas:

1- Consulta, podendo consultar de 4 formar diferentes:
    Consulta por Nome de Clinte | Consulta por Estado | Consulta por Nome de Livro Cadastrado | Consulta por Editora.

2- Cadastro:
    Cadastro de Cliente, onde será cadastrado todos os dados pessoais e de endereço do mesmo.
    Cadastro de Livro, onde será cadastrados todos os dados relevantes do livro.

3- Reservas:
    Nova reserva, onde podera ser realizada junto com os dados do cliente junto com os do livro, tendo adicional de multa, caso passe a data prevista para volta do livro.
    Reservas, onde podera consultar as reservas que estão em aberto no momento.

4- Exclusão:
    Exclusão por ClienteID, onde sera pego atraves da opção Consulta.
    Exclusão por LivroID, onde tambem sera pego atraves da Consulta.
