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

// Rota para buscar clientes
app.get('/cliente', async (req, res) => {
    try {
        const { data, error } = await supabase
            .from('cliente')
            .select('*');

        if (error) {
            console.error('Erro ao buscar clientes:', error);
            throw error;
        }

        if (!data || data.length === 0) {
            return res.status(404).json({ message: 'Nenhum cliente encontrado' });
        }

        res.status(200).json({ message: 'Clientes encontrados com sucesso', data });
    } catch (error) {
        console.error('Erro ao buscar clientes:', error);
        res.status(500).json({ message: 'Erro ao buscar clientes', error: error.message });
    }
});

// Rota para cadastrar um cliente
app.post('/cliente', async (req, res) => {
    try {
        console.log('Dados recebidos do Python:', JSON.stringify(req.body, null, 2));

        const {
            CEP, Rua, Numero, Bairro, Cidade, Estado,
            Nome, Sobrenome, CPF, DataNascimento, DataAfiliacao
        } = req.body;

        // Validação dos campos obrigatórios
        if (!CEP || !Rua || !Numero || !Bairro || !Cidade || !Estado ||
            !Nome || !Sobrenome || !CPF || !DataNascimento || !DataAfiliacao) {
            return res.status(400).json({ message: 'Todos os campos são obrigatórios' });
        }

        // Formatar datas explicitamente
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
            Nome, Sobrenome, CPF,
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
                Estado: dadosFormatados.Estado
            }])
            .select('EnderecoID')
            .single();

        if (enderecoError) {
            console.error('Erro ao cadastrar endereço:', enderecoError);
            throw enderecoError;
        }

        console.log('Endereço cadastrado:', enderecoData);

        const enderecoId = enderecoData?.EnderecoID;

        if (!enderecoId) {
            console.log('Erro: EnderecoID não obtido');
            return res.status(500).json({ message: 'Não foi possível obter o ID do endereço' });
        }

        // Inserir cliente com o EnderecoID
        const clientePayload = {
            Nome: dadosFormatados.Nome,
            Sobrenome: dadosFormatados.Sobrenome,
            CPF: dadosFormatados.CPF,
            DataNascimento: dadosFormatados.DataNascimento,
            DataAfiliacao: dadosFormatados.DataAfiliacao,
            EnderecoID: enderecoId
        };

        console.log('Payload do cliente para o Supabase:', JSON.stringify(clientePayload, null, 2));

        const { data: clienteData, error: clienteError } = await supabase
            .from('cliente')
            .insert([clientePayload])
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

app.listen(3000, () => {
    console.log('Servidor tá rodando, meu consagrado!');
});
