from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///topics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==================== MODEL ====================
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f'<Topic {self.title}>'


# Create tables automatically on first run (works perfectly on Render)
with app.app_context():
    db.create_all()


# ==================== HELPER ====================
def first_review_date(added_date: date) -> date:
    """Weekend-aware first review (your exact rule)"""
    weekday = added_date.weekday()      # 0 = Monday, 4 = Friday
    if weekday <= 2:                    # Mon, Tue, Wed → +2 days
        return added_date + timedelta(days=2)
    else:                               # Thu, Fri → +4 days (skip weekend)
        return added_date + timedelta(days=4)


# ==================== ROUTES ====================
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/enter-topic', methods=['GET', 'POST'])
def enter_topic():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        new_topic = Topic
