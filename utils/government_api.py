import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class GovernmentPolicyAPI:
    def __init__(self):
        self.base_url = "https://api.regulations.gov/v4"
        self.api_key = os.environ.get("REGULATIONS_GOV_API_KEY")
        self.search_suggestions = {
            "document_types": ["RULE", "PRORULE", "NOTICE"],
            "agencies": ["EPA", "DOL", "HHS", "DOT", "ED"],
            "topics": ["Environmental", "Labor", "Healthcare", "Transportation", "Education"]
        }

    def fetch_recent_policies(self, days: int = 30, agency: str = None, topic: str = None) -> List[Dict]:
        """Fetch recent government policies with optional filters."""
        try:
            headers = {"X-Api-Key": self.api_key}
            past_date = datetime.now() - timedelta(days=days)

            params = {
                "filter[lastModifiedDate][ge]": past_date.strftime("%Y-%m-%d"),
                "sort": "-lastModifiedDate"
            }

            if agency:
                params["filter[agencyId]"] = agency
            if topic:
                params["filter[topic]"] = topic

            response = requests.get(
                f"{self.base_url}/documents",
                headers=headers,
                params=params
            )
            response.raise_for_status()

            data = response.json().get("data", [])
            return self._format_policies(data)
        except Exception as e:
            print(f"Error fetching government policies: {e}")
            return []

    def search_policies(self, query: str, document_type: str = None) -> List[Dict]:
        """Search for policies with specific criteria."""
        try:
            headers = {"X-Api-Key": self.api_key}
            params = {
                "filter[searchTerm]": query,
                "sort": "-postedDate"
            }

            if document_type:
                params["filter[documentType]"] = document_type

            response = requests.get(
                f"{self.base_url}/documents",
                headers=headers,
                params=params
            )
            response.raise_for_status()

            data = response.json().get("data", [])
            return self._format_policies(data)
        except Exception as e:
            print(f"Error searching policies: {e}")
            return []

    def get_search_suggestions(self) -> Dict:
        """Get search suggestions for better policy search."""
        return self.search_suggestions

    def _format_policies(self, policies: List[Dict]) -> List[Dict]:
        """Format the API response into a consistent structure."""
        formatted = []
        for policy in policies:
            attributes = policy.get("attributes", {})
            formatted.append({
                "id": policy.get("id"),
                "title": attributes.get("title"),
                "agency": attributes.get("agencyName"),
                "document_type": attributes.get("documentType"),
                "summary": attributes.get("summary"),
                "content": attributes.get("content"),
                "published_date": attributes.get("postedDate"),
                "last_modified": attributes.get("lastModifiedDate"),
                "url": attributes.get("fileFormats", [{}])[0].get("fileUrl")
            })
        return formatted

    def get_policy_details(self, policy_id: str) -> Optional[Dict]:
        """Get detailed information about a specific policy."""
        try:
            headers = {"X-Api-Key": self.api_key}
            response = requests.get(
                f"{self.base_url}/documents/{policy_id}",
                headers=headers
            )
            response.raise_for_status()
            
            return response.json().get("data")
        except Exception as e:
            print(f"Error fetching policy details: {e}")
            return None
    
    def analyze_policy_changes(self, old_policy: Dict, new_policy: Dict) -> Dict:
        """Analyze changes between two versions of a policy."""
        try:
            changes = {
                "title_changed": old_policy["title"] != new_policy["title"],
                "content_changes": [],
                "effective_date_changed": False,
                "summary": "No significant changes detected"
            }
            
            # Compare content
            if old_policy.get("content") != new_policy.get("content"):
                changes["content_changes"].append("Policy content has been modified")
            
            # Compare dates
            if old_policy.get("effectiveDate") != new_policy.get("effectiveDate"):
                changes["effective_date_changed"] = True
                changes["summary"] = "Policy effective date has changed"
            
            return changes
        except Exception as e:
            print(f"Error analyzing policy changes: {e}")
            return {"error": str(e)}