import streamlit as st
import unicodedata
import time

# 1. BASE DE DADOS COMPLETA (Todas as duplas + experimentos múltiplos)
MISTURAS_CADASTRADAS = {
    # --- COMBINAÇÕES DE 2 PRODUTOS (10 no total) ---
    "azulimbicarbonato": {
        "perigo": "ATENÇÃO",
        "alerta": "Reação de neutralização. Pode liberar gases e espuma. Um produto neutraliza a ação do outro, desperdiçando a aplicação.",
        "video": "videos/azulim_bicarbonato.mp4"
    },
    "azulimcandida": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Azulim contém ácidos ou compostos amoniacais. Ao reagir com a Cândida (hipoclorito), libera Gás Cloro ou Cloramina. Altamente tóxico e asfixiante."
    },
    "azulimox": {
        "perigo": "ATENÇÃO",
        "alerta": "Mistura imprevisível e instável. A oxidação rápida de limpadores pesados pode gerar liberação de calor e vapores irritantes."
    },
    "azulimvinagre": {
        "perigo": "ATENÇÃO",
        "alerta": "Mistura de soluções ácidas. Não gera gases letais de imediato, mas intensifica o cheiro forte e potencializa irritação na pele e nos olhos."
    },
    "bicarbonatocandida": {
        "perigo": "SEGURO",
        "alerta": "Não gera gases nocivos, mas o bicarbonato reduz a eficácia antimicrobiana da cândida.",
        "video": "videos/bicarbonato_candida.mp4"
    },
    "bicarbonatoox": {
        "perigo": "SEGURO",
        "alerta": "SEGURO: Gera efervescência de oxigênio mecânico. Muito usado em receitas caseiras para desengordurar e alvejar tecidos."
    },
    "bicarbonatovinagre": {
        "perigo": "ATENÇÃO",
        "alerta": "Reação clássica de efervescência (efeito vulcão). Libera grande quantidade de Gás Carbônico (CO2). Em frascos lacrados, pode estourar pela pressão."
    },
    "candidaox": {
        "perigo": "ALTO",
        "alerta": "PERIGO: Reação vigorosa de óxido-redução. Libera oxigênio gasoso em alta velocidade com geração de calor. Risco de romper recipientes."
    },
    "candidavinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: O ácido acético desestabiliza o hipoclorito, liberando Gás Cloro (Cl2). Causa tosse, sensação de queimação pulmonar e risco de asfixia."
    },
    "oxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO: A junção gera Ácido Peracético. Trata-se de um composto altamente corrosivo que provoca queimaduras químicas em mucosas e olhos."
    },

    # --- EXPERIMENTOS MÚLTIPLOS DOS VÍDEOS ---
    "bicarbonatooxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO: Efervescência imediata combinada com a síntese de Ácido Peracético. Vapores irritantes e risco de projeção nos olhos.",
        "video": "videos/ox_vinagre_bicarbonato.mp4"
    },
    "azulimcandidaoxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Combinação crítica sem agente neutralizante. Síntese maciça de Gás Cloro e vapores corrosivos com risco de colapso respiratório.",
        "video": "videos/todos_sem_bicarbonato.mp4"
    },
    "azulimbicarbonatocandidaoxvinagre": {
        "perigo": "ALTO",
        "alerta": "☢️ PERIGO CRÍTICO E EXPLOSIVO: Coquetel completo. Combina formação de gases asfixiantes com expansão súbita de CO2. Risco iminente de explosão em frascos vedados.",
        "video": "videos/todos_juntos.mp4"
    }
}

# 2. DICIONÁRIO EXPLICATIVO
DICIONARIO = {
    "Azulim": "Limpador desincrustante concentrado. Dependendo da formulação, pode conter ácidos inorgânicos ou tensoativos fortes altamente reativos.",
    "Bicarbonato": "Bicarbonato de Sódio (NaHCO3). Composto básico/alcalino fraco que atua liberando CO2 ao entrar em contato com substâncias ácidas.",
    "Cândida": "Solução aquosa de Hipoclorito de Sódio (NaClO). Agente desinfetante e oxidante com facilidade de liberar gases tóxicos sob pH ácido.",
    "Ox": "Água Oxigenada ou Peróxido de Hidrogênio (H2O2). Poderoso oxidante que se decompõe em água e oxigênio molecular na presença de catalisadores.",
    "Vinagre": "Solução comercial com cerca de 4% a 5% de Ácido Acético (CH3COOH). Reduz expressivamente o pH das soluções onde é introduzido."
}

def normalizar_texto(texto):
    texto = texto.strip().lower()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def analisar_multiplas_misturas(lista_produtos):
    if len(lista_produtos) < 2:
        return "AVISO", "Selecione ao menos 2 reagentes para simular a reação.", None
    
    produtos_normalizados = [normalizar_texto(p) for p in lista_produtos]
    produtos_ordenados = sorted(produtos_normalizados)
    chave_busca = "".join(produtos_ordenados)
    
    if chave_busca in MISTURAS_CADASTRADAS:
        resultado = MISTURAS_CADASTRADAS[chave_busca]
        return resultado["perigo"], resultado["alerta"], resultado.get("video")
    else:
        return "DESCONHECIDO", "Esta combinação específica não possui dados empíricos registrados no laboratório virtual.", None

# 3. INTERFACE VISUAL
st.set_page_config(page_title="Alerta Químico", page_icon="🧪", layout="wide")

with st.sidebar:
    st.header("📚 Dicionário Químico")
    st.markdown("Consulte a base de reagentes avaliados:")
    for produto, descricao in DICIONARIO.items():
        with st.expander(produto):
            st.write(descricao)
    st.divider()
    st.caption("Protótipo interativo desenvolvido para a Feira de Ciências.")

st.title("🧪 Simulador de Reações Químicas")
st.markdown("Selecione os produtos marcando as caixas abaixo para testar a mistura. **Química exige responsabilidade!**")
st.divider()

# Lista de opções
opcoes_produtos = ["Azulim", "Bicarbonato", "Cândida", "Ox", "Vinagre"]

# Função auxiliar para desmarcar todos os checkboxes
def limpar_selecoes():
    for p in opcoes_produtos:
        st.session_state[f"chk_{p}"] = False

# Distribui os produtos em 5 colunas horizontais
cols = st.columns(len(opcoes_produtos))
ingredientes_selecionados = []

for i, produto in enumerate(opcoes_produtos):
    with cols[i]:
        # Inicializa o estado de cada checkbox se ainda não existir
        if f"chk_{produto}" not in st.session_state:
            st.session_state[f"chk_{produto}"] = False
            
        marcado = st.checkbox(produto, key=f"chk_{produto}")
        if marcado:
            ingredientes_selecionados.append(produto)

st.divider()

# Botões de ação lado a lado
col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    executar = st.button("🔬 Simular Reação", type="primary", use_container_width=True)

with col_btn2:
    st.button("Limpar Seleções", on_click=limpar_selecoes, use_container_width=True)

if executar:
    with st.spinner("Processando reatividade no laboratório virtual..."):
        time.sleep(1.8)
    
    nivel_perigo, mensagem, caminho_video = analisar_multiplas_misturas(ingredientes_selecionados)
    
    if nivel_perigo == "AVISO":
        st.info(mensagem)
    elif nivel_perigo == "SEGURO":
        st.success(mensagem)
        if caminho_video:
            st.markdown("#### Registro do Experimento:")
            col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
            with col_v2:
                st.video(caminho_video)
    elif nivel_perigo == "ALTO":
        st.error(mensagem)
        if caminho_video:
            st.markdown("#### Registro do Experimento:")
            col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
            with col_v2:
                st.video(caminho_video)
    else:
        st.warning(mensagem)