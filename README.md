🧬 Sistema de Gestão Multiusuário - LIDDER/UG-NEEDIER (UFRJ)
​Bem-vindo ao repositório oficial da aplicação de gestão da Unidade de Genómica do LIDDER (Laboratório de Investigação Diagnóstica de Doenças Infecciosas Emergentes e Reemergentes) da UFRJ.
​Esta ferramenta foi desenvolvida para digitalizar, organizar e gerir o fluxo de trabalho da plataforma multiusuário, substituindo formulários em papel e trocas de e-mail por uma interface web centralizada e integrada à nuvem.
​🎯 Objetivos e Funcionalidades
​O sistema atua como um portal único para investigadores e alunos, oferecendo:
​🏛️ Portal Institucional:
​Apresentação das normas de funcionamento e biossegurança.
​Lista atualizada de equipamentos disponíveis (NextSeq 1000, TapeStation, etc.).
​Links diretos para o registo no PNIPE/MCTI.
​📝 Cadastro de Projetos (Investigadores Principais):
​Registo obrigatório de projetos de pesquisa.
​Recolha estruturada de fontes de financiamento (FAPERJ, CNPq, FINEP) para relatórios institucionais.
​Validação de requisitos de Biossegurança (NB2/NB3).
​📅 Calendário de Ocupação (Disponibilidade):
​Visualização em tempo real dos horários já reservados.
​Filtros dinâmicos por equipamento para evitar conflitos de agenda ("overbooking").
​🔬 Agendamento Inteligente:
​Solicitação de uso vinculada a projetos previamente aprovados.
​Trava de Segurança: Bloqueia agendamentos no sequenciador NextSeq 1000 se o utilizador não anexar o relatório de Controlo de Qualidade (QC).
​Integração direta com Google Sheets para persistência de dados.
​🏗️ Arquitetura do Sistema
​O projeto utiliza uma arquitetura Serverless leve, ideal para ambientes académicos que necessitam de baixo custo de manutenção.
​Frontend: Desenvolvido em Python com a biblioteca Streamlit.
​Backend/API: Um Web App criado com Google Apps Script que recebe requisições HTTP (POST).
​Base de Dados: Uma Folha de Cálculo Google (Google Sheets) que armazena todas as transações.
​🛠️ Instalação e Configuração
​Siga este guia para executar o projeto localmente ou para implementar uma cópia no seu laboratório.
​1. Pré-requisitos
​Python 3.8 ou superior instalado.
​Uma conta Google (para criar a folha de cálculo).
​2. Configuração da Base de Dados (Google Sheets)
​O sistema depende de uma estrutura de colunas específica para funcionar corretamente.
