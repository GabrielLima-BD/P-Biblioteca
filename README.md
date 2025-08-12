# Seja Bem Vindo!

Este é um projeto baseado em um sistema interno de uma Biblioteca, consistindo em um APP para os funcionários, voltado à inserção, remoção e consultas tanto de livros quanto de leitores.

A ideia para o projeto surgiu de um trabalho da Faculdade, onde precisávamos criar um mini sistema de Biblioteca em Python, com saída pelo Terminal. Porém, na entrega, fiquei pensando sobre a ideia e me surgiu a vontade de criar um sistema realmente funcional, prático e simples.

O APP foi desenvolvido em Python e durante o desenvolvimento foram utilizadas diversas bibliotecas até chegar nas que realmente atenderam o intuito do projeto, sendo elas: TkInter, CustomTkInter, DateTime, Requests e JSON.

Junto ao APP, foi desenvolvida uma API em JavaScript, fazendo a integração com o Banco de Dados hospedado no Supabase. Algumas regras de negócio implantadas na API:

- **Reservas**: quando é feita uma reserva, o número de estoque do livro é abatido; quando o livro é devolvido, o estoque é acrescido novamente.
- **Multas**: quando ultrapassa a data de entrega fornecida pelo usuário na reserva, é acrescentado o valor de R$1,50 na tabela de multas. A cada dia que passa à meia-noite sem que o funcionário confirme a devolução do livro, o valor aumenta e o usuário recebe uma notificação via e-mail.

O Banco de Dados foi criado através do Supabase, utilizando PostgreSQL, com 6 tabelas ao total, todas em perfeita sincronia trabalhando juntas.

## No APP, o funcionário terá as seguintes opções:

1. **Consulta**, podendo consultar de 4 formas diferentes:  
   - Consulta por Nome de Cliente  
   - Consulta por Estado  
   - Consulta por Nome de Livro Cadastrado  
   - Consulta por Editora  
   - Consulta por Gênero dos Livros  

2. **Cadastro**:  
   - Cadastro de Cliente, onde serão cadastrados todos os dados pessoais e de endereço.  
   - Cadastro de Livro, onde serão cadastrados todos os dados relevantes do livro.

3. **Reservas**:  
   - Nova reserva, onde poderá ser realizada junto com os dados do cliente e do livro, tendo adicional de multa caso ultrapasse a data prevista para devolução.  
   - Consulta das reservas em aberto no momento.

4. **Exclusão**:  
   - Exclusão por ClienteID, obtido via Consulta.  
   - Exclusão por LivroID, também obtido via Consulta.
