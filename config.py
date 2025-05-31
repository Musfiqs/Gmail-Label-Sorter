from typing import Dict, List

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# OAuth2 credentials
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# Logging configuration
LOG_FILE = 'gmail_labeler.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Email fetch settings
MAX_EMAILS = 250
CHECK_INTERVAL = 60  # seconds

# Email classification rules - using Gmail-friendly label names
CLASSIFICATION_RULES = {
    'AutoSort-Tech': [
        '@apple.com', '@google.com', '@github.com', '@microsoft.com',
        'tech', 'software', 'update', 'developer'
    ],
    'AutoSort-School': [
        '@edu', 'class', 'homework', 'assignment', 'course', 'lecture',
        'professor', 'student'
    ],
    'AutoSort-Finance': [
        'bank', 'transfer', 'transaction', 'balance', 'statement',
        'investment', 'finance',
        'ninjatrader', 'topstep', 'trading', 'trader', 'futures', 'forex', 'stocks', 'equity',
        'portfolio', 'profit', 'loss', 'margin', 'broker', 'brokerage', 'account balance',
        'trade', 'buy', 'sell', 'market', 'position', 'capital', 'funding', 'withdrawal',
        'deposit', 'commission', 'fee', 'pnl', 'p&l'
    ],
    'AutoSort-Subscriptions': [
        'subscription', 'unsubscribe', 'newsletter', 'weekly update',
        'monthly update'
    ],
    'AutoSort-Receipts': [
        'receipt', 'invoice', 'order', 'payment', 'confirmation',
        'purchased', 'delivery'
    ]
}

# Default label for unclassified emails - set to None to skip labeling
DEFAULT_LABEL = None 