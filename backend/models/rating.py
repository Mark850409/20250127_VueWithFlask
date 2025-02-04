from datetime import datetime
from models.database import db
import pytz

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String(500), nullable=False)
    restaurant_name = db.Column(db.String(200), nullable=False)
    user = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    text = db.Column(db.String(2000))
    english_texts = db.Column(db.String(2000))
    time = db.Column(db.String(50))
    positive_prob = db.Column(db.Float)
    negative_prob = db.Column(db.Float)
    composite_score = db.Column(db.Float)
    confidence = db.Column(db.Float)
    keywords_scores = db.Column(db.Float)
    sentiment = db.Column(db.String(500))
    hash = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'restaurant_name': self.restaurant_name,
            'user': self.user,
            'rating': self.rating,
            'text': self.text,
            'english_texts': self.english_texts,
            'time': self.time,
            'positive_prob': self.positive_prob,
            'negative_prob': self.negative_prob,
            'composite_score': self.composite_score,
            'confidence': self.confidence,
            'keywords_scores': self.keywords_scores,
            'sentiment': self.sentiment,
            'hash': self.hash
        } 