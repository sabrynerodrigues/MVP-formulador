
from typing import List, Dict
from .models import Formula, FormulaItem, Ingredient
from .utils import load_rules

def validate_formula(formula: Formula, ingredients: List[Ingredient]) -> Dict:
    rules = load_rules()
    cats = rules.get("categorias", {})
    globais = rules.get("globais", [])
    cat = cats.get(formula.categoria.lower())
    flags = []

    # mapa de ingredientes por INCI
    ing_map = {ing.inci.lower(): ing for ing in ingredients}
    total_pct = sum([x.pct for x in formula.itens])
    if any(r["regra"] == "soma_percentuais_igual_100" for r in globais):
        if abs(total_pct - 100.0) > 0.01:
            flags.append({"tipo": "erro", "mensagem": f"Soma de percentuais = {total_pct:.2f} (deve ser 100.00)."})

    # faixas individuais
    if any(r["regra"] == "respeitar_faixas_ingredientes" for r in globais):
        for it in formula.itens:
            ing = ing_map.get(it.inci.lower())
            if not ing:
                flags.append({"tipo": "alerta", "mensagem": f"Ingrediente não cadastrado: {it.inci}."})
                continue
            if it.pct < ing.faixa_min or it.pct > ing.faixa_max:
                flags.append({
                    "tipo": "erro",
                    "mensagem": f"{it.inci}: {it.pct}% fora da faixa ({ing.faixa_min}–{ing.faixa_max}%)."
                })

    # limites por categoria
    if cat:
        limites = cat.get("limites", [])
        for lim in limites:
            for it in formula.itens:
                if it.inci.lower() == lim["inci"].lower() and it.pct > lim.get("max_pct", 999):
                    flags.append({
                        "tipo": "erro",
                        "mensagem": f"{it.inci}: {it.pct}% excede limite da categoria {formula.categoria} ({lim['max_pct']}%)."
                    })
        # pH alvo
        if formula.pH_alvo is not None:
            pH_min, pH_max = cat.get("pH_min"), cat.get("pH_max")
            if pH_min is not None and formula.pH_alvo < pH_min or pH_max is not None and formula.pH_alvo > pH_max:
                flags.append({
                    "tipo": "alerta",
                    "mensagem": f"pH alvo {formula.pH_alvo} fora do recomendado para {formula.categoria} ({pH_min}–{pH_max})."
                })

    return {"flags": flags, "observacoes_categoria": cat.get("observacoes", []) if cat else []}
