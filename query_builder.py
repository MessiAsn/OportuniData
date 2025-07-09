# query_builder.py


def montar_query_serpapi(
    linguagens,
    areas_sinonimos,
    senioridades_sinonimos,
    cidades,
    tipos_sinonimos,
    palavra_chave,
):
    partes = []
    # Se nenhum filtro tech for selecionado, adiciona termo tech fixo
    if not (linguagens or areas_sinonimos or senioridades_sinonimos):
        partes.append(
            "(tecnologia OR TI OR T.I. OR tech OR tecnologia da informação OR informação OR dev OR desenvolvedor OR desenvolvedora OR programador OR programadora OR software OR engenharia de software OR analista de sistemas OR informática OR sistemas OR computação OR IT OR information technology OR developer OR programmer OR software engineer OR system analyst OR computer science)"
        )
    if areas_sinonimos:
        if len(areas_sinonimos) == 1:
            partes.append(f"({' OR '.join(areas_sinonimos[0])})")
        else:
            all_areas = set()
            for sins in areas_sinonimos:
                all_areas.update(sins)
            partes.append(f"({' OR '.join(all_areas)})")
    if linguagens:
        if len(linguagens) == 1:
            partes.append(linguagens[0])
        else:
            partes.append(f"({' OR '.join(linguagens)})")
    if senioridades_sinonimos:
        if len(senioridades_sinonimos) == 1:
            partes.append(f"({' OR '.join(senioridades_sinonimos[0])})")
        else:
            all_sen = set()
            for sins in senioridades_sinonimos:
                all_sen.update(sins)
            partes.append(f"({' OR '.join(all_sen)})")
    if cidades:
        if len(cidades) == 1:
            partes.append(cidades[0])
        else:
            partes.append(f"({' OR '.join(cidades)})")
    if tipos_sinonimos:
        if len(tipos_sinonimos) == 1:
            partes.append(f"({' OR '.join(tipos_sinonimos[0])})")
        else:
            all_tipos = set()
            for sins in tipos_sinonimos:
                all_tipos.update(sins)
            partes.append(f"({' OR '.join(all_tipos)})")
    if palavra_chave:
        partes.append(palavra_chave)
    return " ".join(partes)
