import streamlit as st
import unicodedata
import time

# 1. BASE DE DADOS COMPLETA (Todas as 26 combinações possíveis entre os 5 reagentes)
MISTURAS_CADASTRADAS = {
    # ==========================================
    # COMBINAÇÕES DE 2 PRODUTOS (10 no total)
    # ==========================================
    "azulimbicarbonato": {
        "perigo": "ATENÇÃO",
        "alerta": "Em algumas formulações, os componentes podem interagir sem produzir gás visível imediato. Porém, a mistura altera as propriedades dos produtos, reduz a eficácia de limpeza e pode causar irritação.",
        "video": "videos/azulim_bicarbonato.mp4"
    },
    "azulimcandida": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Azulim contém componentes ácidos ou amoniacais que, ao reagir com a Cândida (hipoclorito), liberam Gás Cloro ou Cloraminas tóxicas. Risco grave de sufocamento e lesão pulmonar."
    },
    "azulimox": {
        "perigo": "ATENÇÃO",
        "alerta": "Mistura instável. A oxidação acelerada dos tensoativos do limpador pesado pelo peróxido de hidrogênio pode liberar calor e vapores irritantes às mucosas."
    },
    "azulimvinagre": {
        "perigo": "ATENÇÃO",
        "alerta": "Combinação ácida/reativa. Não gera gases letais imediatos na maioria das versões, mas intensifica a evaporação de compostos voláteis irritantes para os olhos e vias aéreas."
    },
    "bicarbonatocandida": {
        "perigo": "SEGURO",
        "alerta": "O bicarbonato não libera gás cloro por si só ao ser misturado com a água sanitária. Contudo, a alteração de pH desestabiliza o hipoclorito, reduzindo seu poder desinfetante.",
        "video": "videos/bicarbonato_candida.mp4"
    },
    "bicarbonatoox": {
        "perigo": "SEGURO",
        "alerta": "SEGURO: Promove efervescência leve de oxigênio gasoso. Mistura alcalina oxidante frequentemente usada para remoção física de manchas em superfícies e tecidos."
    },
    "bicarbonatovinagre": {
        "perigo": "ATENÇÃO",
        "alerta": "Efervescência imediata (efeito vulcão) com liberação de Dióxido de Carbono (CO2). Os produtos se neutralizam formando acetato de sódio. Em frasco fechado, pode estourar por pressão."
    },
    "candidaox": {
        "perigo": "ALTO",
        "alerta": "PERIGO: Intensa reação de óxido-redução com liberação violenta de gás oxigênio e aquecimento (reação exotérmica). Pode projetar líquidos corrosivos e estourar recipientes."
    },
    "candidavinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: O ácido acético reage com o hipoclorito de sódio liberando Gás Cloro (Cl2). Gás altamente tóxico, asfixiante e corrosivo para todo o trato respiratório."
    },
    "oxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO: A reação entre peróxido de hidrogênio e ácido acético sintetiza Ácido Peracético. Substância altamente corrosiva que causa queimaduras químicas na pele, olhos e pulmões."
    },

    # ==========================================
    # COMBINAÇÕES DE 3 PRODUTOS (10 no total)
    # ==========================================
    "azulimbicarbonatocandida": {
        "perigo": "ALTO",
        "alerta": "PERIGO: A presença do bicarbonato não impede que os componentes reativos do Azulim desestabilizem a Cândida. Há risco severo de formação de vapores clorados tóxicos e espuma."
    },
    "azulimbicarbonatoox": {
        "perigo": "ATENÇÃO",
        "alerta": "Reação efervescente instável. Ocorre decomposição rápida da água oxigenada somada à neutralização parcial do limpador, gerando espuma densa, calor leve e vapores irritantes."
    },
    "azulimbicarbonatovinagre": {
        "perigo": "ATENÇÃO",
        "alerta": "Intensa formação de espuma e liberação de gás carbônico (CO2) pelo choque entre os ácidos e o bicarbonato. Transborda facilmente e espalha vapores ácidos irritantes."
    },
    "azulimcandidaox": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Reação vigorosa e exotérmica! Ocorre liberação simultânea de gás cloro/cloraminas tóxicas e gás oxigênio em alta velocidade, projetando gotículas corrosivas."
    },
    "azulimcandidavinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO LETAL: Dupla acidificação sobre o hipoclorito da Cândida. Acelera drasticamente o desprendimento de nuvens densas de Gás Cloro (Cl2). Risco imediato de asfixia química."
    },
    "azulimoxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO: Meio altamente ácido e oxidante que promove a síntese de Ácido Peracético combinada aos solventes do Azulim. Vapores fortemente corrosivos para olhos e vias respiratórias."
    },
    "bicarbonatocandidaox": {
        "perigo": "ALTO",
        "alerta": "PERIGO: Efervescência violenta pela reação entre o hipoclorito e o peróxido de hidrogênio. O bicarbonato intensifica a formação de espuma alcalina corrosiva com aquecimento do frasco."
    },
    "bicarbonatocandidavinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Embora o bicarbonato reaja com parte do vinagre gerando CO2, o ácido residual ataca a Cândida e libera Gás Cloro tóxico misturado às bolhas da espuma."
    },
    "bicarbonatooxvinagre": {
        "perigo": "ALTO",
        "alerta": "Reação complexa com liberação expressiva de gás carbônico (CO2) e formação concomitante de compostos oxidantes corrosivos (Ácido Peracético). Efervescência intensa com risco de respingos.",
        "video": "videos/ox_vinagre_bicarbonato.mp4"
    },
    "candidaoxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Reação tripla agressiva! Libera Gás Cloro tóxico, Oxigênio sob pressão e sintetiza Ácido Peracético. Altamente exotérmica, corrosiva e asfixiante."
    },

    # ==========================================
    # COMBINAÇÕES DE 4 PRODUTOS (5 no total)
    # ==========================================
    "azulimbicarbonatocandidaox": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Mistura oxidante e alcalino-clorada altamente instável. Gera aquecimento rápido, espuma abundante com risco de transbordamento e liberação de gases clorados irritantes."
    },
    "azulimbicarbonatocandidavinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Intensa expansão gasosa de CO2 combinada com liberação de Gás Cloro (Cl2) e Cloraminas. A espuma retém bolhas de gás tóxico que estouram liberando vapores sufocantes."
    },
    "azulimbicarbonatooxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO: Forte reação efervescente com síntese de Ácido Peracético e liberação massiva de CO2. Gera pressão elevada em recipientes fechados e espalha aerossóis ácidos corrosivos."
    },
    "azulimcandidaoxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO EXTREMO: Mistura líquida sem neutralizante alcalino. Dependendo dos ingredientes presentes nos produtos industriais, há desprendimento imediato de gases tóxicos e corrosivos. Nunca misture!",
        "video": "videos/todos_sem_bicarbonato.mp4"
    },
    "bicarbonatocandidaoxvinagre": {
        "perigo": "ALTO",
        "alerta": "PERIGO CRÍTICO: Reação vigorosa de múltiplos estágios. Libera simultaneamente CO2, Oxigênio e Gás Cloro tóxico, além de formar compostos peracéticos. Altíssimo risco de projeção química."
    },

    # ==========================================
    # COMBINAÇÃO DE 5 PRODUTOS (1 no total)
    # ==========================================
    "azulimbicarbonatocandidaoxvinagre": {
        "perigo": "ALTO",
        "alerta": "☢️ PERIGO CRÍTICO E EXPLOSIVO: Mistura de todos os reagentes! Ocorrem reações múltiplas, exotérmicas e descontroladas, gerando grande volume de gases tóxicos sob pressão (Cl2, CO2, O2) e ácidos corrosivos. Risco iminente de explosão em frascos fechados!",
        "video": "videos/todos_juntos.mp4"
    }
}

# 2. DICIONÁRIO EXPLICATIVO
DICIONARIO = {
    "Azulim": "Limpador desincrustante concentrado. Dependendo da formulação, pode conter ácidos inorgânicos ou tensoativos amoniacais altamente reativos.",
    "Bicarbonato": "Bicarbonato de Sódio (NaHCO3). Composto básico/alcalino fraco que atua liberando gás carbônico (CO2) ao entrar em contato com substâncias ácidas.",
    "Cândida": "Solução aquosa de Hipoclorito de Sódio (NaClO). Agente desinfetante e oxidante com facilidade de liberar Gás Cloro tóxico sob meio ácido.",
    "Ox": "Água Oxigenada ou Peróxido de Hidrogênio (H2O2). Poderoso oxidante que se decompõe liberando oxigênio molecular e calor.",
    "Vinagre": "Solução comercial com cerca de 4% a 5% de Ácido Acético (CH3COOH). Reduz expressivamente o pH e desestabiliza compostos clorados."
}

def normalizar_texto(texto):
    texto = texto.strip().lower()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def analisar_multiplas_misturas(lista_produtos):
    produtos_normalizados = [normalizar_texto(p) for p in lista_produtos]
    produtos_ordenados = sorted(produtos_normalizados)
    chave_busca = "".join(produtos_ordenados)
    
    if chave_busca in MISTURAS_CADASTRADAS:
        resultado = MISTURAS_CADASTRADAS[chave_busca]
        return resultado["perigo"], resultado["alerta"], resultado.get("video")
    else:
        return "DESCONHECIDO", "Combinação não encontrada.", None

# 3. CONFIGURAÇÃO DA PÁGINA E ESTADO DE NAVEGAÇÃO
st.set_page_config(page_title="Alerta Químico", page_icon="🧪", layout="wide")

opcoes_produtos = ["Azulim", "Bicarbonato", "Cândida", "Ox", "Vinagre"]

# Inicializa o controle de tela ("selecao" ou "resultado")
if "tela_atual" not in st.session_state:
    st.session_state["tela_atual"] = "selecao"
if "selecionados_salvos" not in st.session_state:
    st.session_state["selecionados_salvos"] = []

def limpar_selecoes():
    for p in opcoes_produtos:
        st.session_state[f"chk_{p}"] = False

def voltar_para_inicio():
    limpar_selecoes()
    st.session_state["selecionados_salvos"] = []
    st.session_state["tela_atual"] = "selecao"

# Barra Lateral Fixa (Mini-Dicionário)
with st.sidebar:
    st.header("📚 Dicionário Químico")
    st.markdown("Consulte a base de reagentes avaliados:")
    for produto, descricao in DICIONARIO.items():
        with st.expander(produto):
            st.write(descricao)
    st.divider()
    st.caption("Protótipo interativo desenvolvido para a Feira de Ciências.")

# Cabeçalho Principal
st.title("🧪 Simulador de Reações Químicas")

# ==========================================
# TELA 1: SELEÇÃO DE PRODUTOS
# ==========================================
if st.session_state["tela_atual"] == "selecao":
    st.markdown("Selecione **2 ou mais produtos** marcando as caixas abaixo para testar a mistura. **Química exige responsabilidade!**")
    st.divider()

    cols = st.columns(len(opcoes_produtos))
    ingredientes_atuais = []

    for i, produto in enumerate(opcoes_produtos):
        with cols[i]:
            if f"chk_{produto}" not in st.session_state:
                st.session_state[f"chk_{produto}"] = False
                
            marcado = st.checkbox(produto, key=f"chk_{produto}")
            if marcado:
                ingredientes_atuais.append(produto)

    st.divider()

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        executar = st.button("🔬 Simular Reação", type="primary", use_container_width=True)
    with col_btn2:
        st.button("Limpar Seleções", on_click=limpar_selecoes, use_container_width=True)

    if executar:
        if len(ingredientes_atuais) < 2:
            st.warning("⚠️ Selecione pelo menos **2 reagentes** para simular uma reação química!")
        else:
            with st.spinner("Processando reatividade molecular no laboratório virtual..."):
                time.sleep(1.5)
            # Salva os itens escolhidos, muda a tela para "resultado" e recarrega a interface
            st.session_state["selecionados_salvos"] = ingredientes_atuais
            st.session_state["tela_atual"] = "resultado"
            st.rerun()

# ==========================================
# TELA 2: EXIBIÇÃO DO RESULTADO E VÍDEO
# ==========================================
elif st.session_state["tela_atual"] == "resultado":
    escolhidos = st.session_state["selecionados_salvos"]
    
    st.markdown(f"### 🧪 Mistura Analisada: **{' + '.join(escolhidos)}**")
    st.divider()

    nivel_perigo, mensagem, caminho_video = analisar_multiplas_misturas(escolhidos)

    if nivel_perigo == "SEGURO":
        st.success(f"**NÍVEL SEGURO:** {mensagem}")
    elif nivel_perigo == "ALTO":
        st.error(f"**RISCO ELEVADO:** {mensagem}")
    else:
        st.warning(f"**ATENÇÃO:** {mensagem}")

    # Se houver vídeo para essa mistura, exibe centralizado
    if caminho_video:
        st.markdown("#### 🎥 Registro Prático do Experimento:")
        col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
        with col_v2:
            st.video(caminho_video)

    st.divider()
    
    # Botão único de retorno que limpa os dados e volta para a Tela 1
    st.button("🔄 Nova Simulação", type="primary", on_click=voltar_para_inicio, use_container_width=True)