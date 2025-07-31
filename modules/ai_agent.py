import requests
from bs4 import BeautifulSoup
import re
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

class FacebookGrowthAgent:
    def __init__(self):
        self.business_keywords = {
            'restaurant': ['food', 'dining', 'menu', 'cuisine', 'chef', 'restaurant', 'eat', 'meal'],
            'retail': ['shop', 'store', 'buy', 'sale', 'product', 'fashion', 'clothing', 'accessories'],
            'technology': ['tech', 'software', 'digital', 'innovation', 'solution', 'development', 'app'],
            'healthcare': ['health', 'medical', 'care', 'treatment', 'wellness', 'doctor', 'clinic'],
            'education': ['learn', 'education', 'course', 'training', 'school', 'student', 'knowledge'],
            'fitness': ['fitness', 'gym', 'workout', 'health', 'exercise', 'training', 'wellness'],
            'beauty': ['beauty', 'salon', 'spa', 'cosmetics', 'skincare', 'makeup', 'hair'],
            'automotive': ['car', 'auto', 'vehicle', 'repair', 'service', 'parts', 'maintenance'],
            'real_estate': ['property', 'home', 'house', 'real estate', 'buy', 'sell', 'rent'],
            'finance': ['finance', 'money', 'investment', 'banking', 'loan', 'insurance', 'financial']
        }
        
        self.content_templates = {
            'business_tips': [
                "💡 Pro Tip: {tip_content}. What's your experience with this? Share below! #BusinessTips #Growth",
                "🚀 Success Strategy: {tip_content}. Try this and let us know how it works! #BusinessGrowth #Tips",
                "📈 Growth Hack: {tip_content}. Have you tried this approach? #SmallBusiness #Success",
                "💼 Business Insight: {tip_content}. What strategies work best for you? #Entrepreneurship #Business"
            ],
            'promotional_offers': [
                "🎉 Special Offer Alert! {offer_content}. Don't miss out - limited time only! #Sale #SpecialOffer",
                "💥 Exclusive Deal: {offer_content}. Tag a friend who needs this! #Promotion #Deal",
                "🔥 Hot Offer: {offer_content}. Grab yours before it's gone! #LimitedTime #Offer",
                "⭐ Customer Appreciation: {offer_content}. Because you deserve the best! #ThankYou #Discount"
            ],
            'industry_insights': [
                "📊 Industry Update: {insight_content}. What are your thoughts on this trend? #Industry #News",
                "🔍 Market Insight: {insight_content}. How is this affecting your business? #MarketTrends #Business",
                "📰 Industry News: {insight_content}. Stay ahead of the curve! #IndustryNews #Trends",
                "💭 Thought Leadership: {insight_content}. Let's discuss in the comments! #Leadership #Industry"
            ]
        }
        
        self.tone_modifiers = {
            'friendly': {
                'emojis': ['😊', '👋', '💖', '🌟', '✨', '🎉', '💫'],
                'phrases': ['Hey there!', 'Hope you\'re having a great day!', 'We love our community!', 'Thanks for being awesome!'],
                'endings': ['Have a wonderful day! 😊', 'Sending good vibes! ✨', 'You\'re amazing! 💖']
            },
            'professional': {
                'emojis': ['📈', '💼', '🎯', '📊', '🔍', '⚡', '🚀'],
                'phrases': ['Industry leaders know', 'Research shows', 'Best practices indicate', 'Expert analysis reveals'],
                'endings': ['Contact us for more information.', 'Learn more about our solutions.', 'Schedule a consultation today.']
            },
            'witty': {
                'emojis': ['😄', '🤔', '😎', '🎭', '🎪', '🎨', '🎲'],
                'phrases': ['Plot twist:', 'Fun fact:', 'Here\'s the tea:', 'Real talk:'],
                'endings': ['Mind = blown! 🤯', 'You\'re welcome! 😎', 'Drop the mic! 🎤']
            }
        }

    def scrape_website_content(self, url):
        """Scrape and analyze website content"""
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract key information
            title = soup.find('title')
            title_text = title.get_text() if title else ''
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content') if meta_desc else ''
            
            return {
                'title': title_text,
                'description': description,
                'content': text[:2000],  # Limit content length
                'url': url
            }
            
        except Exception as e:
            # Return mock data if scraping fails
            return {
                'title': 'Business Website',
                'description': 'A professional business providing quality services',
                'content': 'Welcome to our business. We provide excellent services and products to our customers.',
                'url': url,
                'error': f'Could not scrape website: {str(e)}'
            }

    def analyze_business(self, website_data, industry_hint=None):
        """Analyze business based on website content and industry hint"""
        content = (website_data.get('title', '') + ' ' + 
                  website_data.get('description', '') + ' ' + 
                  website_data.get('content', '')).lower()
        
        # Determine industry
        detected_industry = self.detect_industry(content, industry_hint)
        
        # Extract business characteristics
        business_analysis = {
            'industry': detected_industry,
            'business_type': self.determine_business_type(content),
            'target_audience': self.identify_target_audience(content, detected_industry),
            'key_services': self.extract_key_services(content, detected_industry),
            'competitive_advantages': self.identify_advantages(content),
            'website_url': website_data.get('url'),
            'analysis_confidence': self.calculate_confidence(content, detected_industry)
        }
        
        return business_analysis

    def detect_industry(self, content, industry_hint=None):
        """Detect industry based on content keywords"""
        if industry_hint and industry_hint.lower() in self.business_keywords:
            return industry_hint.lower()
        
        industry_scores = {}
        for industry, keywords in self.business_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content)
            industry_scores[industry] = score
        
        if industry_scores:
            detected = max(industry_scores, key=industry_scores.get)
            return detected if industry_scores[detected] > 0 else 'general'
        
        return 'general'

    def determine_business_type(self, content):
        """Determine if B2B, B2C, or mixed"""
        b2b_indicators = ['enterprise', 'business', 'corporate', 'professional', 'solution', 'consulting']
        b2c_indicators = ['customer', 'family', 'personal', 'individual', 'home', 'lifestyle']
        
        b2b_score = sum(1 for indicator in b2b_indicators if indicator in content)
        b2c_score = sum(1 for indicator in b2c_indicators if indicator in content)
        
        if b2b_score > b2c_score:
            return 'B2B'
        elif b2c_score > b2b_score:
            return 'B2C'
        else:
            return 'Mixed'

    def identify_target_audience(self, content, industry):
        """Identify target audience based on industry and content"""
        audience_map = {
            'restaurant': 'Food lovers, families, professionals',
            'retail': 'Fashion-conscious consumers, bargain hunters',
            'technology': 'Tech enthusiasts, businesses, developers',
            'healthcare': 'Patients, health-conscious individuals',
            'education': 'Students, professionals, lifelong learners',
            'fitness': 'Fitness enthusiasts, health-conscious individuals',
            'beauty': 'Beauty enthusiasts, self-care focused individuals',
            'automotive': 'Car owners, automotive enthusiasts',
            'real_estate': 'Home buyers, sellers, investors',
            'finance': 'Individuals, businesses, investors'
        }
        
        return audience_map.get(industry, 'General consumers and businesses')

    def extract_key_services(self, content, industry):
        """Extract key services based on content analysis"""
        service_keywords = {
            'restaurant': ['dining', 'takeout', 'catering', 'delivery', 'reservation'],
            'retail': ['shopping', 'fashion', 'accessories', 'sale', 'collection'],
            'technology': ['development', 'consulting', 'support', 'integration', 'solution'],
            'healthcare': ['treatment', 'consultation', 'diagnosis', 'therapy', 'care'],
            'education': ['courses', 'training', 'certification', 'tutoring', 'workshops'],
            'fitness': ['training', 'classes', 'membership', 'coaching', 'programs'],
            'beauty': ['styling', 'treatment', 'consultation', 'makeover', 'services'],
            'automotive': ['repair', 'maintenance', 'inspection', 'parts', 'service'],
            'real_estate': ['buying', 'selling', 'renting', 'property management', 'consultation'],
            'finance': ['planning', 'investment', 'loans', 'insurance', 'advisory']
        }
        
        keywords = service_keywords.get(industry, ['service', 'consultation', 'support'])
        found_services = [keyword for keyword in keywords if keyword in content]
        
        return found_services[:5] if found_services else ['Professional services']

    def identify_advantages(self, content):
        """Identify competitive advantages from content"""
        advantage_keywords = ['best', 'top', 'leading', 'expert', 'professional', 'quality', 
                             'experienced', 'trusted', 'reliable', 'innovative', 'award-winning']
        
        found_advantages = []
        for keyword in advantage_keywords:
            if keyword in content:
                found_advantages.append(keyword.title())
        
        return found_advantages[:3] if found_advantages else ['Quality service']

    def calculate_confidence(self, content, industry):
        """Calculate confidence score for the analysis"""
        if industry == 'general':
            return 0.3
        
        keywords = self.business_keywords.get(industry, [])
        matches = sum(1 for keyword in keywords if keyword in content)
        confidence = min(matches / len(keywords), 1.0)
        
        return round(confidence, 2)

    def generate_content_ideas(self, business_analysis, tone='friendly'):
        """Generate 3 types of content ideas"""
        industry = business_analysis['industry']
        business_type = business_analysis['business_type']
        
        content_ideas = {
            'business_tips': self.generate_business_tips(industry, business_type, tone),
            'promotional_offers': self.generate_promotional_offers(industry, business_analysis, tone),
            'industry_insights': self.generate_industry_insights(industry, tone)
        }
        
        return content_ideas

    def generate_business_tips(self, industry, business_type, tone):
        """Generate business tips content"""
        tips_by_industry = {
            'restaurant': [
                'Use high-quality photos of your dishes on social media to attract customers',
                'Offer seasonal menu items to keep customers coming back',
                'Engage with customer reviews promptly and professionally',
                'Create a loyalty program to reward repeat customers',
                'Partner with local food bloggers for authentic reviews'
            ],
            'retail': [
                'Create window displays that tell a story about your brand',
                'Use customer data to personalize shopping experiences',
                'Implement a seamless omnichannel strategy',
                'Offer exclusive in-store events for VIP customers',
                'Leverage user-generated content in your marketing'
            ],
            'technology': [
                'Focus on solving real problems rather than just showcasing features',
                'Invest in customer education and onboarding',
                'Build a strong developer community around your product',
                'Prioritize security and data privacy in all communications',
                'Use case studies to demonstrate ROI to potential clients'
            ],
            'general': [
                'Know your target audience inside and out',
                'Consistency in branding builds trust and recognition',
                'Customer feedback is your most valuable asset',
                'Invest in employee training for better customer service',
                'Use data analytics to make informed business decisions'
            ]
        }
        
        tips = tips_by_industry.get(industry, tips_by_industry['general'])
        selected_tips = random.sample(tips, min(3, len(tips)))
        
        formatted_tips = []
        for tip in selected_tips:
            template = random.choice(self.content_templates['business_tips'])
            formatted_tip = template.format(tip_content=tip)
            formatted_tip = self.apply_tone(formatted_tip, tone)
            formatted_tips.append(formatted_tip)
        
        return formatted_tips

    def generate_promotional_offers(self, industry, business_analysis, tone):
        """Generate promotional offers content"""
        services = business_analysis.get('key_services', ['services'])
        
        offer_templates = {
            'restaurant': [
                'Get 20% off your next meal when you bring a friend!',
                'Happy Hour special: Buy one appetizer, get one free!',
                'Family dinner deal: Kids eat free on Sundays!',
                'New customer special: 15% off your first order',
                'Loyalty program: Collect 10 stamps, get a free meal!'
            ],
            'retail': [
                'Flash sale: 30% off all items this weekend only!',
                'Buy 2, get 1 free on selected items',
                'New arrivals: First 50 customers get 25% off',
                'Student discount: Show your ID for 15% off',
                'Refer a friend and both get 20% off your next purchase'
            ],
            'technology': [
                'Free consultation for new clients this month',
                'Upgrade your plan and get 2 months free',
                'Early bird special: 40% off our premium package',
                'Bundle deal: Save 25% when you combine our services',
                'Free trial extended to 30 days for limited time'
            ],
            'general': [
                'New customer discount: 20% off your first purchase',
                'Refer a friend and get $50 credit',
                'Limited time: Buy one service, get 50% off the second',
                'Early bird special: Book now and save 25%',
                'Loyalty reward: 10% off for returning customers'
            ]
        }
        
        offers = offer_templates.get(industry, offer_templates['general'])
        selected_offers = random.sample(offers, min(3, len(offers)))
        
        formatted_offers = []
        for offer in selected_offers:
            template = random.choice(self.content_templates['promotional_offers'])
            formatted_offer = template.format(offer_content=offer)
            formatted_offer = self.apply_tone(formatted_offer, tone)
            formatted_offers.append(formatted_offer)
        
        return formatted_offers

    def generate_industry_insights(self, industry, tone):
        """Generate industry insights content"""
        insights_by_industry = {
            'restaurant': [
                'Food delivery apps now account for 60% of restaurant orders',
                'Sustainable dining practices are becoming a key differentiator',
                'Ghost kitchens are revolutionizing the restaurant industry',
                'Contactless dining experiences are here to stay',
                'Plant-based menu options are driving 23% more traffic'
            ],
            'retail': [
                'E-commerce sales are expected to reach $8.1 trillion by 2026',
                'Personalization can increase sales by up to 19%',
                'Social commerce is growing 3x faster than traditional e-commerce',
                'Sustainable products are driving 73% of millennial purchases',
                'AR try-on features increase conversion rates by 64%'
            ],
            'technology': [
                'AI adoption in business has increased by 270% in the last 4 years',
                'Cloud computing market is projected to reach $1.6 trillion by 2030',
                'Cybersecurity spending will exceed $1.75 trillion by 2025',
                'Remote work tools have become permanent fixtures in 87% of companies',
                'Low-code/no-code platforms are democratizing software development'
            ],
            'general': [
                'Digital transformation initiatives have accelerated by 6 years due to COVID-19',
                'Customer experience is now the top competitive differentiator',
                'Sustainability practices influence 83% of consumer purchasing decisions',
                'Social media marketing ROI has increased by 95% in the past year',
                'Data-driven companies are 23x more likely to acquire customers'
            ]
        }
        
        insights = insights_by_industry.get(industry, insights_by_industry['general'])
        selected_insights = random.sample(insights, min(3, len(insights)))
        
        formatted_insights = []
        for insight in selected_insights:
            template = random.choice(self.content_templates['industry_insights'])
            formatted_insight = template.format(insight_content=insight)
            formatted_insight = self.apply_tone(formatted_insight, tone)
            formatted_insights.append(formatted_insight)
        
        return formatted_insights

    def apply_tone(self, content, tone):
        """Apply tone modifications to content"""
        if tone not in self.tone_modifiers:
            return content
        
        modifiers = self.tone_modifiers[tone]
        
        # Add appropriate emoji
        emoji = random.choice(modifiers['emojis'])
        if emoji not in content:
            content = f"{emoji} {content}"
        
        return content

    def create_content_calendar(self, content_ideas, frequency, tone='friendly', post_mix=None):
        """Create a weekly content calendar"""
        if post_mix is None:
            post_mix = {'educational': 40, 'promotional': 30, 'newsy': 30}
        
        # Calculate posts per week based on frequency
        frequency_map = {
            '1x/week': 1,
            '2x/week': 2,
            '3x/week': 3,
            '4x/week': 4,
            '5x/week': 5,
            'daily': 7
        }
        
        posts_per_week = frequency_map.get(frequency, 2)
        
        # Create calendar for next 4 weeks
        calendar = []
        start_date = datetime.now()
        
        for week in range(4):
            week_start = start_date + timedelta(weeks=week)
            week_posts = self.generate_week_posts(
                content_ideas, posts_per_week, week_start, tone, post_mix
            )
            calendar.extend(week_posts)
        
        return calendar

    def generate_week_posts(self, content_ideas, posts_per_week, week_start, tone, post_mix):
        """Generate posts for a specific week"""
        week_posts = []
        
        # Determine post types based on mix
        post_types = []
        educational_count = int(posts_per_week * post_mix['educational'] / 100)
        promotional_count = int(posts_per_week * post_mix['promotional'] / 100)
        newsy_count = posts_per_week - educational_count - promotional_count
        
        post_types.extend(['educational'] * educational_count)
        post_types.extend(['promotional'] * promotional_count)
        post_types.extend(['newsy'] * newsy_count)
        
        # Shuffle to randomize order
        random.shuffle(post_types)
        
        # Generate posts for each day
        posting_days = self.get_optimal_posting_days(posts_per_week)
        
        for i, day_offset in enumerate(posting_days[:posts_per_week]):
            post_date = week_start + timedelta(days=day_offset)
            post_type = post_types[i] if i < len(post_types) else 'educational'
            
            # Select content based on type
            if post_type == 'educational':
                content = random.choice(content_ideas['business_tips'])
                category = 'Business Tips'
            elif post_type == 'promotional':
                content = random.choice(content_ideas['promotional_offers'])
                category = 'Promotional'
            else:  # newsy
                content = random.choice(content_ideas['industry_insights'])
                category = 'Industry Insights'
            
            week_posts.append({
                'id': f"post_{post_date.strftime('%Y%m%d')}_{i}",
                'date': post_date.strftime('%Y-%m-%d'),
                'day': post_date.strftime('%A'),
                'time': self.get_optimal_posting_time(post_type),
                'category': category,
                'type': post_type,
                'content': content,
                'tone': tone,
                'status': 'scheduled',
                'engagement_prediction': self.predict_engagement(post_type, post_date.strftime('%A'))
            })
        
        return week_posts

    def get_optimal_posting_days(self, posts_per_week):
        """Get optimal days for posting based on frequency"""
        optimal_days = {
            1: [1],  # Tuesday
            2: [1, 4],  # Tuesday, Friday
            3: [0, 2, 4],  # Monday, Wednesday, Friday
            4: [0, 1, 3, 4],  # Monday, Tuesday, Thursday, Friday
            5: [0, 1, 2, 3, 4],  # Monday to Friday
            7: [0, 1, 2, 3, 4, 5, 6]  # Every day
        }
        
        return optimal_days.get(posts_per_week, [0, 2, 4])

    def get_optimal_posting_time(self, post_type):
        """Get optimal posting time based on post type"""
        time_map = {
            'educational': '09:00',
            'promotional': '12:00',
            'newsy': '15:00'
        }
        
        return time_map.get(post_type, '10:00')

    def predict_engagement(self, post_type, day):
        """Predict engagement based on post type and day"""
        base_engagement = {
            'educational': {'likes': 25, 'comments': 5, 'shares': 3},
            'promotional': {'likes': 35, 'comments': 8, 'shares': 2},
            'newsy': {'likes': 20, 'comments': 12, 'shares': 6}
        }
        
        day_multiplier = {
            'Monday': 0.8, 'Tuesday': 1.0, 'Wednesday': 1.1,
            'Thursday': 1.2, 'Friday': 1.3, 'Saturday': 0.9, 'Sunday': 0.7
        }
        
        base = base_engagement.get(post_type, base_engagement['educational'])
        multiplier = day_multiplier.get(day, 1.0)
        
        return {
            'likes': int(base['likes'] * multiplier),
            'comments': int(base['comments'] * multiplier),
            'shares': int(base['shares'] * multiplier)
        }

    def simulate_facebook_posting(self, post_data):
        """Simulate posting to Facebook (mock implementation)"""
        # Simulate API call delay
        import time
        time.sleep(0.5)
        
        # Mock successful posting
        post_result = {
            'success': True,
            'post_id': f"fb_post_{random.randint(100000, 999999)}",
            'posted_at': datetime.now().isoformat(),
            'platform': 'Facebook',
            'content': post_data.get('content', ''),
            'scheduled_time': post_data.get('scheduled_time'),
            'status': 'published',
            'reach': random.randint(100, 1000),
            'engagement': {
                'likes': random.randint(5, 50),
                'comments': random.randint(0, 15),
                'shares': random.randint(0, 10)
            },
            'url': f"https://facebook.com/posts/{random.randint(100000, 999999)}"
        }
        
        return post_result
