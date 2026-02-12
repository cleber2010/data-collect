# Resident Evil Database Scraper (Personagens)

Coletor de dados (web scraping) do site **residentevildatabase.com** para extrair informações de personagens, incluindo dados básicos e lista de aparições.  
O resultado é exportado para **CSV** e **Parquet** para facilitar análises posteriores.

> Projeto educacional / portfólio. Respeite os termos do site e use com moderação.

## 📌 O que este projeto faz
- Busca a lista de links de personagens em `/personagens`
- Visita cada página de personagem
- Extrai:
  - Campos básicos (ex: "Nome real", "Altura", etc. conforme a página)
  - Lista de **Aparições**
  - Link da página
  - Nome normalizado a partir da URL
- Gera arquivos:
  - `personagens.csv` (separador `;`)
  - `personagens.parquet`

## 🧱 Estrutura
src/
DATA-COLLECT/
collect.py


## ✅ Requisitos
- Python 3.10+ (recomendado)

## ⚙️ Instalação
```bash
# clone
git clone <SEU_REPO>
cd DATA-COLLECT

# ambiente virtual (opcional, recomendado)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/mac: source .venv/bin/activate

pip install -r requirements.txt
▶️ Como rodar
Exemplo (ajuste para o seu entrypoint):

python -m src.re_vil_db_scraper.scraper

🧠 Decisões técnicas

requests para HTTP

BeautifulSoup para parsing HTML

tqdm para barra de progresso

Exportação dupla (CSV + Parquet) para compatibilidade e performance