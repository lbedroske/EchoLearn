from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///topics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- Models --------------------

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f'<Topic {self.title}>'

# -------------------- Routes --------------------

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
            date_added_str = request.form['date_added']
            date_added = date.fromisoformat(date_added_str)  # Cleaner than strptime
            new_topic = Topic(title=title, description=description, date_added=date_added)
            db.session.add(new_topic)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error adding topic: {e}", 500
    return render_template('enter_missing_topic.html')

# Main review page — accessible from both URLs
@app.route('/review-top
