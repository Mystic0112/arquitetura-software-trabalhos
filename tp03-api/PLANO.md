# TP03 — Plano e divisão (API de Biblioteca)

**Modelo de negócio:** biblioteca. Entidades: `Autor` (1) ── (N) `Livro`, via `livros.autor_id` (ForeignKey).

Prazo de envio: **09/10/2026 às 23:59**. Apresentação de 5 a 10 min no Swagger (`/docs`).

## Estrutura de pastas

```
tp03-api/
├── app/
│   ├── main.py            # Hélio
│   ├── core/database.py   # Hélio
│   ├── models/            # Hélio (autor.py, livro.py)
│   ├── schemas/           # autor.py (Augusto) · livro.py (Yan)
│   └── routers/           # autores.py (Augusto) · livros.py (Yan)
├── alembic/               # Hélio (migration versionada)
├── alembic.ini
├── requirements.txt
└── README.md              # Yan
```

## Divisão

| Parte | Quem | Entrega | Arquivo de instruções |
|---|---|---|---|
| 1 — Base | Hélio | Projeto, banco, models, Alembic e migration, `main.py` | este arquivo |
| 2 — Autores | Augusto | Schemas + router de `Autor` (CRUD) | [`PARTE-AUGUSTO.md`](PARTE-AUGUSTO.md) |
| 3 — Livros e docs | Yan | Schemas + router de `Livro` (com validação de FK) + README + roteiro da apresentação | [`PARTE-YAN.md`](PARTE-YAN.md) |

## Ordem de trabalho

1. Hélio faz a Parte 1 e dá push na `main`. Isso libera os outros dois.
2. Augusto e Yan fazem `git pull`, criam a própria branch (`augusto` / `yan`), trabalham em paralelo (arquivos diferentes, sem conflito) e abrem PR para `main`.
3. Hélio revisa e faz o merge. No fim, todos rodam a API juntos e ensaiam a apresentação.

## Contrato entre as partes

- `Autor`: `id`, `nome` (str, obrigatório), `nacionalidade` (str, opcional)
- `Livro`: `id`, `titulo` (str, obrigatório), `ano` (int, opcional), `autor_id` (int, FK → `autores.id`, obrigatório)
- Tabelas: `autores` e `livros`. Relationship: `Autor.livros` ↔ `Livro.autor`.
- Dependência de sessão: `from app.core.database import get_db`.
- Cada router é exportado como `router` e já é registrado no `main.py` pelo Hélio (`/autores` e `/livros`).
