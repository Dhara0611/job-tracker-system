from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    
#adding role to the model to identify user and admin
    role = db.Column(db.String(20), nullable=False, server_default="user")

# Returns a readable string representation of the User object (useful for debugging)
    def __repr__(self):
        return f"<User {self.email}>"