import logging
from typing import Dict, Optional
import config

class EmailClassifier:
    def __init__(self):
        self.rules = config.CLASSIFICATION_RULES

    def _extract_email_info(self, email: dict) -> Dict[str, str]:
        """Extract relevant information from email payload."""
        headers = email['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
        
        # Simple content extraction (you might want to enhance this)
        content = ''
        if 'snippet' in email:
            content = email['snippet']

        return {
            'subject': subject.lower(),
            'sender': sender.lower(),
            'content': content.lower()
        }

    def classify_email(self, email: dict) -> str:
        """Classify email based on rules."""
        email_info = self._extract_email_info(email)
        
        for label, keywords in self.rules.items():
            for keyword in keywords:
                if (keyword.lower() in email_info['subject'] or
                    keyword.lower() in email_info['sender'] or
                    keyword.lower() in email_info['content']):
                    return label
        
        return config.DEFAULT_LABEL 