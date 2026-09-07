# Orbitz

Orbitz is a personalized fitness web application that helps users stay active based on their **fitness goals, daily activity, and progress**.

Users create an account, choose a goal such as **weight gain, weight loss, muscle gain, cardio/endurance, or general fitness**, and submit daily fitness information. The system analyzes the data using an ML model and generates a personalized plan for the next day.

---

## What Orbitz Does

```text
Register / Login
      ↓
Select Fitness Goal
      ↓
Dashboard
      ↓
Daily Check-in
      ↓
Store Daily Data
      ↓
ML Fitness Analysis
      ↓
AI Fitness Agent
      ↓
Generate Tomorrow's Plan
      ↓
Show Plan on Dashboard
      ↓
Next Day Check-in
```

### Users can

- Create an account and log in
- Select a fitness goal
- Enter personal information
- Submit daily fitness information
- Track weight, steps, exercise, sleep, and water
- View a fitness score
- View progress
- Get a personalized plan for the next day
- View previous plans
- Logout

---

## How the Plan Is Generated

```text
Daily User Data
       ↓
   ML Model
       ↓
Activity Level + Fitness Score
       ↓
   AI Fitness Agent
       ↓
Personalized Plan
```

### ML Model

The ML model analyzes:

- Steps
- Exercise duration
- Sleep
- Water intake
- Weight
- Previous activity
- Consistency

It predicts the user's activity level and produces a fitness score.

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
Daily Activity
Previous Data
ML Result
```

and generates a suitable plan for the next day.

> The initial version can use a rule-based fitness engine instead of an external LLM API. An LLM can be integrated later.

---

# 🛠️ Tech Stack

| Component       | Technology     |
| --------------- | -------------- |
| Frontend        | React          |
| Styling         | CSS            |
| Backend         | FastAPI        |
| Language        | Python         |
| Database        | PostgreSQL     |
| ORM             | SQLAlchemy     |
| Authentication  | JWT            |
| ML              | Scikit-learn   |
| Data Processing | Pandas         |
| AI              | AI Agent / LLM |
| Charts          | Recharts       |

---

# 📁 Project Structure

```text
FitAI/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── FitnessPlanCard.jsx
│   │   │   ├── ProgressChart.jsx
│   │   │   ├── GoalCard.jsx
│   │   │   └── Loading.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── GoalSelection.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DailyCheckIn.jsx
│   │   │   ├── TomorrowPlan.jsx
│   │   │   └── Progress.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── activity.py
│   │   │   ├── plans.py
│   │   │   └── progress.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── analysis.py
│   │   │   └── plan.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── activity.py
│   │   │   └── plan.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── fitness_service.py
│   │   │   └── agent_service.py
│   │   ├── ml/
│   │   │   ├── model.pkl
│   │   │   ├── predict.py
│   │   │   └── preprocessing.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── init_db.py
│   │   └── config.py
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
│
├── ml/
│   ├── data/
│   │   └── fitness_data.csv
│   ├── notebooks/
│   │   └── analysis.ipynb
│   ├── src/
│   │   ├── train.py
│   │   ├── preprocess.py
│   │   ├── evaluate.py
│   │   └── predict.py
│   ├── models/
│   │   └── fitness_model.pkl
│   └── requirements.txt
│
├── .gitignore
├── README.md
└── LICENSE
```

---

# Database Structure

Orbitz uses PostgreSQL.

### Users

```text
users
├── id
├── name
├── email
├── password_hash
├── age
├── gender
├── height
├── weight
├── fitness_goal
├── fitness_level
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
├── exercise_minutes
├── exercise_intensity
├── exercise_types
├── sleep_hours
├── water_liters
├── sitting_hours
├── feeling
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
├── date
├── plan
├── reason
└── created_at
```

---

# Data Flow

```text
React Frontend
      │
      │ POST /activity
      ↓
FastAPI Backend
      │
      ├──────────────→ PostgreSQL
      │                    └── Store daily data
      ↓
ML Model
      │
      ├── Activity Level
      └── Fitness Score
      ↓
AI Fitness Agent
      │
      ├── User Goal
      ├── Fitness Level
      ├── Daily Data
      ├── Previous Data
      └── ML Result
      ↓
Tomorrow's Plan
      ↓
PostgreSQL
      ↓
React Frontend
      ├── Tomorrow Plan Page
      └── Dashboard
```

---

# Frontend Pages

## 1. Login

Existing users enter:

```text
Email
Password
```

Buttons:

```text
[ Login ]
[ Let's Begin ]
```

**Login** → Dashboard

**Let's Begin** → Register

---

## 2. Register

New users enter:

```text
Name
Email
Password
Confirm Password
Age
Gender
Height
Weight
```

After registration, the user selects a fitness goal.

---

## 3. Goal Selection

New users choose their main goal:

- 💪 Muscle Gain
- ⚖️ Weight Gain
- 🔥 Weight Loss
- 🏃 Cardio & Endurance
- ❤️ General Fitness

They also select:

- Beginner
- Intermediate
- Advanced

The goal and fitness level are stored in PostgreSQL.

---

## 4. Dashboard

The dashboard is the main page after login.

It displays:

- Fitness Score
- Weight
- Steps
- Exercise time
- Sleep
- Water intake
- Progress
- Tomorrow's personalized plan

The statistics use **asymmetrical cards** instead of a regular grid.

---

## 5. Daily Check-in

The user submits:

```text
Weight
Steps
Exercise duration
Exercise intensity
Exercise type
Sleep
Water
Sitting hours
Feeling
```

Then clicks:

```text
[ Generate Tomorrow's Plan ]
```

---

## 6. Tomorrow's Plan

Example:

```text
TOMORROW'S PLAN

🏋️ Strength
Squats       3 × 10
Push-ups     3 × 8
Lunges       3 × 10

🏃 Activity
20 minute walk

🧘 Recovery
5 minute stretching

💧 Hydration
Target: 2–2.5 L

😴 Sleep
Target: 7–8 hours
```

The plan also appears on the dashboard.

---

## 7. Progress

The progress page shows:

- Weight trend
- Steps trend
- Exercise trend
- Fitness score
- Weekly consistency
- Weekly averages

Charts can be displayed using Recharts.

---

---

# 🔐 Authentication

Orbitz uses JWT-based authentication.

```text
POST /auth/register
POST /auth/login
GET  /auth/me
POST /auth/logout
```

Passwords are stored as hashed passwords.

---

# 🔌 API Structure

### User

```text
GET /users/profile
PUT /users/profile
PUT /users/goal
```

### Daily Activity

```text
POST /activity
GET /activity/today
GET /activity/history
```

### Fitness Analysis

```text
POST /analysis
GET /analysis/latest
```

### Plans

```text
POST /plans/generate
GET  /plans/tomorrow
GET  /plans/history
```

### Progress

```text
GET /progress/weekly
GET /progress/monthly
```

---

# 💻 Local Setup

## Prerequisites

Install:

- Python 3.10+
- Node.js 18+
- PostgreSQL
- Git

Check installations:

```bash
python --version
node --version
npm --version
psql --version
git --version
```

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd FitAI
```

## 2. Create PostgreSQL Database

```sql
CREATE DATABASE fitai;
```

Example connection:

```text
postgresql://postgres:password@localhost:5432/fitai
```

## 3. Backend Setup

```bash
cd backend
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fitai
SECRET_KEY=your_secret_key
```

If an LLM API is added later:

```env
LLM_API_KEY=your_api_key
```

**Never commit `.env` to GitHub.**

## 4. Initialize Database

```bash
python -m app.database.init_db
```

## 5. Start FastAPI

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 6. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🤖 AI Fitness Agent

The agent uses:

```text
User Goal
+
Fitness Level
+
Daily Activity
+
Previous Activity
+
ML Result
```

to create the next day's plan.

The agent should use a controlled set of exercises and fitness rules rather than freely inventing unsafe recommendations.

---

# 🧪 ML Model

The initial ML model can be a **Random Forest Classifier**.

Possible outputs:

```text
LOW
MODERATE
HIGH
```

Possible input features:

```text
steps
exercise_minutes
sleep_hours
water_liters
weight
consistency
```

Training:

```text
fitness_data.csv
      ↓
Preprocessing
      ↓
Train Model
      ↓
Evaluate Model
      ↓
Save Model
      ↓
fitness_model.pkl
```

---

# ⚠️ Safety

Orbitz provides **general fitness recommendations** based on user-provided information.

It is not a medical diagnosis or treatment system.

Users with medical conditions or serious health concerns should consult a qualified healthcare professional.

---

# 🎯 Project Goal

Orbitz makes fitness guidance simple and personalized.

Instead of giving every user the same plan, Orbitz uses their:

- Fitness goal
- Fitness level
- Daily activity
- Sleep
- Water intake
- Weight
- Previous progress

to create a plan that changes as their activity changes.

---

## 📌 Project Summary

```text
Orbitz

User
 ↓
Choose Fitness Goal
 ↓
Daily Check-in
 ↓
PostgreSQL
 ↓
ML Analysis
 ↓
AI Fitness Agent
 ↓
Personalized Tomorrow Plan
 ↓
Dashboard
 ↓
Track Progress
 ↓
Repeat
```

is a personalized fitness web application that helps users stay active based on their **fitness goals, daily activity, and progress**.

Users create an account, choose a goal such as **weight gain, weight loss, muscle gain, cardio/endurance, or general fitness**, and submit daily fitness information. The system analyzes the data using an ML model and generates a personalized plan for the next day.

---

## What Orbitz Does

```text
Register / Login
      ↓
Select Fitness Goal
      ↓
Dashboard
      ↓
Daily Check-in
      ↓
Store Daily Data
      ↓
ML Fitness Analysis
      ↓
AI Fitness Agent
      ↓
Generate Tomorrow's Plan
      ↓
Show Plan on Dashboard
      ↓
Next Day Check-in
```

### Users can

- Create an account and log in
- Select a fitness goal
- Enter personal information
- Submit daily fitness information
- Track weight, steps, exercise, sleep, and water
- View a fitness score
- View progress
- Get a personalized plan for the next day
- View previous plans
- Logout

---

## 🧠 How the Plan Is Generated

```text
Daily User Data
       ↓
   ML Model
       ↓
Activity Level + Fitness Score
       ↓
   AI Fitness Agent
       ↓
Personalized Plan
```

### ML Model

The ML model analyzes:

- Steps
- Exercise duration
- Sleep
- Water intake
- Weight
- Previous activity
- Consistency

It predicts the user's activity level and produces a fitness score.

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
Daily Activity
Previous Data
ML Result
```

and generates a suitable plan for the next day.

> The initial version can use a rule-based fitness engine instead of an external LLM API. An LLM can be integrated later.

---

# 🛠️ Tech Stack

| Component       | Technology     |
| --------------- | -------------- |
| Frontend        | React          |
| Styling         | CSS            |
| Backend         | FastAPI        |
| Language        | Python         |
| Database        | PostgreSQL     |
| ORM             | SQLAlchemy     |
| Authentication  | JWT            |
| ML              | Scikit-learn   |
| Data Processing | Pandas         |
| AI              | AI Agent / LLM |
| Charts          | Recharts       |

---

# 📁 Project Structure

```text
FitAI/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── FitnessPlanCard.jsx
│   │   │   ├── ProgressChart.jsx
│   │   │   ├── GoalCard.jsx
│   │   │   └── Loading.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── GoalSelection.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DailyCheckIn.jsx
│   │   │   ├── TomorrowPlan.jsx
│   │   │   └── Progress.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── activity.py
│   │   │   ├── plans.py
│   │   │   └── progress.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── analysis.py
│   │   │   └── plan.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── activity.py
│   │   │   └── plan.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── fitness_service.py
│   │   │   └── agent_service.py
│   │   ├── ml/
│   │   │   ├── model.pkl
│   │   │   ├── predict.py
│   │   │   └── preprocessing.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── init_db.py
│   │   └── config.py
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
│
├── ml/
│   ├── data/
│   │   └── fitness_data.csv
│   ├── notebooks/
│   │   └── analysis.ipynb
│   ├── src/
│   │   ├── train.py
│   │   ├── preprocess.py
│   │   ├── evaluate.py
│   │   └── predict.py
│   ├── models/
│   │   └── fitness_model.pkl
│   └── requirements.txt
│
├── .gitignore
├── README.md
└── LICENSE
```

---

# 🗄️ Database Structure

Orbitz uses PostgreSQL.

### Users

```text
users
├── id
├── name
├── email
├── password_hash
├── age
├── gender
├── height
├── weight
├── fitness_goal
├── fitness_level
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
├── exercise_minutes
├── exercise_intensity
├── exercise_types
├── sleep_hours
├── water_liters
├── sitting_hours
├── feeling
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
├── date
├── plan
├── reason
└── created_at
```

---

# 🔄 Data Flow

```text
React Frontend
      │
      │ POST /activity
      ↓
FastAPI Backend
      │
      ├──────────────→ PostgreSQL
      │                    └── Store daily data
      ↓
ML Model
      │
      ├── Activity Level
      └── Fitness Score
      ↓
AI Fitness Agent
      │
      ├── User Goal
      ├── Fitness Level
      ├── Daily Data
      ├── Previous Data
      └── ML Result
      ↓
Tomorrow's Plan
      ↓
PostgreSQL
      ↓
React Frontend
      ├── Tomorrow Plan Page
      └── Dashboard
```

---

# 🌐 Frontend Pages

## 1. Login

Existing users enter:

```text
Email
Password
```

Buttons:

```text
[ Login ]
[ Let's Begin ]
```

**Login** → Dashboard

**Let's Begin** → Register

---

## 2. Register

New users enter:

```text
Name
Email
Password
Confirm Password
Age
Gender
Height
Weight
```

After registration, the user selects a fitness goal.

---

## 3. Goal Selection

New users choose their main goal:

- 💪 Muscle Gain
- ⚖️ Weight Gain
- 🔥 Weight Loss
- 🏃 Cardio & Endurance
- ❤️ General Fitness

They also select:

- Beginner
- Intermediate
- Advanced

The goal and fitness level are stored in PostgreSQL.

---

## 4. Dashboard

The dashboard is the main page after login.

It displays:

- Fitness Score
- Weight
- Steps
- Exercise time
- Sleep
- Water intake
- Progress
- Tomorrow's personalized plan

The statistics use **asymmetrical cards** instead of a regular grid.

---

## 5. Daily Check-in

The user submits:

```text
Weight
Steps
Exercise duration
Exercise intensity
Exercise type
Sleep
Water
Sitting hours
Feeling
```

Then clicks:

```text
[ Generate Tomorrow's Plan ]
```

---

## 6. Tomorrow's Plan

Example:

```text
TOMORROW'S PLAN

🏋️ Strength
Squats       3 × 10
Push-ups     3 × 8
Lunges       3 × 10

🏃 Activity
20 minute walk

🧘 Recovery
5 minute stretching

💧 Hydration
Target: 2–2.5 L

😴 Sleep
Target: 7–8 hours
```

The plan also appears on the dashboard.

---

## 7. Progress

The progress page shows:

- Weight trend
- Steps trend
- Exercise trend
- Fitness score
- Weekly consistency
- Weekly averages

Charts can be displayed using Recharts.

---

---

# 🔐 Authentication

Orbitz uses JWT-based authentication.

```text
POST /auth/register
POST /auth/login
GET  /auth/me
POST /auth/logout
```

Passwords are stored as hashed passwords.

---

# 🔌 API Structure

### User

```text
GET /users/profile
PUT /users/profile
PUT /users/goal
```

### Daily Activity

```text
POST /activity
GET /activity/today
GET /activity/history
```

### Fitness Analysis

```text
POST /analysis
GET /analysis/latest
```

### Plans

```text
POST /plans/generate
GET  /plans/tomorrow
GET  /plans/history
```

### Progress

```text
GET /progress/weekly
GET /progress/monthly
```

---

# 💻 Local Setup

## Prerequisites

Install:

- Python 3.10+
- Node.js 18+
- PostgreSQL
- Git

Check installations:

```bash
python --version
node --version
npm --version
psql --version
git --version
```

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd FitAI
```

## 2. Create PostgreSQL Database

```sql
CREATE DATABASE fitai;
```

Example connection:

```text
postgresql://postgres:password@localhost:5432/fitai
```

## 3. Backend Setup

```bash
cd backend
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fitai
SECRET_KEY=your_secret_key
```

If an LLM API is added later:

```env
LLM_API_KEY=your_api_key
```

**Never commit `.env` to GitHub.**

## 4. Initialize Database

```bash
python -m app.database.init_db
```

## 5. Start FastAPI

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 6. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🤖 AI Fitness Agent

The agent uses:

```text
User Goal
+
Fitness Level
+
Daily Activity
+
Previous Activity
+
ML Result
```

to create the next day's plan.

The agent should use a controlled set of exercises and fitness rules rather than freely inventing unsafe recommendations.

---

# 🧪 ML Model

The initial ML model can be a **Random Forest Classifier**.

Possible outputs:

```text
LOW
MODERATE
HIGH
```

Possible input features:

```text
steps
exercise_minutes
sleep_hours
water_liters
weight
consistency
```

Training:

```text
fitness_data.csv
      ↓
Preprocessing
      ↓
Train Model
      ↓
Evaluate Model
      ↓
Save Model
      ↓
fitness_model.pkl
```

---

# ⚠️ Safety

Orbitz provides **general fitness recommendations** based on user-provided information.

It is not a medical diagnosis or treatment system.

Users with medical conditions or serious health concerns should consult a qualified healthcare professional.

---

# 🎯 Project Goal

Orbitz makes fitness guidance simple and personalized.

Instead of giving every user the same plan, Orbitz uses their:

- Fitness goal
- Fitness level
- Daily activity
- Sleep
- Water intake
- Weight
- Previous progress

to create a plan that changes as their activity changes.

---

## 📌 Project Summary

```text
Orbitz

User
 ↓
Choose Fitness Goal
 ↓
Daily Check-in
 ↓
PostgreSQL
 ↓
ML Analysis
 ↓
AI Fitness Agent
 ↓
Personalized Tomorrow Plan
 ↓
Dashboard
 ↓
Track Progress
 ↓
Repeat
```
