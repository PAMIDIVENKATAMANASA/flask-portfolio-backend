# Flask Portfolio Backend API

A complete, dynamic, and modular Python Flask backend project with the following features:

## Features

1. **Portfolio Website Generation from Resume (PDF/DOC)**
   - Upload resume files (PDF, DOC, DOCX)
   - Extract structured data: Name, Email, Phone, Skills, Experience, Education
   - Return JSON data for portfolio website population

2. **Multi-Lingual Website Support**
   - Translate website content to 19+ languages
   - Dynamic translation using Google Translate API
   - Support for long text with automatic chunking

3. **Multi-Currency Pricing Display**
   - Convert prices based on user's country
   - Support for 25+ countries and currencies
   - Real-time exchange rates with fallback static rates

4. **Frontend Testing Interface**
   - Complete HTML + JavaScript testing interface
   - File upload for resume parsing
   - Translation form with language selection
   - Currency conversion with country selection


## Setup Instructions

### 1. Install Python Dependencies


pip install -r requirements.txt


### 2. Run the Flask Server


python app.py


The server will start on `http://localhost:5000`

### 3. Test the APIs

Open your browser and go to `http://localhost:5000` to access the testing frontend.

## API Endpoints

### Resume Parser
- **POST** `/api/parse-resume`
- Upload a resume file and get structured JSON data

### Translation
- **POST** `/api/translate`
- Translate content to target language
- Body: `{"content": "text", "target_language": "es"}`

### Currency Conversion
- **GET** `/api/convert-currency?price=100&country=IN&base_currency=USD`
- Convert price to local currency based on country

### Helper Endpoints
- **GET** `/api/supported-languages` - Get supported languages
- **GET** `/api/supported-countries` - Get supported countries

## Usage Examples

### Resume Parsing
```python
import requests

files = {'resume': open('resume.pdf', 'rb')}
response = requests.post('http://localhost:5000/api/parse-resume', files=files)
data = response.json()
