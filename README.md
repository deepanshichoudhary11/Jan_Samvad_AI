# JanAI - India's Hyperlocal Civic Agent

## Project Overview

JanAI is a GenAI-powered, multilingual, and mobile-friendly web application designed to empower citizens in semi-urban and rural India. The platform enables users to report local civic issues, track their resolution, discover relevant government schemes, and access emergency helpline numbers.

## Features

- **File Complaints**: AI-powered complaint filing with voice, text, and image inputs
- **Track Status**: Monitor complaint resolution progress
- **Schemes & Scholarships**: Discover relevant government schemes based on demographics
- **Helpline Numbers**: Access emergency contact information by state
- **Multilingual Support**: Support for English and regional languages
- **Mobile-Friendly**: Responsive design for all devices

## Technology Stack

### Frontend
- React.js (JavaScript ES6+)
- CSS3 with custom design system
- HTML5

### Backend
- Python with Flask
- SQLite database (simulated with JSON files)
- AI model integration placeholders

## Project Structure

```
janai/
├── frontend/         # React.js application
│   ├── public/
│   └── src/
│       ├── components/ # Reusable UI components
│       ├── pages/      # Main pages
│       ├── assets/     # Images, icons, fonts
│       ├── services/   # API call functions
│       └── App.js
├── backend/          # Python Flask server
│   ├── api/          # API endpoint definitions
│   ├── models/       # Data models and schemas
│   ├── services/     # Business logic
│   ├── data/         # Dummy data files
│   └── main.py       # Main application entry point
├── .env.example      # Example environment variables
└── README.md         # Project documentation
```

## Setup Instructions

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

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Complaints
- `POST /api/complaint/file` - File a new complaint
- `GET /api/complaint/status?userId=<id>` - Get user's complaints

### Schemes
- `POST /api/schemes/find` - Find relevant schemes

### Helpline
- `GET /api/helpline?state=<state_name>` - Get helpline numbers by state

## Authors

- **Deepanshi Choudhary** (Email: iec2022013@iiita.ac.in, Phone: +91-7906853153)
- **Dimple Bhondekar** (Email: iit2022022@iiita.ac.in, Phone: +91-7972920270)
- **Poonam Gate** (Email: iec2022087@iiita.ac.in, Phone: +91-8824699335)

## Contact

For general inquiries: contact@janai.example.com

## License

This project is developed for educational and demonstration purposes. 
