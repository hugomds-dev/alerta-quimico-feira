import streamlit as st
import unicodedata

# 1. BASE DE DADOS DE REAGENTES
MISTURAS_CADASTRADAS = {
    "azulimbicarbonato": {"perigo": "ATENÇÃO", "alerta": "Reação de neutralização. Pode liberar gases e espuma. Não limpa melhor do que usar separados."},
    "azulimcandida": {"perigo": "ALTO", "alerta": "PERIGO EXTREMO: Azulim contém ácidos ou amônia. Com Cândida, libera gases altamente tóxicos (Cloro ou Cloramina). Risco severo aos pulmões."},
    "azulimox": {"perigo": "ATENÇÃO", "alerta": "Mistura imprevisível. Produtos de limpeza pesada não devem ser misturados com peróxidos. Risco de irritação."},
    "azulimvinagre": {"perigo": "ATENÇÃO", "alerta": "Mistura de ácidos. Não gera gás letal de imediato, mas não potencializa a limpeza e pode irritar a pele."},
    "bicarbonatocandida": {"perigo": "SEGURO", "alerta": "SEGURO: Não há reação tóxica, porém o bicarbonato anula o poder desinfetante da Cândida. Desperdício de produto."},
    "bicarbonatoox": {"perigo": "SEGURO", "alerta": "SEGURO: Forma uma pasta excelente para tirar manchas de tecidos e rejuntes."},
    "bicarbonatovinagre": {"perigo": "ATENÇÃO", "alerta": "Efeito Vulcão! Libera Gás Carbônico (CO2). É seguro em ambiente aberto, mas se colocado em um pote fechado, pode explodir pela pressão."},
    "candidaox": {"perigo": "ALTO", "alerta": "PERIGO: Reação violenta. Libera oxigênio gasoso rapidamente e gera calor. Se estiver num borrifador, ele pode estourar."},
    "candidavinagre": {"perigo": "ALTO", "alerta": "PERIGO EXTREMO: Libera Gás Cloro. É um gás tóxico, asfixiante e corrosivo para as vias respiratórias."},
    "oxvinagre": {"perigo": "ALTO", "alerta": "PERIGO: Forma Ácido Peracético. É altamente corrosivo, pode causar queimaduras na pele e irritação severa nos olhos e pulmões."}
}

def normalizar_texto(texto):
    texto = texto.strip().lower()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def analisar_mistura(produto_1, produto_2):
    if produto_1 == produto_2:
        return "SEGURO", "Você selecionou o mesmo produto duas vezes. Nenhuma reação."
    
    p1 = normalizar_texto(produto_1)
    p2 = normalizar_texto(produto_2)
    produtos_ordenados = sorted([p1, p2])
    chave_busca = produtos_ordenados[0] + produtos_ordenados[1]
    
    if chave_busca in MISTURAS_CADASTRADAS:
        resultado = MISTURAS_CADASTRADAS[chave_busca]
        return resultado["perigo"], resultado["alerta"]
    else:
        return "DESCONHECIDO", f"Não temos dados sobre a combinação: {produto_1} + {produto_2}."

# 2. CONFIGURAÇÃO DA INTERFACE
st.set_page_config(page_title="Alerta Químico", page_icon="🧪", layout="centered")

st.title("🧪 Alerta de Misturas Químicas")
st.markdown("Selecione dois produtos para verificar o risco da mistura. **Lembre-se: Química não é brincadeira!**")
st.divider()

# Função que reseta as escolhas para 'Selecione...'
def resetar():
    st.session_state["p1"] = "Selecione..."
    st.session_state["p2"] = "Selecione..."

# Inicializa o estado se for a primeira vez carregando
if "p1" not in st.session_state:
    st.session_state["p1"] = "Selecione..."
if "p2" not in st.session_state:
    st.session_state["p2"] = "Selecione..."

opcoes_produtos = ["Selecione...", "Azulim", "Bicarbonato", "Cândida", "Ox", "Vinagre"]

col1, col2 = st.columns(2)
with col1:
    reagente_a = st.selectbox("1º Produto:", opcoes_produtos, key="p1")
with col2:
    reagente_b = st.selectbox("2º Produto:", opcoes_produtos, key="p2")

st.divider()

# Botões lado a lado: Analisar e Limpar
btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    analisar = st.button("Analisar Risco da Mistura", type="primary", use_container_width=True)

with btn_col2:
    st.button("Limpar", on_click=resetar, use_container_width=True)

if analisar:
    if reagente_a == "Selecione..." or reagente_b == "Selecione...":
        st.warning("Selecione dois produtos para analisar.")
    else:
        nivel_perigo, mensagem = analisar_mistura(reagente_a, reagente_b)
        if nivel_perigo == "SEGURO":
            st.success(mensagem)
        elif nivel_perigo == "ALTO":
            st.error(mensagem)
        else:
            st.warning(mensagem)

st.caption("Projeto desenvolvido para a Feira de Ciências.")