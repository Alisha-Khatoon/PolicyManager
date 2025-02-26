
import os
from models.database import db, GovernmentPolicy
from utils.government_api import GovernmentPolicyAPI

def populate_government_policies():
    api = GovernmentPolicyAPI()
    
    # Fetch policies from different categories
    categories = ["Environmental", "Labor", "Healthcare", "Transportation", "Education"]
    
    for category in categories:
        policies = api.search_policies(category)
        for policy in policies:
            gov_policy = GovernmentPolicy(
                title=policy['title'],
                content=policy.get('content', policy.get('summary', '')),
                category=category,
                jurisdiction='Federal',
                effective_date=policy.get('published_date')
            )
            db.add(gov_policy)
    
    try:
        db.commit()
        print("Successfully populated government policies")
    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")

if __name__ == "__main__":
    populate_government_policies()
