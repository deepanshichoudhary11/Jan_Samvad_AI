# Email and AI Setup Guide

## Email Setup

### Gmail Setup (Recommended)
1. Go to your Google Account settings
2. Enable 2-Step Verification if not already enabled
3. Go to Security → App passwords
4. Generate a new app password for "Mail"
5. Use this password in your .env file

### Alternative Email Providers
- **Outlook**: Use your email and password
- **Yahoo**: Use your email and app-specific password

## Gemini AI Setup

### Getting Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Setting Environment Variables
Create a `.env` file in the backend folder with:

```
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Gemini AI Configuration (Required for Voice Emergency Processing)
GEMINI_API_KEY=your-gemini-api-key-here
```

### Voice Emergency Feature Requirements
The new voice emergency feature requires a valid Gemini API key to:
- Detect the language of voice input
- Identify the probable Indian state/region
- Classify emergency type (police, medical, fire, etc.)
- Generate multilingual responses

Without the API key, the voice emergency feature will show "AI service temporarily unavailable".

### Example .env file:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=deepanshichoudhary03@gmail.com
MAIL_PASSWORD=your-app-password
GEMINI_API_KEY=AIzaSyC...your-actual-api-key
```

## Running the Application

1. Make sure you're in the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```
   python main.py
   ```

4. In another terminal, start the frontend:
   ```
   cd frontend
   npm start
   ```

## Troubleshooting

### Email Issues
- Ensure 2FA is enabled for Gmail
- Use App Password, not regular password
- Check that MAIL_USERNAME and MAIL_PASSWORD are correct

### Gemini AI Issues
- Ensure GEMINI_API_KEY is set in .env file
- Restart the backend server after adding the API key
- Check that the API key is valid and has proper permissions