
# Cosmetic Formulation Copilot — MVP (FastAPI)

Este é um MVP do **Copiloto de P&D Cosmético** com:
- API em FastAPI
- Catálogo de ingredientes (JSON) + fornecedores e preços
- Regras básicas por categoria (shampoo, condicionador, creme)
- Funções de validação, cálculo de custos e geração de lista INCI
- Rotas para buscar ingredientes e validar formulações

## Como rodar
```bash
python -m venv .venv
source .venv/bin/activate  # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Abra: http://127.0.0.1:8000/docs para testar a API interativamente.

## Estrutura
```
cosmetic-ai-mvp/
├─ app.py                # API FastAPI
├─ core/
│  ├─ models.py          # Pydantic models
│  ├─ rules_engine.py    # Motor de validação / regras
│  └─ utils.py           # Utilitários (INCI, custos, etc.)
├─ data/
│  ├─ ingredients.json   # Catálogo de ingredientes (exemplo)
│  └─ rules.json         # Regras por categoria (exemplo)
├─ prompts/
│  └─ system_prompt.txt  # Prompt do sistema sugerido para LLM orquestrado
├─ requirements.txt
└─ README.md
```

## Fluxo recomendado
1. **/ingredients/search**: buscar ingredientes por nome/INCI/função.
2. **/formula/validate**: enviar uma fórmula (categoria + itens) para flags de segurança/regulatório.
3. **/formula/generate_inci**: gerar a lista INCI ordenada.
4. **/formula/costs**: calcular custo por lote e por 100 g com base nos preços.

## Aviso
Este software é **educacional** e **não substitui** validação de bancada, testes regulatórios e responsável técnico (ANVISA).
