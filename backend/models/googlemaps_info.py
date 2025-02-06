from models.database import db
from datetime import datetime

class GoogleMapsInfo(db.Model):
    __tablename__ = 'googlemaps_info'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    place_id = db.Column(db.String(255), unique=True)
    place_names = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=True)
    city_CN = db.Column(db.Text, nullable=True)
    redirection_url = db.Column(db.Text, nullable=True)
    navigation_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'place_names': self.place_names,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'city': self.city,
            'city_CN': self.city_CN,
            'redirection_url': self.redirection_url,
            'navigation_url': self.navigation_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 