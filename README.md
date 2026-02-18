Sistema de Gestão de Plataforma Multiusuário (LIDDER/UFRJ)

Este projeto consiste em uma aplicação web desenvolvida em Python utilizando o framework Streamlit. O objetivo é gerenciar o cadastro de projetos e o agendamento de equipamentos em laboratórios multiusuários de pesquisa, com configuração específica para a plataforma de genômica do LIDDER (UG-NEEDIER).

A ferramenta substitui formulários genéricos e planilhas manuais, oferecendo uma interface profissional, validação de regras de negócio (ex: obrigatoriedade de Controle de Qualidade para sequenciamento) e integração automática com o Google Sheets.

🎯 Funcionalidades Principais

Portal Institucional: Exibe informações sobre a unidade, regimento interno, normas de biossegurança e lista de equipamentos, mantendo a identidade visual da UFRJ.

Cadastro de Projetos (PI): Formulário exclusivo para Investigadores Principais, coletando dados de fomento (Faperj/CNPq/Finep) essenciais para relatórios institucionais.

Agendamento Inteligente:

Vincula o agendamento a um projeto previamente cadastrado.

Trava de Segurança: Impede o agendamento do NextSeq 1000 se o usuário não anexar o laudo de Controle de Qualidade (QC).

Biossegurança: Alertas automáticos para amostras de risco biológico (NB3).

Banco de Dados em Nuvem: Todos os dados são salvos instantaneamente em uma planilha do Google Sheets via API, sem necessidade de servidores complexos.

🛠️ Tecnologias Utilizadas

As dependências do projeto são leves e focadas em processamento de dados e requisições web:

Streamlit: Framework para criação da interface web interativa.

Pandas: Manipulação de dados e leitura das planilhas de projetos.

Requests: Comunicação HTTP para envio dos dados ao Google Apps Script.

🚀 Como Executar o Projeto

1. Instalação

Certifique-se de ter o Python instalado. Clone este repositório e instale as dependências listadas no arquivo requirements.txt:

pip install -r requirements.txt


2. Configuração (Segredos)

O sistema depende de uma conexão com o Google Sheets. Para rodar localmente ou na nuvem, configure os segredos do Streamlit (arquivo .streamlit/secrets.toml):

LINK_MAGICO = "Sua_URL_do_Google_Apps_Script"
ID_PLANILHA = "Seu_ID_da_Planilha_Google"


3. Execução

Rode o comando abaixo na raiz do projeto:

streamlit run app.py


♻️ Guia de Reuso (Adaptação para Outros Laboratórios)

Este código é Open Source e foi desenhado para ser facilmente adaptado por outras unidades da UFRJ (Microscopia, Proteômica, Citometria, etc.).

Passo 1: Configurar o "Backend" (Google Sheets)

Crie uma nova planilha no Google Sheets com duas abas: Projetos e Agendamentos.

Vá em Extensões > Apps Script.

Cole o script de recepção (doPost) que salva os dados na linha.

Implante como App da Web (Acesso: "Qualquer pessoa") e copie a URL gerada.

Passo 2: Personalizar o Código (app.py)

No arquivo app.py, você pode alterar facilmente:

Identidade Visual: Atualize a variável LOGO_UFRJ_URL ou insira o logo da sua unidade.

Equipamentos: Localize a lista equip_lista e substitua pelos equipamentos do seu laboratório:

equip_lista = [
    "Microscópio Eletrônico",
    "Citômetro de Fluxo",
    "Outros"
]


Regras: Remova ou ajuste as travas de QC (is_nextseq) caso seus equipamentos não exijam controle de qualidade prévio.

🔒 Segurança

Proteção de Credenciais: O sistema utiliza st.secrets para gerenciar links sensíveis, evitando que URLs de edição fiquem expostas no código-fonte público.

Integridade: O Google Apps Script atua como um porteiro, permitindo apenas a inserção de novos dados (append), protegendo o histórico da planilha contra deleções acidentais via API.

Desenvolvido para fortalecer a infraestrutura de pesquisa da UFRJ.
