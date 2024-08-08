# Teste Técnico - Aplicação de Upload e Gerenciamento de Dados em CSV

## Descrição
Este projeto consiste no desenvolvimento de uma aplicação web para permitir o upload de um arquivo CSV (dados_teste.csv), salvar os dados desse arquivo em um banco de dados e realizar operações como edição, adição de novos itens, download da tabela atualizada/filtrada e visualização do histórico de alterações da tabela.

## Requisitos Funcionais
1. **Interface de Upload:**
    - Uma página com um formulário para fazer upload de um arquivo CSV.
    - Um botão para enviar o arquivo.
2. **Backend:**
    - Um endpoint para receber o arquivo CSV enviado pelo frontend.
    - Parser para ler o arquivo CSV e extrair os dados.
    - Lógica para salvar os dados no banco de dados.
    - Funcionalidade de edição dos dados da tabela no banco.
    - Funcionalidade de adicionar novos itens à tabela no banco.
    - Funcionalidade de exportar a tabela atualizada/filtrada em formato CSV.
    - Implementação de um histórico de alterações da tabela, registrando as modificações feitas.
3. **Frontend:**
    - A tecnologia utilizada no frontend fica a critério do desenvolvedor.
    - Uma página para exibir os dados do CSV em uma tabela.
    - Funcionalidade de filtro para filtrar os dados exibidos na tabela com base em critérios como coluna, valor etc.
    - Funcionalidade de busca para buscar dados na tabela com base em palavras-chave.
    - Botões para editar os dados da tabela e adicionar novos itens.
    - Botão para baixar a tabela atualizada/filtrada em formato CSV.
    - Visualização do histórico de alterações da tabela.
4. **Fluxo de Uso Exemplo:**
    - Passo 1: O usuário acessa a página de upload da aplicação.
    - Passo 2: Ele seleciona um arquivo CSV a partir de seu dispositivo e envia o arquivo.
    - Passo 3: O backend recebe o arquivo, lê e salva os dados no banco de dados.
    - Passo 4: O usuário é redirecionado para a página de visualização da tabela, onde pode ver os dados do arquivo CSV.
    - Passo 5: Ele utiliza as funcionalidades de filtro e busca para encontrar os dados desejados.
    - Passo 6: O usuário decide editar um item da tabela e faz as alterações necessárias.
    - Passo 7: Após a edição, ele pode visualizar o histórico de alterações para verificar as modificações realizadas.
    - Passo 8: Se necessário, o usuário pode adicionar novos itens à tabela.
    - Passo 9: Ao finalizar suas operações, ele pode baixar a tabela atualizada em formato CSV.
5. **Tecnologias:**
    - O frontend pode ser desenvolvido utilizando a tecnologia de preferência do desenvolvedor, como React, Angular, Vue.js, ou qualquer outra.
    - O backend pode ser desenvolvido em Node.js, Python.
    - Utilize um banco de dados relacional ou NoSQL para armazenar os dados do CSV.

## Requisitos não Funcionais
1. A aplicação deve ser responsiva e ter uma boa usabilidade.
2. O código deve seguir as boas práticas de desenvolvimento, incluindo padrões de codificação, arquitetura limpa e modularidade.
3. Testes unitários devem ser desenvolvidos para garantir a qualidade do código. Isso é um plus e não um requisito obrigatório.

## Entregáveis
1. Código fonte da aplicação.
2. Instruções detalhadas sobre como configurar e executar a aplicação localmente.
3. Documentação explicando a arquitetura da aplicação, escolhas tecnológicas, decisões de design, entre outros detalhes relevantes.

## Observações
- O desenvolvedor pode estender o teste adicionando mais funcionalidades extras, como autenticação de usuários, paginação na tabela, etc., se desejar.

## Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).