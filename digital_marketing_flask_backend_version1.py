
from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    client_name = request.form['client_name']
    client_email = request.form['client_email']
    marketing_needs = request.form.getlist('marketing_needs')
    
    # Capture the new product details
    product_name = request.form['product_name']
    product_cost = request.form['product_cost']
    product_use = request.form['product_use']

    client = onboard_client(client_name, client_email, marketing_needs)
    services = suggest_services(client)
    
    # Update the function call to include product details
    email_content = generate_email_content(client['client_name'], product_name, product_cost, product_use)
    report = generate_email_report()
    
    return jsonify({
        'client': client,
        'services': format_services(services),
        'email_content': format_email_content(email_content),
        'report': report
    })

def onboard_client(client_name, client_email, marketing_needs):
    return {
        'client_name': client_name,
        'client_email': client_email,
        'marketing_needs': [int(need) for need in marketing_needs]
    }

def suggest_services(client_data):
    marketing_options = {
        1: "Email Marketing",
        2: "Ad Creation",
        3: "Product Design",
        4: "Social Media Marketing"
    }
    
    service_recommendations = {
        1: ["Newsletter Campaigns", "Drip Email Campaigns"],
        2: ["Google Ads", "Facebook Ads"],
        3: ["3D Product Visualization", "Product Photography"],
        4: [
            "Facebook Page Management",
            "Instagram: Consistent Posting, Use of Hashtags, Engage with Followers, Collaborate with Influencers, Instagram Ads",
            "TikTok: Create Trending Content, Engage with Audience, Collaborate with TikTok Creators, TikTok Challenges, TikTok Ads"
        ]
    }
    
    recommendations = {}
    for need in client_data['marketing_needs']:
        recommendations[marketing_options[need]] = service_recommendations[need]
    return recommendations
    
def generate_email_content(client_name, product_name, product_cost, product_use):
    email_template = f"""
Hello Loyal Customer!

We are excited to introduce our latest product: {product_name}!

Features:
- Purpose: {product_use}
- Price: ${product_cost}

We believe that {product_name} will perfectly cater to your needs and offer unparalleled value. Whether you're looking to {product_use.lower()} or just explore something new, this product is designed with you in mind.

Order yours today and experience the difference!

Warm regards,
{client_name}
    """
    return email_template

def generate_email_report():
    return "This is a sample report content."

def format_services(services):
    return "\n".join([f"{k}: {', '.join(v)}" for k, v in services.items()])

def format_email_content(email_content):
    return email_content


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT if it's there, otherwise default to 5000 for local development
    app.run(host='0.0.0.0', port=port)
