from app import app, db
from models import User 

def add_user(username, password):
    with app.app_context():
        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists.")
            return

        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()
        print(f"User '{username}' added successfully.")

if __name__ == "__main__":
    # Add your desired user here
    add_user('testuser', 'testpassword')
