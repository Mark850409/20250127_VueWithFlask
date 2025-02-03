from datetime import datetime
from models.database import db

class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    normalized_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    budget = db.Column(db.Float)
    city = db.Column(db.String(50), nullable=False)
    city_CN = db.Column(db.String(50), nullable=False)
    customer_phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    hero_image = db.Column(db.String(255))
    hero_listing_image = db.Column(db.String(255))
    distance = db.Column(db.Float)
    is_new_until = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    minimum_delivery_fee = db.Column(db.Float)
    minimum_delivery_time = db.Column(db.Integer)
    minimum_order_amount = db.Column(db.Float)
    minimum_pickup_time = db.Column(db.Integer)
    primary_cuisine_id = db.Column(db.String(50))
    rating = db.Column(db.Float)
    redirection_url = db.Column(db.String(255))
    review_number = db.Column(db.Integer)
    tag = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯定義
    ratings = db.relationship(
        'Rating',
        backref='store',
        lazy=True,
        cascade="all, delete-orphan",
        primaryjoin="and_(Store.id==Rating.store_id, Rating.status!='deleted')"
    )
    
    comments = db.relationship(
        'Comment',
        backref='store',
        lazy=True,
        cascade="all, delete-orphan",
        primaryjoin="and_(Store.id==Comment.store_id, Comment.status!='deleted')"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'normalized_name': self.normalized_name,
            'address': self.address,
            'budget': self.budget,
            'city': self.city,
            'city_CN': self.city_CN,
            'customer_phone': self.customer_phone,
            'description': self.description,
            'hero_image': self.hero_image,
            'hero_listing_image': self.hero_listing_image,
            'distance': self.distance,
            'is_new_until': self.is_new_until.isoformat() if self.is_new_until else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'minimum_delivery_fee': self.minimum_delivery_fee,
            'minimum_delivery_time': self.minimum_delivery_time,
            'minimum_order_amount': self.minimum_order_amount,
            'minimum_pickup_time': self.minimum_pickup_time,
            'primary_cuisine_id': self.primary_cuisine_id,
            'rating': self.rating,
            'redirection_url': self.redirection_url,
            'review_number': self.review_number,
            'tag': self.tag,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def get_average_rating(self):
        active_ratings = [r for r in self.ratings if r.status == 'active']
        if not active_ratings:
            return 0
        return round(sum(float(r.score) for r in active_ratings) / len(active_ratings), 1) 