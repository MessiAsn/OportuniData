import os
import streamlit as st
from dotenv import load_dotenv
from scraper import JobRadarScraper
from utils import (
    carregar_linguagens,
    carregar_areas,
    carregar_senioridades,
    carregar_tipos,
    carregar_estados_cidades,
    extrair_nomes,
    buscar_sinonimos,
)
from query_builder import montar_query_serpapi
import pandas as pd


# Carrega a API key
def get_api_key():
    load_dotenv()
    return os.getenv("SERPAPI_KEY")


# Carrega listas dinâmicas dos JSONs
linguagens = carregar_linguagens()
areas = carregar_areas()
senioridades = carregar_senioridades()
tipos = carregar_tipos()
estados, cidades_por_estado = carregar_estados_cidades()

# Extrai nomes para exibir nos filtros
linguagens_nomes = (
    linguagens if isinstance(linguagens[0], str) else extrair_nomes(linguagens)
)
areas_nomes = extrair_nomes(areas)
senioridades_nomes = extrair_nomes(senioridades)
tipos_nomes = extrair_nomes(tipos)

st.set_page_config(page_title="OportuniData", layout="wide")
st.title("🚀 OportuniData – Vagas via Google Jobs")

st.markdown(
    """
Selecione os filtros desejados para montar sua busca booleana:
"""
)

areas_sel = st.multiselect("Áreas", areas_nomes)
linguagens_sel = st.multiselect("Linguagens", linguagens_nomes)
senioridades_sel = st.multiselect("Senioridade", senioridades_nomes)
tipos_sel = st.multiselect("Tipo de vaga", tipos_nomes)

# Adiciona campo de busca livre
palavra_chave = st.text_input("Palavra-chave (opcional)")


# Só considera cidades na query se houver seleção, nunca inclui estado
cidades_sel = []  # Garante definição antes do uso
cidades_query = cidades_sel if cidades_sel else []

tem_filtros = any(
    [
        linguagens_sel,
        areas_sel,
        senioridades_sel,
        cidades_query,
        tipos_sel,
        palavra_chave,
    ]
)

# Busca sinônimos para montagem da query
areas_sinonimos = buscar_sinonimos(areas, areas_sel)
senioridades_sinonimos = buscar_sinonimos(senioridades, senioridades_sel)
tipos_sinonimos = buscar_sinonimos(tipos, tipos_sel)

query = (
    montar_query_serpapi(
        linguagens_sel,
        areas_sinonimos,
        senioridades_sinonimos,
        cidades_query,
        tipos_sinonimos,
        palavra_chave,
    )
    if tem_filtros
    else ""
)

# Checkbox para busca apenas no Brasil
apenas_brasil = st.checkbox(
    "Buscar apenas vagas no Brasil", value=True, key="apenas_brasil"
)

# Inicializa variáveis
estado_sel = None
cidades_sel = []
cidades_query = []
location_param = ""

if apenas_brasil:
    estado_sel = st.selectbox(
        "Estado", ["(Todo o Brasil)"] + estados, key="estado_brasil"
    )
    if estado_sel != "(Todo o Brasil)":
        cidades_sel = st.multiselect(
            "Cidade(s)", cidades_por_estado[estado_sel], key="cidades_brasil"
        )
    cidades_query = cidades_sel if cidades_sel else []
    location_param = (
        f"{cidades_sel[0]}, Brazil"
        if cidades_sel and len(cidades_sel) == 1
        else f"{', '.join(cidades_sel)}, Brazil" if cidades_sel else "Brazil"
    )
else:
    # Busca global, sem restrição de localização e sem mostrar campo extra
    cidades_query = []
    location_param = ""

params_api = {
    "engine": "google_jobs",
    "q": query,
    "location": location_param,
    "hl": "pt-br",
    "gl": "br" if apenas_brasil else "",
    "api_key": get_api_key(),
}

# Carrega e injeta o CSS externo (sempre)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not tem_filtros or not query.strip():
    st.warning("Preencha pelo menos um filtro para realizar a busca.")
else:
    # Exibe resumo amigável dos filtros selecionados
    st.markdown("#### Filtros selecionados:")
    if areas_sel:
        st.write("**Áreas:**", ", ".join(areas_sel))
    if linguagens_sel:
        st.write("**Linguagens:**", ", ".join(linguagens_sel))
    if senioridades_sel:
        st.write("**Senioridade:**", ", ".join(senioridades_sel))
    if tipos_sel:
        st.write("**Tipo de vaga:**", ", ".join(tipos_sel))
    if apenas_brasil:
        if estado_sel and estado_sel != "(Todo o Brasil)":
            st.write("**Estado:**", estado_sel)
        if cidades_sel:
            st.write("**Cidade(s):**", ", ".join(cidades_sel))
    if palavra_chave:
        st.write("**Palavra-chave:**", palavra_chave)

    if st.button("Buscar Vagas"):
        api_key = get_api_key()
        if not api_key:
            st.error("Erro: SERPAPI_KEY não definida no .env!")
        else:
            scraper = JobRadarScraper(api_key)
            with st.spinner("Consultando Google Jobs..."):
                try:
                    from serpapi import Client

                    serp_client = Client(api_key=api_key)
                    results = serp_client.search(params_api)
                    jobs = results.get("jobs_results", [])
                    # Se não encontrar vagas, tenta uma query mais simples (apenas linguagem + vaga)
                    if (
                        not jobs
                        and linguagens_sel
                        and not any(
                            [
                                areas_sel,
                                senioridades_sel,
                                cidades_query,
                                tipos_sel,
                                palavra_chave,
                            ]
                        )
                    ):
                        query_simples = f"(vaga OR vacancy OR job OR emprego OR opportunity) {' '.join(linguagens_sel)}"
                        params_api_simples = params_api.copy()
                        params_api_simples["q"] = query_simples
                        results = serp_client.search(params_api_simples)
                        jobs = results.get("jobs_results", [])
                        st.info(
                            "Poucas vagas encontradas. Buscando novamente de forma mais ampla..."
                        )
                    # Implementa paginação correta usando next_page_token
                    all_jobs = jobs.copy() if jobs else []
                    next_page_token = results.get("serpapi_pagination", {}).get(
                        "next_page_token"
                    )
                    max_pages = 3
                    page_count = 1
                    while next_page_token and page_count < max_pages:
                        paged_results = serp_client.search(
                            {**params_api, "next_page_token": next_page_token}
                        )
                        paged_jobs = paged_results.get("jobs_results", [])
                        if not paged_jobs:
                            break
                        all_jobs.extend(paged_jobs)
                        next_page_token = paged_results.get(
                            "serpapi_pagination", {}
                        ).get("next_page_token")
                        page_count += 1
                    if not all_jobs:
                        st.warning(
                            "Nenhuma vaga encontrada para sua busca. Tente usar menos filtros ou termos mais genéricos."
                        )
                    else:
                        for job in all_jobs:
                            st.markdown(
                                f"""<div class="vaga-card">\n                                <div class="vaga-titulo">{job.get('title','')}</div>\n                                <div class="vaga-empresa">{job.get('company_name','')}</div>\n                                <div class="vaga-local">{job.get('location','')}</div>\n                                <div class="vaga-desc">{job.get('description','')[:400]}{'...' if job.get('description','') and len(job.get('description',''))>400 else ''}</div>\n                                <a class="vaga-link" style="background:#60a5fa; color:#fff;" href="{job.get('link') or job.get('share_link')}" target="_blank">Ver vaga no Google Jobs</a>\n                            </div>""",
                                unsafe_allow_html=True,
                            )
                        st.success(f"{len(all_jobs)} vagas encontradas.")
                        # CSV download
                        df = pd.DataFrame(
                            [
                                {
                                    "Título": job.get("title"),
                                    "Empresa": job.get("company_name"),
                                    "Localização": job.get("location"),
                                    "Link": job.get("link") or job.get("share_link"),
                                    "Descrição": job.get("description"),
                                }
                                for job in all_jobs
                            ]
                        )
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "📥 Baixar CSV", csv, "dev_vagas.csv", "text/csv"
                        )
                    st.markdown("### Resposta completa da API (debug)")
                    st.json(results)
                except Exception as e:
                    st.error(f"Erro: {e}")
