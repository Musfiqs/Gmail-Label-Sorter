# Gmail Auto-Labeler 📧🏷️

An intelligent Python application that automatically categorizes and labels your Gmail emails using keyword matching and the Gmail API. Say goodbye to cluttered inboxes!

## ✨ Features

- **Automatic Email Classification**: Intelligently categorizes emails into predefined labels
- **Custom Label Creation**: Automatically creates and manages Gmail labels
- **Real-time Processing**: Continuously monitors inbox for new emails
- **Keyword-based Matching**: Uses smart keyword detection in subject, sender, and content
- **Background Operation**: Runs silently in the background every 60 seconds
- **Secure Authentication**: Uses OAuth2 for secure Gmail API access
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## 🏷️ Auto-Generated Labels

The application creates and manages these labels:

- **AutoSort-Tech**: Technology-related emails (Apple, Google, GitHub, etc.)
- **AutoSort-Finance**: Financial emails (banking, trading platforms like NinjaTrader, Topstep)
- **AutoSort-School**: Educational emails (universities, assignments, courses)
- **AutoSort-Subscriptions**: Newsletter and subscription emails
- **AutoSort-Receipts**: Purchase confirmations, invoices, and receipts

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Gmail account
- Google Cloud Project with Gmail API enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Musfiqs/Gmail-Label-Sorter.git
   cd Gmail-Label-Sorter
   ```

2. **Install dependencies**
   ```bash
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client apscheduler
   ```

3. **Set up Gmail API credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Gmail API
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Choose "Desktop application"
   - Download the JSON file and save it as `credentials.json` in the project directory

4. **Run the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Customizing Classification Rules

Edit `config.py` to modify classification keywords:
