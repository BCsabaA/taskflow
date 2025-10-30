from __future__ import annotations
from datetime import datetime, UTC
from . import db, login_manager

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=UTC), nullable=False)
    settings = db.relationship("UserSettings", backref="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))

class UserSettings(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    default_list_id = db.Column(db.Integer)        # később idegen kulcs List-re
    default_priority = db.Column(db.Integer, default=2)  # 1..3
    default_status = db.Column(db.String(20), default="TODO")  # TODO/DOING/DONE
    default_due_days = db.Column(db.Integer, default=0)  # pl. gyors rögzítés +N nap
    quick_add_fields = db.Column(db.Text)          # JSON list of field names