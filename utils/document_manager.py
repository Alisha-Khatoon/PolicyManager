import pandas as pd
from datetime import datetime
import json

class DocumentManager:
    def __init__(self):
        self.policies = pd.DataFrame(columns=[
            'id', 'title', 'content', 'department',
            'created_at', 'updated_at', 'version'
        ])
        
    def add_policy(self, title, content, department):
        """Add a new policy document."""
        policy_id = len(self.policies) + 1
        new_policy = {
            'id': policy_id,
            'title': title,
            'content': content,
            'department': department,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'version': 1
        }
        self.policies = pd.concat([
            self.policies,
            pd.DataFrame([new_policy])
        ], ignore_index=True)
        return policy_id

    def update_policy(self, policy_id, content):
        """Update an existing policy."""
        if policy_id in self.policies['id'].values:
            idx = self.policies[self.policies['id'] == policy_id].index[0]
            self.policies.at[idx, 'content'] = content
            self.policies.at[idx, 'updated_at'] = datetime.now()
            self.policies.at[idx, 'version'] += 1
            return True
        return False

    def get_policy(self, policy_id):
        """Retrieve a policy by ID."""
        policy = self.policies[self.policies['id'] == policy_id]
        return policy.to_dict('records')[0] if not policy.empty else None

    def search_policies(self, query, search_type='all'):
        """Search policies by content, title, or department."""
        if search_type == 'title':
            mask = self.policies['title'].str.contains(query, case=False)
        elif search_type == 'content':
            mask = self.policies['content'].str.contains(query, case=False)
        elif search_type == 'department':
            mask = self.policies['department'].str.contains(query, case=False)
        else:  # 'all'
            mask = (
                self.policies['title'].str.contains(query, case=False) |
                self.policies['content'].str.contains(query, case=False) |
                self.policies['department'].str.contains(query, case=False)
            )
        return self.policies[mask].to_dict('records')

    def get_all_policies(self):
        """Get all policies."""
        return self.policies.to_dict('records')
