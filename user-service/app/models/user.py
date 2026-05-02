from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Returns a readable string representation of the User object (useful for debugging)
    def __repr__(self):
        return f"<User {self.email}>"