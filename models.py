
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Ingredient(BaseModel):
    id: str
    inci: str
    aliases: List[str] = []
    funcao: Optional[str] = None
    origem: Optional[str] = None
    faixa_min: float
    faixa_max: float
    pH_min: float
    pH_max: float
    solubilidade: Optional[str] = None
    incompatibilidades: List[str] = []
    regulatorio: Dict = {}
    fornecedores: List[Dict] = []

class FormulaItem(BaseModel):
    inci: str
    pct: float

class Formula(BaseModel):
    categoria: str
    itens: List[FormulaItem]
    pH_alvo: Optional[float] = None
    lote_total_g: Optional[float] = 1000.0

class CostRequest(BaseModel):
    itens: List[FormulaItem]
    lote_total_g: float = 1000.0

class SearchQuery(BaseModel):
    q: str = Field("", description="Termo de busca por INCI, alias ou função")
