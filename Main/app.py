import os

import streamlit as st
from redis import Redis
from redis.exceptions import RedisError
from supabase import Client, create_client
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(page_title="Sistema de Brinquedos", layout="centered")

CACHE_KEY = "play_toy:brinquedos"
CACHE_TTL_SECONDS = 60


def config_value(name):
    """Lê configuração de variáveis de ambiente ou dos secrets do Streamlit."""
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets[name]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


@st.cache_resource
def get_supabase() -> Client:
    url = config_value("SUPABASE_URL")
    key = config_value("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Configure SUPABASE_URL e SUPABASE_KEY.")
    return create_client(url, key)


@st.cache_resource
def get_redis():
    url = config_value("REDIS_URL")
    if not url:
        return None
    try:
        client = Redis.from_url(url, decode_responses=True, socket_connect_timeout=2)
        client.ping()
        return client
    except (RedisError, ValueError):
        return None


def invalidar_cache():
    cache = get_redis()
    if cache:
        try:
            cache.delete(CACHE_KEY)
        except RedisError:
            pass


def listar_brinquedos():
    cache = get_redis()
    if cache:
        try:
            dados = cache.get(CACHE_KEY)
            if dados:
                import json
                return json.loads(dados)
        except (RedisError, ValueError):
            pass

    response = get_supabase().table("brinquedos").select("*").order("id").execute()
    brinquedos = response.data or []
    if cache:
        try:
            import json
            cache.setex(CACHE_KEY, CACHE_TTL_SECONDS, json.dumps(brinquedos, ensure_ascii=False))
        except RedisError:
            pass
    return brinquedos


try:
    supabase = get_supabase()
    brinquedos = listar_brinquedos()
except Exception as exc:
    st.error(f"Não foi possível conectar ao banco de dados: {exc}")
    st.info("Configure SUPABASE_URL e SUPABASE_KEY nas variáveis de ambiente ou em .streamlit/secrets.toml.")
    st.stop()

if not config_value("REDIS_URL") or get_redis() is None:
    st.sidebar.caption("Redis indisponível: usando o Supabase sem cache.")
else:
    st.sidebar.caption("Cache Redis ativo.")

st.title("🧸 Sistema de Cadastro de Brinquedos")
menu = st.sidebar.selectbox(
    "Menu", ["Cadastrar", "Listar", "Atualizar", "Remover", "Relatórios", "Buscar", "Sair"]
)

if menu == "Cadastrar":
    st.header("Cadastrar Brinquedo")
    id_input = st.text_input("ID do brinquedo")
    nome = st.text_input("Nome do brinquedo")
    marca = st.text_input("Marca")
    preco = st.text_input("Preço (apenas números)")
    status = st.selectbox("Tem estoque?", ["Sim", "Não"])

    if st.button("✅ Cadastrar"):
        try:
            brinquedo_id = int(id_input)
            valor = float(preco.replace(",", "."))
            if brinquedo_id < 0:
                raise ValueError("O ID não pode ser negativo.")
            if valor < 0:
                raise ValueError("O preço não pode ser negativo.")
            if any(item["id"] == brinquedo_id for item in brinquedos):
                raise ValueError("ID já utilizado!")
            supabase.table("brinquedos").insert({
                "id": brinquedo_id,
                "nome": nome,
                "marca": marca,
                "preco": valor,
                "disponibilidade": "Brinquedo com Estoque" if status == "Sim" else "Brinquedo sem Estoque",
            }).execute()
            invalidar_cache()
            st.success("✅ Brinquedo cadastrado com sucesso!")
            st.rerun()
        except ValueError as exc:
            st.error(f"❌ {exc}")
        except Exception as exc:
            st.error(f"Não foi possível cadastrar: {exc}")

elif menu == "Listar":
    st.header("Lista de Brinquedos")
    if brinquedos:
        st.table(brinquedos)
    else:
        st.warning("Nenhum brinquedo cadastrado!")

elif menu == "Buscar":
    st.header("Buscar Brinquedo")
    busca = st.text_input("Digite nome, marca ou ID:").strip().lower()
    if st.button("🔍 Buscar"):
        resultados = [item for item in brinquedos if busca in str(item["id"]).lower()
                      or busca in item["nome"].lower() or busca in item["marca"].lower()]
        if resultados:
            st.success("✅ Resultado encontrado:")
            st.table(resultados)
        else:
            st.error("❌ Nenhum brinquedo encontrado!")

elif menu == "Remover":
    st.header("Remover Brinquedo")
    ids = [item["id"] for item in brinquedos]
    if ids:
        escolha = st.selectbox("Selecione o ID:", ids)
        if st.button("🗑 Remover"):
            try:
                supabase.table("brinquedos").delete().eq("id", escolha).execute()
                invalidar_cache()
                st.success("✅ Brinquedo removido com sucesso!")
                st.rerun()
            except Exception as exc:
                st.error(f"Não foi possível remover: {exc}")
    else:
        st.warning("Nenhum brinquedo cadastrado!")

elif menu == "Atualizar":
    st.header("Atualizar Brinquedo")
    ids = [item["id"] for item in brinquedos]
    if ids:
        escolha = st.selectbox("Selecione o ID:", ids)
        atual = next(item for item in brinquedos if item["id"] == escolha)
        novo_nome = st.text_input("Nome:", atual["nome"])
        nova_marca = st.text_input("Marca:", atual["marca"])
        novo_preco = st.text_input("Preço:", str(atual["preco"]))
        novo_status = st.selectbox("Disponibilidade:", ["Brinquedo com Estoque", "Brinquedo sem Estoque"],
                                   index=0 if atual["disponibilidade"] == "Brinquedo com Estoque" else 1)
        if st.button("✅ Atualizar"):
            try:
                valor = float(novo_preco.replace(",", "."))
                if valor < 0:
                    raise ValueError("O preço não pode ser negativo.")
                supabase.table("brinquedos").update({
                    "nome": novo_nome, "marca": nova_marca, "preco": valor,
                    "disponibilidade": novo_status,
                }).eq("id", escolha).execute()
                invalidar_cache()
                st.success("✅ Atualizado com sucesso!")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Não foi possível atualizar: {exc}")
    else:
        st.warning("Nenhum brinquedo cadastrado!")

elif menu == "Relatórios":
    st.header("Relatórios")
    if not brinquedos:
        st.warning("Nenhum brinquedo cadastrado!")
    else:
        marcas = {}
        for item in brinquedos:
            marcas.setdefault(item["marca"], []).append(item["nome"])
        st.subheader("📌 Brinquedos por marca")
        st.write(marcas)
        st.subheader("✅ Com estoque")
        st.write([item["nome"] for item in brinquedos
                  if item["disponibilidade"] == "Brinquedo com Estoque"] or "Nenhum")
        st.subheader("❌ Sem estoque")
        st.write([item["nome"] for item in brinquedos
                  if item["disponibilidade"] == "Brinquedo sem Estoque"] or "Nenhum")

elif menu == "Sair":
    st.info("✅ Feche a aba para sair do sistema.")
