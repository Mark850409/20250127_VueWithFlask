from models.database import db
from datetime import datetime

class RestaurantTypeList(db.Model):
    __tablename__ = 'restaurant_type_list'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
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