from passlib.hash import pbkdf2_sha256
from models.database import User, db
import secrets
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
import re

class PasswordAuth:
    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password, hash):
        return pbkdf2_sha256.verify(password, hash)

    def validate_email(self, email):
        """Validate email format"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))

    def validate_username(self, username):
        """Validate username format"""
        # Username should be 3-20 characters, alphanumeric and underscores only
        username_pattern = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
        return bool(username_pattern.match(username))

    def create_user(self, email, username, password):
        """Create a new user with email/password authentication."""
        try:
            if not self.validate_email(email):
                raise ValueError("Invalid email format")

            if not self.validate_username(username):
                raise ValueError("Username must be 3-20 characters, alphanumeric and underscores only")

            existing_user = db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()

            if existing_user:
                raise ValueError("Email or username already exists")

            user = User(
                email=email,
                username=username,
                password_hash=self.hash_password(password),
                is_google_auth=False
            )
            db.add(user)
            db.commit()
            return user

        except Exception as e:
            db.rollback()
            raise ValueError(str(e))

    def authenticate_user(self, username_or_email, password):
        """Authenticate a user with username/email and password."""
        try:
            # Check if input is email or username
            is_email = '@' in username_or_email

            if is_email and not self.validate_email(username_or_email):
                raise ValueError("Invalid email format")

            user = db.query(User).filter(
                User.email == username_or_email if is_email else User.username == username_or_email
            ).first()

            if user and not user.is_google_auth and self.verify_password(password, user.password_hash):
                db.commit()
                return user
            db.rollback()
            return None

        except Exception as e:
            db.rollback()
            raise ValueError(str(e))

    def generate_reset_token(self, email):
        """Generate a password reset token for the user."""
        try:
            if not self.validate_email(email):
                raise ValueError("Invalid email format")

            user = db.query(User).filter_by(email=email).first()
            if user:
                token = secrets.token_urlsafe(32)
                user.reset_token = token
                user.reset_token_expiry = datetime.utcnow() + timedelta(hours=24)
                db.commit()
                return token
            return None

        except Exception as e:
            db.rollback()
            raise ValueError(str(e))

    def verify_reset_token(self, token):
        """Verify if the reset token is valid."""
        try:
            user = db.query(User).filter_by(reset_token=token).first()
            if user and user.reset_token_expiry > datetime.utcnow():
                return user
            return None

        except Exception as e:
            db.rollback()
            raise ValueError(str(e))

    def reset_password(self, token, new_password):
        """Reset user's password using the token."""
        try:
            user = self.verify_reset_token(token)
            if user:
                user.password_hash = self.hash_password(new_password)
                user.reset_token = None
                user.reset_token_expiry = None
                db.commit()
                return True
            return False

        except Exception as e:
            db.rollback()
            raise ValueError(str(e))