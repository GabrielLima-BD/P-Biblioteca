import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';


dotenv.config();
console.log('URL do Supabase:', process.env.SUPABASE_URL);
console.log('Chave do Supabase:', process.env.SUPABASE_KEY ? 'OK' : 'FALHA');

const app = express();
app.use(cors());
app.use(express.json());

// Conecta ao Supabase
const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_KEY
);

// Função para formatar data de DD/MM/YYYY para YYYY-MM-DD
function formatarData(data) {
    if (!data || !/^\d{2}\/\d{2}\/\d{4}$/.test(data)) {
        console.log(`Data inválida ou não formatada: ${data}`);
        return data; // Retorna sem alterar se não for data válida
    }
    const [dia, mes, ano] = data.split('/');
    const dataFormatada = `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`;
    console.log(`Data formatada: ${data} -> ${dataFormatada}`);
    return dataFormatada;
}

//____________________________ROTAS___________________________//

//_________________ROTAS PARA AS CONSULTAS____________________//


// Rota para buscar clientes por nome
app.get('/cliente', async (req, res) => {
    try {
        const { Nome } = req.query;

        if (!Nome) {
            return res.status(400).json({ message: 'O campo Nome é obrigatório' });
        }

        const { data, error } = await supabase
            .from('cliente')
            .select('*, endereco(*)')
            .ilike('Nome', `%${Nome.trim()}%`);

        if (error) {
            console.error('Erro ao buscar cliente:', error);
            return res.status(500).json({ message: 'Erro ao buscar cliente', error: error.message });
        }

        return res.status(200).json({ message: 'Cliente(s) encontrados com sucesso', data });
    } catch (error) {
        console.error('Erro inesperado:', error);
        return res.status(500).json({ message: 'Erro inesperado ao buscar cliente', error: error.message });
    }
});

// Rota para buscar clientes por Estado
app.get('/endereco', async (req, res) => {
  try {
    const { Estado } = req.query;
    if (!Estado) return res.status(400).json({ message: 'O campo Estado é obrigatório' });

    const { data, error } = await supabase
      .from('cliente')
      .select(`
        Nome,
        Sobrenome,
        CPF,
        DataNascimento,
        DataAfiliacao,
        QuantidadeLivrosReservados,
        QuantidadePendencias,
        endereco (
          CEP,
          Numero,
          Bairro,
          Cidade,
          Estado,
          Complemento
        )
      `);

    if (error) {
      console.error('Erro ao buscar clientes:', error);
      return res.status(500).json({ message: 'Erro ao buscar clientes', error: error.message });
    }

    // Filtro manual no back-end para os Estados
    const estadoAlvo = Estado.trim().toUpperCase();
    const clientesFiltrados = data.filter(cliente => {
      const estado = cliente.endereco?.Estado?.toUpperCase() || '';
      return estado === estadoAlvo;
    });

    return res.status(200).json({ message: 'Clientes encontrados com sucesso', data: clientesFiltrados });
  } catch (error) {
    console.error('Erro inesperado:', error);
    return res.status(500).json({ message: 'Erro inesperado ao buscar clientes', error: error.message });
  }
});

// Rota para buscar por nome do livro
app.get('/livro', async (req, res) => {
    try {
        const { NomeLivro } = req.query;

        if (!NomeLivro) {
            return res.status(400).json({ message: 'O campo Nome do Livro é obrigatório' });
        }

        const { data, error } = await supabase
        .from('livro')
        .select(`
            Autor,
            NomeLivro,
            Idioma,
            QuantidadePaginas,
            Editora,
            DataPublicacao,
            QuantidadeDisponivel,
            genero:GeneroID (
            NomeGenero
            )
        `)
        .ilike('NomeLivro', `%${NomeLivro.trim()}%`);



        if (error) {
            console.error('Erro ao buscar livro:', error);
            return res.status(500).json({ message: 'Erro ao buscar livro', error: error.message });
        }

        if (!data || data.length === 0) {
            return res.status(404).json({ message: 'Livro não encontrado' });
        }

        return res.status(200).json({ message: 'Livro(s) encontrado(s) com sucesso', data });

    } catch (error) {
        console.error('Erro inesperado:', error);
        return res.status(500).json({ message: 'Erro inesperado ao buscar livro', error: error.message });
    }
});

// Rota para buscar por nome do Autor
app.get('/livro/autor', async (req, res) => {
    try {
        const { NomeAutor } = req.query;

        if (!NomeAutor) {
            return res.status(400).json({ message: 'O campo Nome do Autor é obrigatório' });
        }

        const { data, error } = await supabase
        .from('livro')
        .select(`
            Autor,
            NomeLivro,
            Idioma,
            QuantidadePaginas,
            Editora,
            DataPublicacao,
            QuantidadeDisponivel,
            genero:GeneroID (
            NomeGenero
            )
        `)
        .ilike('Autor', `%${NomeAutor.trim()}%`);



        if (error) {
            console.error('Erro ao buscar livro:', error);
            return res.status(500).json({ message: 'Erro ao buscar Autor(a)', error: error.message });
        }

        if (!data || data.length === 0) {
            return res.status(404).json({ message: 'Autor(a) não encontrado' });
        }

        return res.status(200).json({ message: 'Autor(a) encontrado(a) com sucesso', data });

    } catch (error) {
        console.error('Erro inesperado:', error);
        return res.status(500).json({ message: 'Erro inesperado ao buscar Autor(a)', error: error.message });
    }
});

//___________________ROTAS PARA CADASTRO______________________//

// Rota para cadastrar um cliente
app.post('/cliente', async (req, res) => {
    try {
        console.log('Dados de Cadastro de Usuario e Endereço recebidos do Python:', JSON.stringify(req.body, null, 2));

        // dados recebidos pelo python
        const {
            CEP, Rua, Numero, Bairro, Cidade, Estado, Complemento,
            Nome, Sobrenome, CPF, DataNascimento, DataAfiliacao
        } = req.body;

        // Validação dos campos obrigatórios
        if (!CEP || !Rua || !Numero || !Bairro || !Cidade || !Estado ||
            !Nome || !Sobrenome || !CPF || !DataNascimento || !DataAfiliacao) {
            return res.status(400).json({ message: 'Todos os campos são obrigatórios' });
        }
        // formata as datas para a inserção ao banco
        const dataNascimentoFormatada = formatarData(DataNascimento);
        const dataAfiliacaoFormatada = formatarData(DataAfiliacao);

        // Verificar se as datas foram formatadas corretamente
        if (dataNascimentoFormatada === DataNascimento || dataAfiliacaoFormatada === DataAfiliacao) {
            console.log('Erro: Datas não foram formatadas:', { DataNascimento, DataAfiliacao });
            return res.status(400).json({ message: 'Formato de data inválido. Use DD/MM/YYYY.' });
        }

        // Dados para inserção
        const dadosFormatados = {
            CEP, Rua, Numero, Bairro, Cidade, Estado, 
            Complemento, Nome, Sobrenome, CPF,
            DataNascimento: dataNascimentoFormatada,
            DataAfiliacao: dataAfiliacaoFormatada
        };

        console.log('Dados formatados para inserção:', JSON.stringify(dadosFormatados, null, 2));

        // Inserir endereço e obter EnderecoID
        const { data: enderecoData, error: enderecoError } = await supabase
            .from('endereco')
            .insert([{
                CEP: dadosFormatados.CEP,
                Rua: dadosFormatados.Rua,
                Numero: dadosFormatados.Numero,
                Bairro: dadosFormatados.Bairro,
                Cidade: dadosFormatados.Cidade,
                Estado: dadosFormatados.Estado,
                Complemento: dadosFormatados.Complemento
            }])
            .select('EnderecoID')
            .single();

        if (enderecoError) {
            console.error('Erro ao cadastrar endereço:', enderecoError);
            throw enderecoError;
        }

        console.log('Endereço cadastrado:', enderecoData);

        const enderecoId = enderecoData.EnderecoID;

        if (!enderecoId) {
            console.log('Erro: EnderecoID não obtido');
            return res.status(500).json({ message: 'Não foi possível obter o ID do endereço' });
        }

        // Inserir cliente com o EnderecoID
        const clientedados = {
            Nome: dadosFormatados.Nome,
            Sobrenome: dadosFormatados.Sobrenome,
            CPF: dadosFormatados.CPF,
            DataNascimento: dadosFormatados.DataNascimento,
            DataAfiliacao: dadosFormatados.DataAfiliacao,
            EnderecoID: enderecoId
        };

        console.log('Dados do cliente para o Supabase:', JSON.stringify(clientedados, null, 2));

        const { data: clienteData, error: clienteError } = await supabase
            .from('cliente')
            .insert([clientedados])
            .select()
            .single();

        if (clienteError) {
            console.error('Erro ao cadastrar cliente:', clienteError);
            throw clienteError;
        }

        res.status(201).json({
            message: 'Cliente e endereço cadastrados com sucesso',
            cliente: clienteData,
            endereco: enderecoData
        });

    } catch (error) {
        console.error('Erro final:', error);
        res.status(500).json({ message: 'Erro ao cadastrar cliente', error: error.message });
    }
});


// rota para cadastrar uma nova reserva
app.post('/reservas', async (req, res) => {
    try {
        console.log('Dados recebidos do Python:', JSON.stringify(req.body, null, 2));

        const {
            CPFReserva, NomeLivro, QntdLivro,
            DataRetirada, DataVolta, Entrega, Observacao
        } = req.body;

        if (!CPFReserva || !NomeLivro || !QntdLivro || !DataRetirada || !DataVolta || !Entrega || !Observacao) {
            return res.status(400).json({ message: 'Todos os campos são obrigatórios' });
        }

        const DataRetiradaFormatada = formatarData(DataRetirada);
        const DataVoltaFormatada = formatarData(DataVolta);

        if (DataRetiradaFormatada === DataRetirada || DataVoltaFormatada === DataVolta) {
            console.log('Erro: Datas não foram formatadas:', { DataRetirada, DataVolta });
            return res.status(400).json({ message: 'Formato de data inválido. Use DD/MM/YYYY.' });
        }

        const dadosFormatados = {
            QntdLivro, Entrega, Observacao,
            DataRetirada: DataRetiradaFormatada,
            DataVolta: DataVoltaFormatada
        };

        console.log('Dados formatados para inserção:', JSON.stringify(dadosFormatados, null, 2));

        const { data: clienteData, error: clienteErro } = await supabase
            .from('cliente')
            .select('ClienteID')
            .eq('CPF', CPFReserva.trim())
            .maybeSingle();

        console.log('Resultado da busca do cliente:', clienteData);

        if (clienteErro) {
            console.error('Erro ao buscar cliente:', clienteErro);
            return res.status(500).json({ message: 'Erro na consulta de cliente' });
        }

        if (!clienteData) {
            return res.status(402).json({ message: 'Cliente não encontrado' });
        }

        const IDClienteReserva = clienteData.ClienteID;

        const { data: livroData, error: livroErro } = await supabase
            .from('livro')
            .select('LivroID, NomeLivro')
            .ilike('NomeLivro', `%${NomeLivro.trim()}%`)
            .maybeSingle();

        if (livroErro) {
            console.error('Erro na busca do livro:', livroErro);
            return res.status(504).json({ message: 'Erro na consulta de livro' });
        }

        if (!livroData) {
            return res.status(404).json({ message: 'Livro não encontrado' });
        }

        console.log('Resultado da busca do livro:', livroData);

        const IDLivroReserva = livroData.LivroID;
        const reservadados = {
            ClienteID: IDClienteReserva,
            LivroID: IDLivroReserva,
            DataRetirada: dadosFormatados.DataRetirada,
            DataPrevistaEntrega: dadosFormatados.DataVolta,
            FormaRetirada: dadosFormatados.Entrega,
            QuantidadeReservada: dadosFormatados.QntdLivro,
            Observacao: dadosFormatados.Observacao
        };

        console.log('Dados da reserva para inserir:', JSON.stringify(reservadados, null, 2));

        const { data: reservaData, error: reservaErro } = await supabase
            .from('reservas')
            .insert([reservadados])
            .select()
            .single();

        if (reservaErro) {
            console.error('Erro ao cadastrar reserva:', reservaErro);
            return res.status(500).json({ message: 'Erro ao inserir reserva' });
        }

        res.status(201).json({
            message: 'Reserva cadastrada com sucesso',
            reserva: reservaData
        });

    } catch (error) {
        console.error('Erro final:', error);
        res.status(500).json({ message: 'Erro ao cadastrar reserva', error: error.message });
    }
});


//____________________________________________________________//

app.listen(3000, () => {
    console.log('Servidor tá rodando, meu consagrado!');
});
