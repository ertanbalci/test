from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
 
login = LoginManager()
db = SQLAlchemy()
 
class MemberModel(db.Model, UserMixin):
    __tablename__ = 'members' 
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(15), unique=True)
    eposta    = db.Column(db.String(40))
    hashed_pw = db.Column(db.String()) 
 
    def hash_password(self,pw):
        self.hashed_pw = generate_password_hash(pw)
     
    def control_password(self,pw):
        return check_password_hash(self.hashed_pw, pw)
 
@login.user_loader
def load_user(id):
    return MemberModel.query.get(int(id))
