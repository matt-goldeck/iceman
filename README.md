# Iceman
![MSDTOGU_EC038](https://github.com/user-attachments/assets/cd189adc-ef5b-4a39-a891-3095c3794ade)

[you guys really are cowboys](https://youtu.be/z_BEJmY911s)

Iceman is the backend for the Afterburner job tracking platform. Built with FastAPI, SQLModel, and Supabase, Iceman does the heavy lifting when it comes to parsing, user data management, and AI-powered tasks.

## 🧰 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Supabase](https://supabase.com/)
- [OpenAI](https://platform.openai.com/)
- [Python 3.12](https://www.python.org/)

## 🛠️ Local Setup

### 1. Clone the Repository
```bash
git clone git@github.com:matt-goldeck/iceman.git
cd iceman
```

### 2. Install Dependencies
```bash
pipenv install --dev
```

### 3. Create .env
```
DATABASE_URL=postgresql://user:password@localhost:5432/afterburner
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
OPENAI_API_KEY=your-openai-api-key
(...)
```

### 4. Takeoff
```bash
uvicorn index:app --reload --log-level debug
```
navigate to [localhost:8000/docs](http://localhost:8000/docs) for Swagger UI
