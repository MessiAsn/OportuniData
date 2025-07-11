import json


def carregar_linguagens():
    with open("json/ling-programacao.json", encoding="utf-8") as f:
        return json.load(f)


def carregar_areas():
    with open("json/areas-atuacao.json", encoding="utf-8") as f:
        return json.load(f)


def carregar_senioridades():
    with open("json/senioridades.json", encoding="utf-8") as f:
        return json.load(f)


def carregar_tipos():
    with open("json/modalidades.json", encoding="utf-8") as f:
        return json.load(f)


def carregar_estados_cidades():
    with open("json/estados-cidades.json", encoding="utf-8") as f:
        dados = json.load(f)
    estados = [e["nome"] for e in dados["estados"] if e["cidades"]]
    cidades_por_estado = {e["nome"]: e["cidades"] for e in dados["estados"]}
    return estados, cidades_por_estado


def extrair_nomes(lista_dicts):
    return [item["nome"] for item in lista_dicts]


def buscar_sinonimos(lista_dicts, selecionados):
    sinonimos = []
    for nome in selecionados:
        for item in lista_dicts:
            if item["nome"] == nome:
                sinonimos.append(item["sinonimos"])
                break
    return sinonimos
