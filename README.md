# EchoLearn – Spaced Repetition Learning Tool

**Live Demo:** https://echolearn-2voe.onrender.com  
**GitHub Profile:** https://github.com/lbedroske

## Overview
EchoLearn is a full-stack web prototype I designed to help teachers automate spaced-repetition review scheduling. Inspired by my classroom teaching experience and the Ebbinghaus Forgetting Curve, it generates personalized intervals (2, 4, 14, 35 days) with weekend adjustments, allowing flexible, data-driven review plans.

Built as a school pilot tool to tackle real retention issues—simple entry for topics, automatic scheduling, and persistent tracking.

## Key Features
- Topic entry and review date calculation
- Weekend-aware interval logic
- User-friendly interface for educators
- SQLite persistence for review history

## Tech Stack
- Python (core algorithm and scripting)
- Flask (web framework)
- SQLAlchemy ORM (SQLite database)
- HTML/CSS (frontend styling)
- Render (hosting and deployment)

## Development Approach
The concept, requirements, interval algorithm, testing, and deployment were driven by my educational background. I used generative AI tools for rapid code prototyping and boilerplate generation, then personally reviewed, customized, integrated, and refined all logic to ensure pedagogical fit and functionality.

## Setup (Local Run)
1. Clone: `git clone https://github.com/lbedroske/EchoLearn.git`
2. Install: `pip install -r requirements.txt`
3. Run: `python app.py`  
   Visit http://localhost:5000

Open to feedback or small improvements—this is an ongoing pilot!
