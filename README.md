# 🌍 What Is This Project?

This is a clean, modular **URL Shortener API** built using:

- ✅ **FastAPI** for the web API  
- ✅ **PostgreSQL** as the main database (with **SQLite** fallback if Postgres is unavailable)  
- ✅ **Base62 encoding** for short, unique, and human-friendly short codes  

---

## 💡 What Does the API Do?

It has **2 main endpoints**:

### 🔹 `POST /shorten`

- **Input**: A long URL (e.g., `https://www.google.com`)  
- **Output**: A short URL (e.g., `http://localhost:8000/bM9`)

✅ If the same URL is sent again, it returns the **existing short URL** (no duplication).

---

### 🔹 `GET /{short_code}`

- **Input**: A short code from the URL (like `bM9`)  
- **Output**: **Redirects** to the original long URL

---

## 🧠 How Does It Ensure Uniqueness?

Short code generation is **deterministic and unique**:

- When a new URL is added, it's assigned a **unique auto-incrementing ID** in the database.
- This ID is converted into a **Base62 string** (digits + A–Z + a–z).

### This ensures:
- 🔒 Codes are **always unique**
- ❌ No random collisions
- 📏 Codes are **shorter over time** (first few are just 1–2 characters like `1`, `a`, `B`, `z`, etc.)

✅ Even if a user sends the **same URL again** — it **reuses** the original short code.

---

## 📁 Project Structure

```
url_shortener/
├── app/
│   ├── main.py         # FastAPI app entry point
│   ├── database.py     # Sets up DB connection (Postgres or fallback to SQLite)
│   ├── models.py       # DB table definition using SQLAlchemy
│   ├── schemas.py      # Request/Response format validation (Pydantic)
│   ├── utils.py        # Encodes integer ID to Base62
│   └── routers/
│       └── url.py      # Main routing logic: shortening and redirecting
└── requirements.txt    # All needed packages
```

---

## 🔐 Fallback to SQLite

If `DATABASE_URL` is **not set** (e.g. in `.env` or environment variables), it automatically uses:

```
sqlite:///./url_shortener.db
```

This helps:

- ✅ Run the project locally without setting up Postgres  
- 🔁 Still allows switching to Postgres in production (just set the `DATABASE_URL`)

---

## 🛠️ How to Run the Project

1. Clone the repo or create files as shown

2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist yet, use:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

4. Run the app

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Test the API

### 🔸 `POST /shorten`

```http
POST http://localhost:8000/shorten
Content-Type: application/json

{
  "original_url": "https://openai.com"
}
```

**Response:**

```json
{
  "short_url": "http://localhost:8000/bM9"
}
```

---

### 🔸 `GET /bM9`

Open in browser:

```
http://localhost:8000/bM9
```

It redirects you to:

```
https://openai.com
```

---
