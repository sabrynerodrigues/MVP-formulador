
import json, os
from typing import List, Dict, Tuple
from .models import Formula, FormulaItem, Ingredient

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_ingredients() -> List[Ingredient]:
    path = os.path.join(DATA_DIR, "ingredients.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Ingredient(**x) for x in data]

def load_rules() -> Dict:
    path = os.path.join(DATA_DIR, "rules.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def inci_sorted_list(items: List[FormulaItem]) -> str:
    # Ordenar por % decrescente (como proxy; na prática, ordem INCI tem regras específicas)
    sorted_items = sorted(items, key=lambda x: -x.pct)
    return ", ".join([x.inci for x in sorted_items])

def cost_estimate(items: List[FormulaItem], ingredients: List[Ingredient], lote_total_g: float) -> Tuple[float, float]:
    # custo por lote e custo por 100 g
    price_map = {ing.inci: (ing.fornecedores[0]["preco_kg"] if ing.fornecedores else 0.0) for ing in ingredients}
    total_cost = 0.0
    for it in items:
        preco_kg = price_map.get(it.inci, 0.0)
        massa_g = (it.pct / 100.0) * lote_total_g
        custo = (massa_g / 1000.0) * preco_kg
        total_cost += custo
    cost_per_100g = (total_cost / lote_total_g) * 100.0 if lote_total_g else 0.0
    return round(total_cost, 4), round(cost_per_100g, 4)
