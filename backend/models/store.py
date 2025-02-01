from datetime import datetime
from models.database import db
import pytz

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    business_hours = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz), onupdate=lambda: datetime.now(tw_tz))

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
            'address': self.address,
            'city': self.city,
            'phone': self.phone,
            'business_hours': self.business_hours,
            'description': self.description,
            'image_url': self.image_url,
            'status': self.status,
            'views': self.views,
            'avg_rating': self.get_average_rating(),
            'rating_count': len(self.ratings),
            'comment_count': len(self.comments),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

    def get_average_rating(self):
        active_ratings = [r for r in self.ratings if r.status == 'active']
        if not active_ratings:
            return 0
        return round(sum(float(r.score) for r in active_ratings) / len(active_ratings), 1) 