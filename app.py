from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///topics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- Model --------------------
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f'<Topic {self.title}>'

# Auto-create database tables on startup (safe on Render)
with app.app_context():
    db.create_all()

# -------------------- Helper Function --------------------
def first_review_date(added_date: date) -> date:
    """
    Your exact weekend-skipping rule for first review:
    Mon → Wed (+2), Tue → Thu (+2), Wed → Fri (+2)
    Thu → Mon (+4), Fri → Tue (+4)
    """
    weekday = added_date.weekday()  # 0=Mon, 1=Tue, ..., 4=Fri
    if weekday <= 2:  # Monday, Tuesday, Wednesday
        return added_date + timedelta(days=2)
    else:  # Thursday or Friday
        return added_date + timedelta(days=4)

# -------------------- Routes --------------------
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/enter-topic', methods=['GET', 'POST'])
def enter_topic():
    if request.method == '
