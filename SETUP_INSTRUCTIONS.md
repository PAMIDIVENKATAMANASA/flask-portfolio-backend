# Flask Portfolio Backend - Setup Instructions

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Git

## Quick Setup

### 1. Clone the Repository
\`\`\`bash
git clone <your-repository-url>
cd flask-portfolio-backend
\`\`\`

### 2. Create Virtual Environment (Recommended)
\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Run the Application
\`\`\`bash
python app.py
\`\`\`

The server will start on `http://localhost:5000`

### 5. Test the APIs

#### Option 1: Web Interface
Open your browser and go to `http://localhost:5000` to access the complete testing frontend.

#### Option 2: Postman
1. Import the `postman_collection.json` file into Postman
2. Set the base_url variable to `http://localhost:5000`
3. Test all endpoints

#### Option 3: cURL Commands
\`\`\`bash
# Test resume parser
curl -X POST -F "resume=@sample_resume.pdf" http://localhost:5000/api/parse-resume

# Test translation
curl -X POST -H "Content-Type: application/json" \
  -d '{"content":"Hello World","target_language":"es"}' \
  http://localhost:5000/api/translate

# Test currency conversion
curl "http://localhost:5000/api/convert-currency?price=100&country=IN&base_currency=USD"
\`\`\`

## Project Structure
\`\`\`
flask-portfolio-backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── modules/                    # Backend modules
│   ├── __init__.py
│   ├── resume_parser.py        # Resume parsing logic
│   ├── translator.py           # Translation functionality
│   └── currency_converter.py   # Currency conversion
├── frontend/
│   └── index.html             # Testing frontend
├── uploads/                   # Temporary uploads (auto-created)
├── postman_collection.json    # Postman API collection
├── API_DOCUMENTATION.md       # API documentation
└── README.md                  # Project documentation
\`\`\`

## Environment Configuration

### Optional Environment Variables
Create a `.env` file for production settings:
\`\`\`bash
FLASK_ENV=production
FLASK_DEBUG=False
MAX_CONTENT_LENGTH=16777216  # 16MB
\`\`\`

### Production Considerations
1. **API Keys**: Add real API keys for translation and currency services
2. **Database**: Consider adding database for caching
3. **Authentication**: Implement API authentication
4. **Rate Limiting**: Add rate limiting for production
5. **HTTPS**: Use HTTPS in production
6. **Error Logging**: Implement proper logging

## Troubleshooting

### Common Issues

#### 1. Module Import Errors
\`\`\`bash
# Ensure you're in the project directory and virtual environment is activated
pip install -r requirements.txt
\`\`\`

#### 2. File Upload Issues
- Check file size (max 16MB)
- Ensure file format is PDF, DOC, or DOCX
- Verify uploads folder permissions

#### 3. Translation Errors
- Check internet connection
- Translation service may have rate limits
- Fallback to static responses if API fails

#### 4. Currency Conversion Issues
- API might have rate limits
- System falls back to static exchange rates
- Check country code format (US, IN, GB, etc.)

### Port Already in Use
If port 5000 is busy:
\`\`\`bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
\`\`\`

### Dependencies Issues
\`\`\`bash
# Upgrade pip
pip install --upgrade pip

# Install specific versions
pip install Flask==2.3.3
\`\`\`

## Testing

### Manual Testing
1. Start the server: `python app.py`
2. Open `http://localhost:5000`
3. Test each feature using the web interface

### API Testing
1. Import Postman collection
2. Run all requests in the collection
3. Verify responses match expected format

### File Testing
Test with various resume formats:
- PDF resumes
- DOC/DOCX files
- Different resume layouts
- Various file sizes

## Deployment

### Local Development
\`\`\`bash
python app.py
\`\`\`

### Production Deployment
1. Set environment variables
2. Use production WSGI server (gunicorn)
3. Configure reverse proxy (nginx)
4. Set up SSL certificates
5. Implement monitoring and logging

## Support
For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Test with provided Postman collection
4. Verify all dependencies are installed correctly
