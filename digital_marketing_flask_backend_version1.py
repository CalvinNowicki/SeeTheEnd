from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    influencer_name = request.form['influencer_name']
    influencer_email = request.form['influencer_email']

    influencer = onboard_influencer(influencer_name, influencer_email)
    services = suggest_services()
    
    email_content = generate_email_content(influencer['influencer_name'])
    
    return jsonify({
        'influencer': influencer,
        'services': format_services(services),
        'email_content': format_email_content(email_content),
    })

def onboard_influencer(influencer_name, influencer_email):
    return {
        'influencer_name': influencer_name,
        'influencer_email': influencer_email,
    }

def suggest_services():
    return {
        "Email Marketing for Influencers": [
            "Personalized Newsletter Campaigns",
            "Engagement-driven Drip Email Campaigns",
            "Collaborative Brand Promotions",
            "Exclusive Offer Announcements",
            "Audience Feedback Surveys"
        ]
    }

def generate_email_content(influencer_name):
    email_template = f"""
Hello {influencer_name},

As an influential figure in the social media realm, it's essential to keep your audience engaged and informed. Our specialized email marketing solutions for influencers can help elevate your brand and deepen the connection with your followers.

Explore our services and discover how we can assist you in reaching new heights.

Best regards,
Your Marketing Team
    """
    return email_template

def format_services(services):
    return "\n".join([f"{k}: {', '.join(v)}" for k, v in services.items()])

def format_email_content(email_content):
    return email_content

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
