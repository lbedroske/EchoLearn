from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///topics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.Date, nullable=False, default=date.today)

with app.app_context():
    db.create_all()

def first_review_date(added_date: date) -> date:
    weekday = added_date.weekday()
    if weekday <= 2:  # Mon, Tue, Wed → +2 days
        return added_date + timedelta(days=2)
    else:             # Thu, Fri → +4 days (skip weekend)
        return added_date + timedelta(days=4)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/enter-topic', methods=['GET', 'POST'])
def enter_topic():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        new_topic = Topic(title=title, description=description)
        db.session.add(new_topic)
        db.session.commit()
        return redirect('/')
    return render_template('enter_topic.html')

@app.route('/enter-missing-topic', methods=['GET', 'POST'])
def enter_missing_topic():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form.get('description', '')
            date_added = date.fromisoformat(request.form['date_added'])
            new_topic = Topic(title=title, description=description, date_added=date_added)
            db.session.add(new_topic)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}", 500
    return render_template('enter_missing_topic.html')

@app.route('/review-topics')
@app.route('/review-scheduled-topics')
def review_topics():
    today = date.today()
    all_topics = Topic.query.order_by(Topic.date_added).all()

    short_term = [t for t in all_topics if first_review_date(t.date_added) == today]
    medium_term = Topic.query.filter(Topic.date_added == today - timedelta(days=14)).order_by(Topic.title).all()
    long_term = Topic.query.filter(Topic.date_added == today - timedelta(days=35)).order_by(Topic.title).all()

    return render_template(
        'review_topics.html',
        short_term=short_term,
        medium_term=medium_term,
        long_term=long_term,
        today=today
    )



