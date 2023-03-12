import orjson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Page(BaseModel):
    name: str
    date: str
    author: str
    url: str
    content: str

    @staticmethod
    def from_dict(data: dict):
        record = Page(**data)
        return record


class Problem(BaseModel):
    detail: str


class Database:
    def __init__(self):
        self._data: list = []

    def load_from_filename(self, filename: str):
        with open(filename, "rb") as f:
            data = orjson.loads(f.read())
            for record in data:
                obj = Page.from_dict(record)
                self._data.append(obj)

    def delete(self, id: int):
        if 0 < id >= len(self._data):
            return
        self._data.pop(id)

    def add(self, article: Page):
        self._data.append(article)

    def get(self, id: int):
        if 0 < id >= len(self._data):
            return
        return self._data[id]

    def get_all(self) -> list[Page]:
        return self._data

    def update(self, id: int, article: Page):
        if 0 < id >= len(self._data):
            return
        self._data[id] = article

    def count(self) -> int:
        return len(self._data)


db = Database()
db.load_from_filename('articles.json')

app = FastAPI(title="Iservery Database", version="0.1", docs_url="/docs")

app.is_shutdown = False


@app.get("/articles", response_model=list[Page], description="Vrátí seznam článků")
async def get_articles():
    return db.get_all()


@app.get("/articles/{id}", response_model=Page)
async def get_article(id: int):
    return db.get(id)


@app.post("/articles", response_model=Page, description="Přidáme měsíc do DB")
async def post_articles(article: Page):
    db.add(article)
    return article


@app.delete("/articles/{id}", description="Sprovodíme film ze světa", responses={
    404: {'model': Problem}
})
async def delete_article(id: int):
    article = db.get(id)
    if article is None:
        raise HTTPException(404, "Článek neexistuje")
    db.delete(id)
    return {'status': 'smazano'}


@app.patch("/articles/{id}", description="Aktualizujeme clanek do DB", responses={
    404: {'model': Problem}
})
async def update_article(id: int, updated_article: Page):
    article = db.get(id)
    if article is None:
        raise HTTPException(404, "Film neexistuje")
    db.update(id, updated_article)
    return {'old': article, 'new': updated_article}