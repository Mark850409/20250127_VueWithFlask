from models.database import db
from models.user import User
from models.log import Log
from models.menu import Menu
from models.store import Store
from models.rating import Rating
from models.comment import Comment
from models.admin import Admin
from models.favorite import Favorite
from models.restaurant import RestaurantTypeList

# 確保所有模型都被導入
__all__ = ['db', 'User', 'Log', 'Menu', 'Store', 'Rating', 'Comment', 'Admin', 'Favorite', 'RestaurantTypeList'] 