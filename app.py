
from fastapi import FastAPI, HTTPException
from typing import List
from core.models import Ingredient, Formula, FormulaItem, CostRequest, SearchQuery
from core.utils import load_ingredients, inci_sorted_list, cost_estimate
from core.rules_engine import validate_formula

app = FastAPI(title="Cosmetic Formulation Copilot — MVP")

INGREDIENTS: List[Ingredient] = load_ingredients()

@app.get("/ingredients", response_model=List[Ingredient])
def list_ingredients():
    return INGREDIENTS

@app.post("/ingredients/search", response_model=List[Ingredient])
def search_ingredients(q: SearchQuery):
    term = q.q.lower().strip()
    if not term:
        return INGREDIENTS
    out = []
    for ing in INGREDIENTS:
        if (term in ing.inci.lower() 
            or any(term in a.lower() for a in ing.aliases)
            or (ing.funcao and term in ing.funcao.lower())):
            out.append(ing)
    return out

@app.post("/formula/validate")
def formula_validate(formula: Formula):
    # valida e retorna flags
    return validate_formula(formula, INGREDIENTS)

@app.post("/formula/generate_inci")
def formula_inci(formula: Formula):
    return {"rotulo_inci": inci_sorted_list(formula.itens)}

@app.post("/formula/costs")
def formula_costs(cost_req: CostRequest):
    total, per100 = cost_estimate(cost_req.itens, INGREDIENTS, cost_req.lote_total_g)
    return {"custo_lote": total, "custo_por_100g": per100}
