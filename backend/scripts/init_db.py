from backend.db.session import engine, Base
from backend.models.policy import Policy

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init()
