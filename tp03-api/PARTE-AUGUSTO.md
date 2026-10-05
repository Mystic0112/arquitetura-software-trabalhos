# Parte do Augusto — Autores

**Branch:** `augusto`  ·  **Prazo para abrir o PR:** 07/10/2026

Você cuida do recurso **Autor**: os schemas e o router. Os models e o banco o Hélio já deixa prontos na `main`. Leia o [`PLANO.md`](PLANO.md) antes de começar.

## Preparação

```bash
git clone git@github.com:Mystic0112/arquitetura-software-trabalhos.git
cd arquitetura-software-trabalhos/tp03-api
git checkout -b augusto
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload     # abra http://localhost:8000/docs
```

## O que fazer

### 1. `app/schemas/autor.py`
Três schemas Pydantic, separados:
- `AutorCreate`: `nome` (obrigatório), `nacionalidade` (opcional)
- `AutorUpdate`: todos os campos opcionais (serve para o PATCH)
- `AutorResponse`: `id`, `nome`, `nacionalidade`. Use `model_config = ConfigDict(from_attributes=True)`.

### 2. `app/routers/autores.py`
O arquivo já existe com `router = APIRouter()` vazio; preencha-o com estes endpoints (use `db: Session = Depends(get_db)`):

| Método | Rota | Status | Comportamento |
|---|---|---|---|
| POST | `/` | 201 | Cria um autor |
| GET | `/` | 200 | Lista todos |
| GET | `/{autor_id}` | 200 / 404 | Busca um; 404 com `HTTPException` se não existir |
| PATCH | `/{autor_id}` | 200 / 404 | Atualiza só os campos enviados (`model_dump(exclude_unset=True)`) |
| DELETE | `/{autor_id}` | 204 / 404 / 409 | Remove. Se o autor ainda tiver livros, devolva **409** com uma mensagem clara. |

Dica: o `main.py` já registra o seu router em `/autores`, então dentro do arquivo as rotas ficam só `/` e `/{autor_id}`.

## Como saber que terminou
- Pelo Swagger, você cria, lista, busca, atualiza e remove um autor.
- Buscar um id inexistente dá 404. Enviar um body sem `nome` dá 422.
- Apagar um autor que tem livro dá 409.

## Entrega
Faça commits pequenos com o seu usuário do Git (`git config user.name` e `user.email` seus). Depois `git push -u origin augusto` e abra o PR para `main` no GitHub.
