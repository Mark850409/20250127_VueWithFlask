from models.database import db

class RecommendData(db.Model):
    __tablename__ = 'recommend_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float)
    distance = db.Column(db.Float)
    review_number = db.Column(db.Integer)
    sentiment_score = db.Column(db.Float)
    weighted_score = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'rating': self.rating,
            'distance': self.distance,
            'review_number': self.review_number,
            'sentiment_score': self.sentiment_score,
            'weighted_score': self.weighted_score
        } 