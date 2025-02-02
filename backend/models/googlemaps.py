from models.database import db

class GoogleMapsReview(db.Model):
    __tablename__ = 'google_maps_review_with_selenium_ollama'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_id = db.Column(db.String(500))
    restaurant_name = db.Column(db.String(200))
    user = db.Column(db.String(100))
    rating = db.Column(db.Float)
    text = db.Column(db.String(2000))
    english_texts = db.Column(db.String(2000))
    time = db.Column(db.String(50))
    positive_prob = db.Column(db.Float)
    negative_prob = db.Column(db.Float)
    composite_score = db.Column(db.Float)
    confidence = db.Column(db.Float)
    keywords_scores = db.Column(db.Float)
    sentiment = db.Column(db.String(500))
    hash = db.Column(db.String(500), nullable=False, unique=True)

    def __repr__(self):
        return f'<GoogleMapsReview {self.restaurant_name} - {self.user}>' 