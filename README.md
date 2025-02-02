⚙️ Setup Instructions

1️⃣ Clone the Repository

# Clone the project from GitHub (replace with your repo URL)

```bash
git clone https://github.com/your-repo/openai-integration-project.git
cd openai-integration-project
```

2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

3️⃣ Activate the Virtual Environment

On Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

5️⃣ Run Database Migrations

```bash
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

6️⃣ Start the FastAPI Server

```bash
uvicorn main:app --reload
```

The API will now be available at: http://127.0.0.1:8000

