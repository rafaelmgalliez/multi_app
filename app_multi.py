import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time

# ==============================================================================
# CONFIGURAÇÕES E SEGREDOS
# ==============================================================================
# Tenta carregar dos Secrets (Nuvem), senão fica vazio para teste local
try:
    LINK_MAGICO_SCRIPT = st.secrets["LINK_MAGICO"]
    ID_PLANILHA = st.secrets["ID_PLANILHA"]
except:
    LINK_MAGICO_SCRIPT = "" 
    ID_PLANILHA = ""

# URL para ler os dados (CSV Público do Google Sheets)
URL_CSV_PROJETOS = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/gviz/tq?tqx=out:csv&sheet=Projetos"

# Logo Oficial UFRJ (Versão Negativa/Branca)
LOGO_UFRJ_URL = "https://needier.ufrj.br/wp-content/themes/arion/assets/images/ufrj-horizontal-simplificada-negativa.png"

# ==============================================================================
# FUNÇÕES DE BACKEND (Conexão Google Sheets)
# ==============================================================================
def salvar_no_google(aba, dados_lista):
    """Envia dados para o Google Apps Script via HTTP POST"""
    if not LINK_MAGICO_SCRIPT:
        st.error("Erro de Configuração: Link do Apps Script não encontrado nos Secrets.")
        return False
        
    payload = {"aba": aba, "dados": dados_lista}
    try:
        response = requests.post(LINK_MAGICO_SCRIPT, json=payload)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Erro ao salvar na nuvem: {response.text}")
            return False
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return False

def carregar_projetos():
    """Lê a planilha de Projetos para preencher o dropdown de agendamento"""
    try:
        if not ID_PLANILHA: return []
        df = pd.read_csv(URL_CSV_PROJETOS)
        if df.empty: return []
        return df.to_dict('records')
    except:
        return []

# ==============================================================================
# INTERFACE GRÁFICA (FRONTEND)
# ==============================================================================
st.set_page_config(page_title="LIDDER / UG-NEEDIER", page_icon="🧬", layout="wide")

# CSS Personalizado (Identidade Visual UFRJ)
st.markdown("""
    <style>
    /* Cabeçalhos */
    .main-header { font-size: 2.5rem; color: #003366; text-align: center; font-weight: 800; margin-top: 10px; }
    .sub-header { text-align: center; color: #444; font-size: 1.2rem; font-weight: 500; margin-bottom: 5px; }
    
    /* Links Oficiais */
    .official-link { text-align: center; margin-bottom: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 10px; border: 1px solid #ddd; }
    .official-link a { text-decoration: none; color: #003366; font-weight: bold; font-size: 1.1rem; margin: 0 15px; }
    .official-link a:hover { color: #d6001c; text-decoration: underline; }
    
    /* Títulos de Seção */
    .section-title { font-size: 1.3rem; font-weight: bold; color: #003366; margin-top: 20px; border-bottom: 3px solid #d6001c; padding-bottom: 5px; }
    
    /* Caixas de Aviso */
    .warning-box { background-color: #eef6fc; padding: 15px; border-radius: 8px; border-left: 6px solid #003366; margin-bottom: 20px; color: #2c3e50; }
    .warning-box a { color: #d6001c; font-weight: bold; text-decoration: underline; }
    
    /* Ajuste da Logo UFRJ (Fundo azul para imagem negativa) */
    div[data-testid="stImage"] > img { 
        max-height: 80px; 
        object-fit: contain; 
        background-color: #003366; /* Azul UFRJ para dar contraste na logo branca */
        padding: 10px; 
        border-radius: 8px; 
    }
    div[data-testid="stImage"] { display: flex; justify-content: center; align-items: center; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
col_logo, col_title, col_empty = st.columns([1, 4, 1])

with col_logo:
    try:
        st.image("logo_ufrj.png", use_container_width=True)
    except:
        st.image(LOGO_UFRJ_URL, use_container_width=True)

with col_title:
    st.markdown('<div class="main-header">LIDDER / UG-NEEDIER</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Núcleo de Enfrentamento e Estudos de Doenças Infecciosas Emergentes e Reemergentes</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Universidade Federal do Rio de Janeiro</div>', unsafe_allow_html=True)

# --- BARRA DE LINKS ---
st.markdown("""
    <div class="official-link">
        🌐 <a href="https://needier.ufrj.br/" target="_blank">Site Oficial do NEEDIER</a>
        <span style="color: #ccc;">|</span>
        <a href="https://pnipe.mcti.gov.br/laboratory/8559" target="_blank" style="font-size: 0.9rem; color: #666;">Cadastro PNIPE/MCTI</a>
    </div>
""", unsafe_allow_html=True)

# --- ABAS DE NAVEGAÇÃO ---
tab1, tab2, tab3 = st.tabs(["🏛️ A Unidade", "📝 Cadastro de Projeto (PI)", "📅 Agendamento de Uso"])

# ==============================================================================
# ABA 1: INFO E REGRAS
# ==============================================================================
with tab1:
    col_info1, col_info2 = st.columns([1.5, 1])
    with col_info1:
        st.markdown('<div class="section-title">Sobre a Infraestrutura</div>', unsafe_allow_html=True)
        st.write("""
        O **LIDDER (Laboratório de Investigação Diagnóstica de Doenças Infecciosas Emergentes e Reemergentes)** é uma unidade estratégica da UFRJ, dedicada à vigilância genômica, diagnóstico molecular avançado e pesquisa 
        em patógenos de alto risco.
        """)
        
        # Link do Regimento Atualizado aqui
        st.markdown('<div class="warning-box">⚠️ <b>Normas de Acesso (<a href="https://needier.ufrj.br/?page_id=70" target="_blank">Ler Regimento Interno</a>):</b><br>'
                    '1. <b>Cadastro Obrigatório:</b> O uso da plataforma é exclusivo para projetos cadastrados pelo Investigador Principal (PI).<br>'
                    '2. <b>Sequenciamento:</b> O agendamento do <b>Illumina NextSeq 1000</b> requer, obrigatoriamente, o envio do laudo de Controle de Qualidade (TapeStation/Qubit).<br>'
                    '3. <b>Dados:</b> A unidade não realiza armazenamento de longo prazo. O backup dos dados brutos é responsabilidade imediata do usuário.<br>'
                    '4. <b>Biossegurança:</b> O respeito às normas NB2/NB3 é mandatório.</div>', unsafe_allow_html=True)

    with col_info2:
        st.markdown('<div class="section-title">Equipamentos Disponíveis</div>', unsafe_allow_html=True)
        st.info("""
        **Sequenciamento de Nova Geração**
        * Illumina NextSeq 1000
        
        **Preparo de Amostras & QC**
        * TapeStation System Agilent 4200
        * BluePippin Instrument (Sage Science)
        """)
        st.markdown("Para mais detalhes técnicos, consulte o [Site do NEEDIER](https://needier.ufrj.br/).")

# ==============================================================================
# ABA 2: CADASTRO DE PROJETO (PI)
# ==============================================================================
with tab2:
    st.markdown('<div class="section-title">Cadastro do Investigador Principal (PI)</div>', unsafe_allow_html=True)
    st.caption("Preenchimento único por vigência do projeto. Necessário para relatórios do MCTI/Finep.")

    with st.form("form_cadastro_completo"):
        c1, c2 = st.columns(2)
        with c1:
            coord_nome = st.text_input("Nome Completo do Coordenador (PI)*")
            coord_email = st.text_input("E-mail Institucional*")
            coord_lattes = st.text_input("Link do Currículo Lattes*")
        
        with c2:
            inst_opcoes = ["UFRJ - CCS", "UFRJ - Outros Centros", "Fiocruz", "INCA", "LNCC", "Outra ICT", "Empresa Privada", "Outros"]
            coord_inst = st.selectbox("Instituição de Vínculo*", inst_opcoes)
            inst_extra = ""
            if coord_inst in ["Outra ICT", "Empresa Privada", "Outros", "UFRJ - Outros Centros"]:
                inst_extra = st.text_input("Qual Instituição/Empresa/Centro?")

        st.markdown('<div class="section-title">Detalhes do Projeto</div>', unsafe_allow_html=True)
        proj_titulo = st.text_input("Título do Projeto*", help="Este será o nome usado para agendamentos futuros.")
        
        c3, c4 = st.columns(2)
        with c3:
            fomento_opcoes = ["FAPERJ", "CNPq", "CAPES", "FINEP", "Ministério da Saúde", "Emenda Parlamentar", "Recursos Próprios", "Outro"]
            proj_fomento = st.multiselect("Agência(s) de Fomento*", fomento_opcoes)
            fomento_outro = ""
            if "Outro" in proj_fomento:
                fomento_outro = st.text_input("Especifique a outra fonte de fomento:")

        with c4:
            area_opcoes = ["Doenças Infecciosas", "Virologia", "Bacteriologia", "Genética Humana", "Imunologia", "Biotecnologia", "Diagnóstico", "Outra"]
            proj_area = st.multiselect("Área de Conhecimento*", area_opcoes)
            area_outro = ""
            if "Outra" in proj_area:
                 area_outro = st.text_input("Especifique a outra área:")

        proj_resumo = st.text_area("Resumo do Projeto e Justificativa de Uso*", max_chars=1000)

        st.markdown("---")
        proj_nb3 = st.checkbox("Este projeto envolve manipulação de patógenos de Risco 3?")
        termo_aceite = st.checkbox("Declaro que as informações são verdadeiras e concordo com o Regimento Interno do LIDDER/NEEDIER.")

        btn_cadastrar = st.form_submit_button("Cadastrar Projeto", type="primary")

        if btn_cadastrar:
            if not coord_nome or not coord_email or not proj_titulo or not proj_fomento or not termo_aceite:
                st.error("❌ Por favor, preencha todos os campos obrigatórios.")
            else:
                # Formata campos "Outros"
                inst_final = f"{coord_inst}: {inst_extra}" if inst_extra else coord_inst
                fomento_final = ", ".join(proj_fomento)
                if fomento_outro: fomento_final += f" ({fomento_outro})"
                area_final = ", ".join(proj_area)
                if area_outro: area_final += f" ({area_outro})"

                dados_projeto = [
                    str(datetime.now()), coord_nome, coord_email, proj_titulo, 
                    inst_final, fomento_final, area_final, 
                    "SIM" if proj_nb3 else "NÃO", coord_lattes, proj_resumo
                ]
                
                if salvar_no_google("Projetos", dados_projeto):
                    st.success(f"✅ Projeto '{proj_titulo}' cadastrado com sucesso!")
                    st.balloons()
                    st.cache_data.clear() # Atualiza cache para dropdown

# ==============================================================================
# ABA 3: AGENDAMENTO DETALHADO
# ==============================================================================
with tab3:
    st.markdown('<div class="section-title">Solicitação de Uso e Serviços</div>', unsafe_allow_html=True)
    
    # Carrega lista de projetos
    lista_db = carregar_projetos()
    opcoes_projetos = [item['Projeto'] for item in lista_db if 'Projeto' in item] if lista_db else []
    
    if not opcoes_projetos:
        st.warning("⚠️ Nenhum projeto encontrado no sistema. Realize o cadastro na aba anterior primeiro.")
        opcoes_projetos = ["---"]

    with st.form("form_agendamento_detalhado"):
        st.markdown("**1. Identificação do Usuário**")
        c_user1, c_user2 = st.columns(2)
        with c_user1:
            user_nome = st.text_input("Nome do Usuário (Quem vai usar)*")
            user_email = st.text_input("E-mail do Usuário*", help="Para envio de confirmação")
            user_lab = st.text_input("Laboratório de Origem*")
        with c_user2:
            proj_selecionado = st.selectbox("Projeto Vinculado (PI)*", opcoes_projetos)
            user_vinculo = st.selectbox("Vínculo Institucional*", ["Iniciação Científica", "Mestrado", "Doutorado", "Pós-Doc", "Técnico", "Docente/Pesquisador", "Outro"])
            vinculo_extra = ""
            if user_vinculo == "Outro":
                vinculo_extra = st.text_input("Qual o vínculo?")

        st.markdown("---")
        st.markdown("**2. Equipamento e Serviço**")
        c_eq1, c_eq2 = st.columns(2)
        with c_eq1:
            # Lista Oficial Restrita (Apenas os 3 solicitados)
            equip_lista = [
                "Sequenciador Illumina NextSeq 1000",
                "TapeStation System Agilent 4200",
                "BluePippin Instrument (Sage Science)"
            ]
            equip_escolha = st.selectbox("Equipamento / Plataforma*", equip_lista)

        with c_eq2:
            tipo_servico = st.radio("Tipo de Solicitação*", ["Uso Autônomo (Já sou treinado)", "Solicitação de Treinamento", "Entrega de Amostras (Serviço)"])

        st.markdown("---")
        st.markdown("**3. Detalhes da Amostra**")
        c_am1, c_am2 = st.columns(2)
        with c_am1:
            tipo_amostra = st.selectbox("Natureza da Amostra*", [
                "DNA Genômico", "RNA Total", "Biblioteca NGS Pronta", "Produto de PCR (Amplicon)", 
                "Plasmídeo", "Cultura Celular", "Soro/Plasma", "Outro"
            ])
            if tipo_amostra == "Outro":
                tipo_amostra = st.text_input("Especifique o tipo da amostra:")
            n_amostras = st.number_input("Número de Amostras", min_value=1, value=1)

        with c_am2:
            risco_bio = st.selectbox("Nível de Risco Biológico*", [
                "Risco 1 (Não Infeccioso)", "Risco 2 (Patógenos Moderados)", "Risco 3 (Alto Risco)"
            ])
            if risco_bio == "Risco 3 (Alto Risco)":
                st.warning("⚠️ Atenção: Amostras de Risco 3 requerem procedimentos específicos de biossegurança.")

        st.markdown("---")
        st.markdown("**4. Data e Controle de Qualidade**")
        c_date1, c_date2, c_date3 = st.columns(3)
        with c_date1: date_req = st.date_input("Data Pretendida*")
        with c_date2: time_ini = st.time_input("Horário Início*", value=time(9,0))
        with c_date3: time_fim = st.time_input("Horário Término*", value=time(13,0))

        # Lógica de QC para NextSeq
        is_nextseq = "NextSeq 1000" in equip_escolha
        msg_qc = "Upload do Laudo de QC (TapeStation/Qubit) *" if is_nextseq else "Upload de QC (Opcional)"
        
        qc_file = st.file_uploader(msg_qc, type=['pdf', 'jpg', 'png'], help="Obrigatório para NextSeq.")
        
        obs_geral = st.text_area("Observações Adicionais")
        termos_uso = st.checkbox("Declaro que cumprirei as normas de biossegurança e limpeza da unidade.")
        
        btn_agendar = st.form_submit_button("Enviar Solicitação", type="primary")

        if btn_agendar:
            if proj_selecionado == "---":
                st.error("Selecione um projeto válido.")
            elif not user_nome or not user_email or not user_lab:
                st.error("Preencha a identificação completa do usuário.")
            elif is_nextseq and not qc_file:
                st.error("🚫 Bloqueio: Para uso do NextSeq 1000, o laudo de Controle de Qualidade é OBRIGATÓRIO.")
            elif not termos_uso:
                st.error("Você precisa aceitar os termos de uso.")
            else:
                qc_status = "Enviado" if qc_file else "Não Enviado"
                vinculo_final = f"{user_vinculo}: {vinculo_extra}" if vinculo_extra else user_vinculo
                
                dados_agenda = [
                    str(datetime.now()), str(date_req), f"{time_ini} - {time_fim}",
                    user_nome, vinculo_final, user_lab, user_email,
                    equip_escolha, proj_selecionado, tipo_servico,
                    tipo_amostra, risco_bio, qc_status, obs_geral
                ]

                if salvar_no_google("Agendamentos", dados_agenda):
                    st.success("✅ Solicitação enviada com sucesso! Aguarde a confirmação por e-mail.")
