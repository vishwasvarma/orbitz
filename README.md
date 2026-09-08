# Orbitz

Orbitz is a personalized fitness web application that helps users stay active based on their **fitness goals, daily activity, and progress**.

Users create an account, choose a goal such as **weight gain, weight loss, muscle gain, cardio/endurance, or general fitness**, and submit a daily check-in. The system analyzes the data using an ML model and an AI fitness agent, then generates a personalized **exercise and diet plan for tomorrow**.

---

## What Orbitz Does

```text
Register / Login
      ↓
Onboarding (goal + fitness level)
      ↓
Dashboard
      ↓
Daily Check-in
      ↓
Store Daily Data (history is kept)
      ↓
ML Fitness Analysis
      ↓
AI Fitness Agent
      ↓
Tomorrow's Plan (exercise + diet)
      ↓
Progress charts + PDF reports
```

### Users can

- Create an account and log in
- Complete onboarding (goal, level, and profile)
- Submit a daily check-in
- Log total exercise time **or minutes per activity** (walking, gym, running, and more)
- Add **medical constraints** so those exercises are left out of tomorrow's plan
- Choose **veg or non-veg for tomorrow** and list **food allergies**
- Get a personalized exercise and diet plan for the next day
- Track weight, steps, exercise, sleep, water, and fitness score
- Download a **weekly PDF** and a **3-day PDF**
- Log out

Past check-ins and plans are not wiped when new fields are added. Re-submitting only updates **today's** check-in and **tomorrow's** plan.

---

## How the Plan Is Generated

```text
Daily User Data
  (activity minutes, medical constraints, veg/non-veg, allergies)
       ↓
   ML Model
       ↓
Activity Level + Fitness Score
       ↓
   AI Fitness Agent
   (Groq, with a rule-based fallback)
       ↓
Exercise catalog (medical filters applied)
       +
Food catalog (diet preference + allergies applied)
       ↓
Personalized Tomorrow Plan
```

### ML Model

The ML model analyzes:

- Steps
- Exercise duration (sum of per-activity minutes when provided)
- Sleep
- Water intake
- Sitting time
- Intensity and how the user feels

It predicts activity level and a fitness score.

Example:

```text
Activity Level: Moderate
Fitness Score: 72/100
```

### AI Fitness Agent

The agent receives:

```text
User Goal
Fitness Level
Daily Activity (including minutes per type)
Medical Constraints
Tomorrow's diet preference (veg / non-veg)
Food allergies
Previous Data
ML Result
```

It builds tomorrow's plan from a **controlled exercise catalog** and a **controlled food catalog**. Exercises that conflict with medical constraints are skipped. Allergenic foods are excluded.

If no Groq API key is set, or the LLM call fails, Orbitz falls back to the rule-based engine.

---

# Tech Stack

| Component       | Technology        |
| --------------- | ----------------- |
| Frontend        | React + Vite      |
| Styling         | CSS               |
| Backend         | FastAPI           |
| Language        | Python            |
| Database        | SQLite (default)  |
| ORM             | SQLAlchemy        |
| Authentication  | JWT               |
| ML              | Scikit-learn      |
| AI              | Groq LLM + rules  |
| Reports         | PDF (fpdf2)       |
| Charts          | Recharts          |

PostgreSQL can be used by setting `DATABASE_URL`. Local development uses SQLite (`backend/orbitz.db`). New columns are added with `ALTER TABLE` so existing rows are kept.

---

# Project Structure

```text
orbitz/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── FitnessPlanCard.jsx
│   │   │   ├── ProgressChart.jsx
│   │   │   ├── ThemeToggle.jsx
│   │   │   └── Loading.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Onboarding.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DailyCheckIn.jsx
│   │   │   ├── TomorrowPlan.jsx
│   │   │   └── Progress.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── context/
│   │   │   ├── AuthContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── agent_service.py
│   │   │   ├── exercise_rules.py
│   │   │   ├── diet_rules.py
│   │   │   ├── report_service.py
│   │   │   └── fitness_service.py
│   │   ├── ml/
│   │   ├── database/
│   │   └── config.py
│   ├── requirements.txt
│   └── .env.example
│
├── ml/
├── README.md
└── .gitignore
```

---

# Database Structure

### Users

```text
users
├── id
├── username
├── password_hash
├── name
├── age
├── gender
├── height
├── weight
├── fitness_goal
├── fitness_level
├── onboarding_complete
└── created_at
```

### Daily Activity

```text
daily_activity
├── id
├── user_id
├── date
├── weight
├── steps
├── exercise_minutes          # total (sum of breakdown when provided)
├── exercise_intensity
├── exercise_types
├── exercise_breakdown        # e.g. { "Walking": 20, "Gym": 40 }
├── sleep_hours
├── water_liters
├── sitting_hours
├── feeling
├── medical_constraints       # e.g. ["knee_pain"]
├── diet_preference           # veg | non_veg (for tomorrow)
├── food_allergies
└── created_at
```

### Fitness Analysis

```text
fitness_analysis
├── id
├── daily_activity_id
├── activity_level
├── fitness_score
└── created_at
```

### Fitness Plans

```text
fitness_plans
├── id
├── user_id
├── date                      # plan is for tomorrow
├── plan                      # JSON: exercise sections + diet
├── reason
└── created_at
```

---

# Frontend Pages

## Login / Register

Username and password. New accounts go to onboarding.

## Onboarding

Users choose a goal:

- Muscle Gain
- Weight Gain
- Weight Loss
- Cardio & Endurance
- General Fitness

And a level: Beginner, Intermediate, or Advanced.

## Dashboard

Shows fitness score, today's stats, and a preview of tomorrow's plan.

## Daily Check-in

The user submits:

```text
Weight
Steps
Exercise by type + minutes (Walking, Running, Gym, Cycling, Sports, Yoga, Other)
  or a single total exercise minutes value
Exercise intensity
Sleep
Water
Sitting hours
Feeling
Medical constraints (skipped in tomorrow's workout)
Tomorrow veg or non-veg
Food allergies to exclude
```

Then:

```text
[ Generate Tomorrow's Plan ]
```

## Tomorrow's Plan

Includes:

- Strength, activity, and recovery from the allowed catalog
- Exercises skipped for medical reasons
- Diet for breakfast, lunch, dinner, and a snack
- Hydration and sleep targets

Example diet line:

```text
Lunch: Chicken 100 g, Steamed rice 150 g, Salad 100 g
```

## Progress

Weekly charts plus:

```text
[ Download weekly PDF ]
[ Download 3-day PDF ]
```

---

# Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
POST /auth/onboarding
PUT  /auth/profile
```

Passwords are stored hashed. Access uses a JWT bearer token.

---

# API

### Daily Activity

```text
POST /activity
GET  /activity/today
GET  /activity/history
```

`POST /activity` stores today's check-in, runs ML analysis, and upserts tomorrow's plan.

### Plans

```text
GET /plans/tomorrow
GET /plans/history
GET /plans/{plan_id}
```

### Progress

```text
GET /progress/dashboard
GET /progress/weekly
GET /progress/monthly
GET /progress/weekly.pdf
GET /progress/three-day.pdf
```

---

# Local Setup

## Prerequisites

- Python 3.10+ (3.11 recommended)
- Node.js 18+
- Git

```bash
python --version
node --version
npm --version
git --version
```

## 1. Backend

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set values:

```env
DATABASE_URL=sqlite:///./orbitz.db
SECRET_KEY=orbitz-dev-secret-change-in-production
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

`GROQ_API_KEY` is optional. Without it, plans still generate from the rule-based engine.

Tables are created on startup. New columns are added without deleting existing data.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8020
```

The frontend currently calls the API on port **8020** (`frontend/src/services/api.js`).

- API: http://127.0.0.1:8020
- Docs: http://127.0.0.1:8020/docs

## 2. Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

- App: http://localhost:5173

On the same Wi-Fi, others can open the Network URL Vite prints (for example `http://<your-lan-ip>:5173`). Keep the backend listening on `0.0.0.0`.

**Never commit `.env` files that contain real API keys.**

---

# Safety

Orbitz provides **general fitness and food suggestions** from user-provided information.

It is not a medical diagnosis, treatment, or nutrition prescription.

People with medical conditions, injuries, or allergies should confirm advice with a qualified professional.

---

# Project Goal

Orbitz makes fitness guidance simple and personal. Plans change with:

- Fitness goal and level
- Daily activity, including time spent on each type
- Medical constraints
- Tomorrow's veg / non-veg choice and allergies
- Sleep, water, weight, and recent progress
