from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
from modules.resume_parser import ResumeParser
from modules.translator import Translator
from modules.currency_converter import CurrencyConverter
from modules.ai_agent import FacebookGrowthAgent
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize modules
resume_parser = ResumeParser()
translator = Translator()
currency_converter = CurrencyConverter()
ai_agent = FacebookGrowthAgent()

@app.route('/api/analyze-business', methods=['POST'])
def analyze_business():
    """Analyze business from website URL and generate content strategy"""
    try:
        data = request.get_json()
        
        if not data or 'website_url' not in data:
            return jsonify({'error': 'Website URL is required'}), 400
        
        website_url = data['website_url']
        industry_hint = data.get('industry')
        
        # Scrape and analyze website
        website_data = ai_agent.scrape_website_content(website_url)
        business_analysis = ai_agent.analyze_business(website_data, industry_hint)
        
        # Generate content ideas
        tone = data.get('tone', 'friendly')
        content_ideas = ai_agent.generate_content_ideas(business_analysis, tone)
        
        return jsonify({
            'success': True,
            'website_data': website_data,
            'business_analysis': business_analysis,
            'content_ideas': content_ideas,
            'message': 'Business analysis completed successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/content-planner', methods=['POST'])
def create_content_planner():
    """Create content calendar based on user preferences"""
    try:
        data = request.get_json()
        
        required_fields = ['website_url', 'frequency']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'website_url and frequency are required'}), 400
        
        website_url = data['website_url']
        frequency = data['frequency']
        tone = data.get('tone', 'friendly')
        post_mix = data.get('post_mix', {'educational': 40, 'promotional': 30, 'newsy': 30})
        industry_hint = data.get('industry')
        
        # Analyze business and generate content
        website_data = ai_agent.scrape_website_content(website_url)
        business_analysis = ai_agent.analyze_business(website_data, industry_hint)
        content_ideas = ai_agent.generate_content_ideas(business_analysis, tone)
        
        # Create content calendar
        calendar = ai_agent.create_content_calendar(content_ideas, frequency, tone, post_mix)
        
        return jsonify({
            'success': True,
            'business_analysis': business_analysis,
            'content_calendar': calendar,
            'calendar_summary': {
                'total_posts': len(calendar),
                'frequency': frequency,
                'tone': tone,
                'post_mix': post_mix,
                'date_range': {
                    'start': calendar[0]['date'] if calendar else None,
                    'end': calendar[-1]['date'] if calendar else None
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview-post/<post_id>', methods=['GET'])
def preview_post(post_id):
    """Preview a specific post from the calendar"""
    try:
        # In a real application, you'd fetch from database
        # For demo, we'll generate a sample post
        sample_post = {
            'id': post_id,
            'date': '2024-02-15',
            'day': 'Thursday',
            'time': '10:00',
            'category': 'Business Tips',
            'type': 'educational',
            'content': '💡 Pro Tip: Customer feedback is your most valuable asset. What\'s your experience with this? Share below! #BusinessTips #Growth',
            'tone': 'friendly',
            'status': 'scheduled',
            'engagement_prediction': {'likes': 30, 'comments': 6, 'shares': 4},
            'hashtags': ['#BusinessTips', '#Growth', '#SmallBusiness'],
            'preview_url': f'https://facebook.com/preview/{post_id}'
        }
        
        return jsonify({
            'success': True,
            'post': sample_post
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/edit-post/<post_id>', methods=['PUT'])
def edit_post(post_id):
    """Edit a post before publishing"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Post data is required'}), 400
        
        # In a real application, you'd update the database
        updated_post = {
            'id': post_id,
            'date': data.get('date'),
            'time': data.get('time'),
            'content': data.get('content'),
            'tone': data.get('tone'),
            'category': data.get('category'),
            'status': 'updated',
            'last_modified': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Post updated successfully',
            'post': updated_post
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/publish-post', methods=['POST'])
def publish_post():
    """Simulate publishing post to Facebook"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Post content is required'}), 400
        
        # Simulate Facebook posting
        post_result = ai_agent.simulate_facebook_posting(data)
        
        return jsonify({
            'success': True,
            'message': 'Post published successfully to Facebook',
            'post_result': post_result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bulk-schedule', methods=['POST'])
def bulk_schedule_posts():
    """Schedule multiple posts for publishing"""
    try:
        data = request.get_json()
        
        if not data or 'posts' not in data:
            return jsonify({'error': 'Posts array is required'}), 400
        
        posts = data['posts']
        scheduled_posts = []
        
        for post in posts:
            # Simulate scheduling
            scheduled_post = {
                'id': post.get('id'),
                'content': post.get('content'),
                'scheduled_time': post.get('date') + ' ' + post.get('time', '10:00'),
                'status': 'scheduled',
                'platform': 'Facebook'
            }
            scheduled_posts.append(scheduled_post)
        
        return jsonify({
            'success': True,
            'message': f'Successfully scheduled {len(scheduled_posts)} posts',
            'scheduled_posts': scheduled_posts
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve the testing frontend"""
    with open('frontend/index.html', 'r') as f:
        return f.read()

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """Parse resume from uploaded PDF/DOC file"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not resume_parser.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOC/DOCX files are allowed'}), 400
        
        # Save uploaded file with safe filename
        import uuid
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        safe_filename = f"{uuid.uuid4().hex}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(filepath)
        
        try:
            # Parse the resume
            parsed_data = resume_parser.parse_resume(filepath)
            
            return jsonify({
                'success': True,
                'data': parsed_data,
                'message': 'Resume parsed successfully'
            })
            
        except Exception as parse_error:
            return jsonify({
                'error': f'Failed to parse resume: {str(parse_error)}',
                'success': False
            }), 500
            
        finally:
            # Always clean up uploaded file
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500

@app.route('/api/translate', methods=['POST'])
def translate_content():
    """Translate website content to target language"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data or 'target_language' not in data:
            return jsonify({'error': 'Content and target_language are required'}), 400
        
        content = data['content']
        target_language = data['target_language']
        source_language = data.get('source_language', 'auto')
        
        translated_content = translator.translate_text(content, target_language, source_language)
        
        return jsonify({
            'success': True,
            'original_content': content,
            'translated_content': translated_content,
            'source_language': source_language,
            'target_language': target_language
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/convert-currency', methods=['GET'])
def convert_currency():
    """Convert price to local currency based on country"""
    try:
        country = request.args.get('country')
        price = request.args.get('price', type=float)
        base_currency = request.args.get('base_currency', 'USD')
        
        if not country or price is None:
            return jsonify({'error': 'Country and price parameters are required'}), 400
        
        converted_price = currency_converter.convert_price(price, country, base_currency)
        
        return jsonify({
            'success': True,
            'original_price': price,
            'base_currency': base_currency,
            'country': country,
            'local_currency': converted_price['currency'],
            'converted_price': converted_price['amount'],
            'exchange_rate': converted_price['rate']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/supported-languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages for translation"""
    return jsonify({
        'success': True,
        'languages': translator.get_supported_languages()
    })

@app.route('/api/supported-countries', methods=['GET'])
def get_supported_countries():
    """Get list of supported countries for currency conversion"""
    return jsonify({
        'success': True,
        'countries': currency_converter.get_supported_countries()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
