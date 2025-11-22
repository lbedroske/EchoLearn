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

# Auto-create tables on startup (safe even if they exist)
with app.app_context():
    db.create_all()

# -------------------- Routes --------------------
@app.route('/')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return f"Dashboard template missing or error: {str(e)}", 500

@app.route('/enter-topic', methods=['GET', 'POST'])
def enter_topic():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        new_topic = Topic(title=title, description=description)
        db.session.add(new_topic)
        db.session.commit()
        return redirect('/')
    try:
        return render_template('enter_topic.html')
    except Exception as e:
        return f"Enter topic template missing or error: {str(e)}", 500

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
            return f"Error adding topic: {e}", 500
    try:
        return render_template('enter_missing_topic.html')
    except Exception as e:
        return f"Enter missing topic template missing or error: {str(e)}", 500

# Both URLs now work perfectly — with error debugging
@app.route('/review-topics')
@app.route('/review-scheduled-topics')
def review_topics():
    try:
        today = date.today()

        recent = Topic.query.filter(
            Topic.date_added == today - timedelta(days=3)
        ).order_by(Topic.title).all()

        medium = Topic.query.filter(
            Topic.date_added == today - timedelta(days=14)
        ).order_by(Topic.title).all()

        long = Topic.query.filter(
            Topic.date_added == today - timedelta(days=35)
        ).order_by(Topic.title).all()

        return render_template(
            'review_topics.html',
            recent=recent,
            medium=medium,
            long=long,
            today=today
        )
    except Exception as e:
        return f"Review topics error (this will show in browser): {str(e)}<br><pre>{str(e.__class__)}: {str(e)}</pre>", 500

# -------------------- Run --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
