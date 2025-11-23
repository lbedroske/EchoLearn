from datetime import date, timedelta

# Smart "first review" date — skips weekends exactly as you wanted
def first_review_date(added_date: date) -> date:
    weekday = added_date.weekday()  # 0=Mon ... 6=Sun
    if weekday <= 2:      # Mon–Wed → +2 days
        return added_date + timedelta(days=2)
    else:                 # Thu–Fri → +4 days (skip weekend)
        return added_date + timedelta(days=4)

@app.route('/review-topics')
@app.route('/review-scheduled-topics')
def review_topics():
    try:
        today = date.today()

        all_topics = Topic.query.order_by(Topic.date_added).all()

        # Short-term: first review (your smart 3-day logic)
        short_term = [
            t for t in all_topics
            if first_review_date(t.date_added) == today
        ]

        # Medium-term: second review (~14 days ago exactly for now)
        medium_term = Topic.query.filter(
            Topic.date_added == today - timedelta(days=14)
        ).order_by(Topic.title).all()

        # Long-term: third review (~35 days ago exactly for now)
        long_term = Topic.query.filter(
            Topic.date_added == today - timedelta(days=35)
        ).order_by(Topic.title).all()

        return render_template(
            'review_topics.html',
            short_term=short_term,
            medium_term=medium_term,
            long_term=long_term,
            today=today
        )

    except Exception as e:
        return f"Error: {str(e)}", 500
