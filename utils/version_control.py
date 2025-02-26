from datetime import datetime
import json

class VersionControl:
    def __init__(self):
        self.versions = {}
        self.audit_trail = []

    def create_version(self, policy_id, content, user):
        """Create a new version of a policy."""
        if policy_id not in self.versions:
            self.versions[policy_id] = []
            
        version_number = len(self.versions[policy_id]) + 1
        version = {
            'version': version_number,
            'content': content,
            'timestamp': datetime.now(),
            'user': user
        }
        self.versions[policy_id].append(version)
        
        # Add to audit trail
        self.audit_trail.append({
            'policy_id': policy_id,
            'action': 'create_version',
            'version': version_number,
            'user': user,
            'timestamp': datetime.now()
        })
        
        return version_number

    def get_version(self, policy_id, version_number):
        """Get a specific version of a policy."""
        if policy_id in self.versions:
            versions = self.versions[policy_id]
            if 1 <= version_number <= len(versions):
                return versions[version_number - 1]
        return None

    def get_version_history(self, policy_id):
        """Get the version history of a policy."""
        return self.versions.get(policy_id, [])

    def get_audit_trail(self, policy_id=None):
        """Get the audit trail for a policy or all policies."""
        if policy_id:
            return [
                entry for entry in self.audit_trail
                if entry['policy_id'] == policy_id
            ]
        return self.audit_trail
