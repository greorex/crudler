# CRUDLer 🛠️  
_Automate your FastAPI microservice with dynamic SQLModel(s) — no boilerplate, just results._

## 📖 Overview  
**CRUDLer** is a helper workspace that lets you spin up a fully functional **FastAPI** microservice by simply defining your data models in **SQLModel**.  
Forget writing repetitive CRUD logic — CRUDLer automatically:  
- Creates your database schema  
- Generates REST API endpoints  
- Provides you with ready-to-run tests
- Builds production Docker image

You focus on **what** your data looks like, CRUDLer handles the **how**.

---

## ✨ Features & Benefits  
- Zero Boilerplate** – Define models, and you’re done.  
- Automatic Database Creation** – Tables are created from your SQLModel definitions.  
- REST API Generation** – CRUD endpoints for each model, instantly.  
- Test Suite Included** – Auto-generated tests to validate endpoints.  
- FastAPI Powered** – High-performance, async-ready APIs.  

---

## 📦 Setup Environment  
Just clone repository into VSCode Container Volume and wait until the creation process is done.

## 🛠️ Quick Start

### Let's quickly create a new Book model

Create a ```books.py``` file in the ```models``` folder

```python
from sqlmodel import Field, SQLModel 
from datetime import datetime

class Book(SQLModel):
    __tablename__ = "books"
    __route__ = "books"

    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True, nullable=False)
    author: str = Field(nullable=False)
    year: int = Field(nullable=False)
    timestamp: datetime | None = Field(default_factory=datetime.now, index=True)
```

Open ```.test.env``` file and add the model:
```env
MODELS="
...
books.Book
"
```

Add ```books.Book.json``` test fixture into ```tests/fixtures``` folder:
```json
{
  "path": "books",
  "item": {
    "title": "This is a new book",
    "author": "The famous author",
    "year": 2025
  },
  "update": {
    "title": "This is updated edition"
  },
  "id": null
}
``` 

### Test the service

Before starting the service run tests:

```bash
   pytest -v
   ```

### It's time to run the service

That's it. Just run:

```bash
   uvicorn src.main:app --reload
   ```

### Test in interactive mode

Use the OpenAPI docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).



