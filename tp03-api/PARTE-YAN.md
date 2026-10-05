# Parte do Yan — Livros, README e apresentação

**Branch:** `yan`  ·  **Prazo para abrir o PR:** 07/10/2026

Você cuida do recurso **Livro** (schemas e router), do **README.md** final e do roteiro da apresentação. Os models e o banco o Hélio já deixa prontos na `main`. Leia o [`PLANO.md`](PLANO.md) antes de começar.

## Preparação

```bash
git clone git@github.com:Mystic0112/arquitetura-software-trabalhos.git
cd arquitetura-software-trabalhos/tp03-api
git checkout -b yan
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload     # abra http://localhost:8000/docs
```

## O que fazer

### 1. `app/schemas/livro.py`
- `LivroCreate`: `titulo` (obrigatório), `ano` (opcional), `autor_id` (obrigatório)
- `LivroUpdate`: todos os campos opcionais
- `LivroResponse`: `id`, `titulo`, `ano`, `autor_id`, com `model_config = ConfigDict(from_attributes=True)`

### 2. `app/routers/livros.py`
O arquivo já existe com `router = APIRouter()` vazio (registrado em `/livros` pelo `main.py`), com `db: Session = Depends(get_db)`:

| Método | Rota | Status | Comportamento |
|---|---|---|---|
| POST | `/` | 201 / 404 | **Antes de criar, confira se o `autor_id` existe.** Se não existir, 404 com mensagem clara (requisito 8 do trabalho). |
| GET | `/` | 200 | Lista todos. Opcional: filtro `?autor_id=`. |
| GET | `/{livro_id}` | 200 / 404 | Busca um |
| PATCH | `/{livro_id}` | 200 / 404 | Atualiza só os campos enviados. Se trocar o `autor_id`, valide-o de novo. |
| DELETE | `/{livro_id}` | 204 / 404 | Remove |

### 3. `README.md` (em `tp03-api/`)
O professor exige estes itens:
- Descrição do modelo de negócio (biblioteca, Autor e Livro)
- Diagrama ou descrição das entidades e do relacionamento (pode ser mermaid `classDiagram` ou `erDiagram`)
- Passo a passo: instalar dependências, rodar `alembic upgrade head`, subir com `uvicorn`
- Lista dos endpoints implementados (tabela método, rota, descrição)

### 4. Roteiro da apresentação (5 a 10 min)
Crie `tp03-api/APRESENTACAO.md` com a sequência da demo no Swagger:
1. Criar um autor → 201
2. Criar um livro com esse autor → 201
3. Criar um livro com `autor_id` inexistente → 404 (validação de FK)
4. Enviar body inválido → 422
5. Listar, atualizar e apagar
6. Tentar apagar um autor com livros → 409
Indique quem fala cada parte: o Hélio explica a estrutura e a migration, o Augusto mostra os autores, o Yan mostra os livros e a validação.

## Como saber que terminou
- Todas as rotas de `/livros` funcionam no Swagger, e o `POST` com autor inexistente dá 404.
- Alguém que nunca viu o projeto consegue rodá-lo só seguindo o README.

## Entrega
Faça commits pequenos com o seu usuário do Git (`git config user.name` e `user.email` seus). Depois `git push -u origin yan` e abra o PR para `main` no GitHub.
