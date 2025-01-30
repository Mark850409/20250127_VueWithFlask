from dao.user_dao import UserDAO
from utils.password_util import hash_password

class UserService:
    def __init__(self):
        self.dao = UserDAO()
    
    def get_all_users(self):
        return self.dao.get_all_users()
    
    def get_user(self, user_id):
        return self.dao.get_user_by_id(user_id)
    
    def create_user(self, user_data):
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        return self.dao.create_user(user_data)
    
    def update_user(self, user_id, user_data):
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        return self.dao.update_user(user_id, user_data)
    
    def delete_user(self, user_id):
        return self.dao.delete_user(user_id) 