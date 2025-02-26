from google.oauth2 import id_token
from google.auth.transport import requests
from models.database import User, db
import os
from sqlalchemy.exc import SQLAlchemyError

class GoogleAuth:
    def __init__(self):
        self.client_id = os.environ.get('GOOGLE_CLIENT_ID')

    def verify_google_token(self, token):
        """Verify the Google OAuth token."""
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                self.client_id
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid issuer')

            return {
                'email': idinfo['email'],
                'sub': idinfo['sub']
            }
        except Exception as e:
            raise ValueError(f"Invalid token: {str(e)}")

    def get_or_create_user(self, google_info):
        """Get existing user or create new one from Google authentication."""
        try:
            user = db.query(User).filter_by(email=google_info['email']).first()

            if not user:
                user = User(
                    email=google_info['email'],
                    username=google_info['email'].split('@')[0],
                    is_google_auth=True
                )
                db.add(user)
                db.commit()
            return user

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error with Google authentication: {str(e)}")