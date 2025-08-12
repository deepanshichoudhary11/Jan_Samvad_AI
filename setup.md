# JanAI Setup Guide

## Quick Start

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask server:
   ```bash
   python main.py
   ```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will run on `http://localhost:3000`

## Demo Credentials

You can use these demo credentials to test the application:

**Login:**
- Email: `iec2022013@iiita.ac.in`
- Password: `password123`

**Alternative users:**
- Email: `iit2022022@iiita.ac.in` / Password: `password123`
- Email: `iec2022087@iiita.ac.in` / Password: `password123`

## Features to Test

1. **Authentication**: Register a new account or login with demo credentials
2. **File Complaint**: Test the AI-powered complaint filing with voice, text, and image inputs
3. **Track Status**: View and filter your submitted complaints
4. **Schemes**: Find relevant government schemes based on your demographics
5. **Helpline**: Get emergency contact numbers by state

## AI Simulation Features

The application includes simulated AI features:
- **Voice Transcription**: Click the microphone button to simulate speech-to-text
- **Image Analysis**: Upload images to see simulated AI analysis
- **Complaint Drafting**: Generate AI-powered complaint drafts

## Troubleshooting

- If the backend fails to start, ensure Python 3.8+ is installed
- If the frontend fails to start, ensure Node.js 14+ is installed
- Check that both servers are running on their respective ports
- Ensure CORS is properly configured (already set up in the backend)

## Project Structure

```
janai/
├── frontend/         # React.js application
├── backend/          # Python Flask server
├── README.md         # Project documentation
└── setup.md          # This setup guide
``` 