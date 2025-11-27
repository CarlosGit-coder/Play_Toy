import streamlit as st

st.set_page_config(page_title="Sistema de Brinquedos", layout="centered")

if "brinquedos" not in st.session_state:
    st.session_state.brinquedos = []
    st.session_state.id_set = set()


def atualizar_id_set():
    st.session_state.id_set = set([item['id'] for item in st.session_state.brinquedos])


def verificar_id(id_input):
    try:
        id_input = int(id_input)
        if id_input in st.session_state.id_set:
            st.error("❌ ID já utilizado!")
            return False
        if id_input < 0:
            st.error("❌ ID não pode ser negativo!")
            return False
    except:
        st.error("❌ O ID deve ser um número inteiro positivo!")
        return False
    return id_input


st.title("🧸 Sistema de Cadastro de Brinquedos")


menu = st.sidebar.selectbox(
    "Menu",
    ["Cadastrar", "Listar", "Atualizar", "Remover", "Relatórios", "Buscar", "Sair"]
)

# ✅ CADASTRAR
if menu == "Cadastrar":
    st.header("Cadastrar Brinquedo")

    id_input = st.text_input("ID do brinquedo")
    nome = st.text_input("Nome do brinquedo")
    marca = st.text_input("Marca")
    preco = st.text_input("Preço (apenas números)")
    status = st.selectbox("Tem estoque?", ["Sim", "Não"])

    if st.button("✅ Cadastrar"):
        id_validado = verificar_id(id_input)
        if id_validado is not False:
            brinquedo = {
                "id": id_validado,
                "nome": nome,
                "marca": marca,
                "preço": preco,
                "disponibilidade": "Brinquedo com Estoque" if status == "Sim" else "Brinquedo sem Estoque"
            }
            st.session_state.brinquedos.append(brinquedo)
            atualizar_id_set()
            st.success("✅ Brinquedo cadastrado com sucesso!")


# ✅ LISTAR
elif menu == "Listar":
    st.header("Lista de Brinquedos")
    if not st.session_state.brinquedos:
        st.warning("Nenhum brinquedo cadastrado!")
    else:
        st.table(st.session_state.brinquedos)


# ✅ BUSCAR
elif menu == "Buscar":
    st.header("Buscar Brinquedo")
    busca = st.text_input("Digite nome, marca ou ID:")

    if st.button("🔍 Buscar"):
        resultados = []
        for item in st.session_state.brinquedos:
            if busca.lower() in str(item['id']).lower() or \
               busca.lower() in item['nome'].lower() or \
               busca.lower() in item['marca'].lower():
                resultados.append(item)

        if resultados:
            st.success("✅ Resultado encontrado:")
            st.table(resultados)
        else:
            st.error("❌ Nenhum brinquedo encontrado!")


# ✅ REMOVER
elif menu == "Remover":
    st.header("Remover Brinquedo")
    ids = [item['id'] for item in st.session_state.brinquedos]

    if ids:
        escolha = st.selectbox("Selecione o ID:", ids)
        if st.button("🗑 Remover"):
            st.session_state.brinquedos = [b for b in st.session_state.brinquedos if b['id'] != escolha]
            atualizar_id_set()
            st.success("✅ Brinquedo removido com sucesso!")
    else:
        st.warning("Nenhum brinquedo cadastrado!")


# ✅ ATUALIZAR
elif menu == "Atualizar":
    st.header("Atualizar Brinquedo")
    ids = [item['id'] for item in st.session_state.brinquedos]

    if ids:
        escolha = st.selectbox("Selecione o ID:", ids)
        brinquedo = next(b for b in st.session_state.brinquedos if b['id'] == escolha)

        novo_nome = st.text_input("Nome:", brinquedo['nome'])
        nova_marca = st.text_input("Marca:", brinquedo['marca'])
        novo_preco = st.text_input("Preço:", brinquedo['preço'])
        novo_status = st.selectbox("Disponibilidade:", ["Brinquedo com Estoque", "Brinquedo sem Estoque"])

        if st.button("✅ Atualizar"):
            brinquedo.update({
                "nome": novo_nome,
                "marca": nova_marca,
                "preço": novo_preco,
                "disponibilidade": novo_status
            })
            st.success("✅ Atualizado com sucesso!")
    else:
        st.warning("Nenhum brinquedo cadastrado!")


# ✅ RELATÓRIOS
elif menu == "Relatórios":
    st.header("Relatórios")

    if not st.session_state.brinquedos:
        st.warning("Nenhum brinquedo cadastrado!")
    else:
        marcas = {}
        for b in st.session_state.brinquedos:
            marcas.setdefault(b['marca'], []).append(b['nome'])

        st.subheader("📌 Brinquedos por marca")
        st.write(marcas)

        disponiveis = [b['nome'] for b in st.session_state.brinquedos if b['disponibilidade'] == "Brinquedo com Estoque"]
        sem = [b['nome'] for b in st.session_state.brinquedos if b['disponibilidade'] == "Brinquedo sem Estoque"]

        st.subheader("✅ Com estoque")
        st.write(disponiveis or "Nenhum")

        st.subheader("❌ Sem estoque")
        st.write(sem or "Nenhum")


elif menu == "Sair":
    st.info("✅ Feche a aba para sair do sistema.")
