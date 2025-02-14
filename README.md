📸 AI Caption & Image Generator 🚀
Generate engaging captions and hashtags for Instagram posts using AI!
🎨 Fetch AI-generated images based on your topic and seamlessly integrate with Zapier and Buffer.

🔥 Features
✅ AI-powered Instagram caption generator
✅ AI-generated hashtags for better engagement
✅ Fetch relevant images using Pexels API
✅ Choose from multiple AI models (Mistral, Gemma, Llama3)
✅ Download captions as CSV
✅ Integrate with Buffer via Zapier Webhooks

🛠 Tech Stack
Backend: Flask (Python)
Frontend: Tailwind CSS, HTML, JavaScript
AI Models: Ollama AI
Image Source: Pexels API
Automation: Zapier Webhooks

🚀 How to Run the Project

1️⃣ Clone this repository:
bash
Copy
git clone https://github.com/your_username/instagram-ai-generator.git
cd instagram-ai-generator

2️⃣ Set up a virtual environment:
For Windows:

bash
Copy
python -m venv venv
venv\Scripts\activate
For Mac/Linux:

bash
Copy
python -m venv venv
source venv/bin/activate

3️⃣ Install dependencies:
bash
Copy
pip install -r requirements.txt

4️⃣ Set environment variables:
Create a .env file in the root directory with the following keys:

plaintext
Copy
PEXELS_API_KEY=your_pexels_api_key_here

ZAPIER_WEBHOOK_URL=your_zapier_webhook_url_here

5️⃣ Run the Flask app:
bash
Copy
python app.py
Your app should now be running on:

plaintext
Copy
http://127.0.0.1:5000
🌟 Troubleshooting
No images found:

Make sure your Pexels API key is valid and correctly set in the .env file.
Check that your Pexels account has access to the API.
Zapier webhook issues:

Confirm that the correct Zapier webhook URL is set in the .env file.
Ensure that the Zap is properly configured and active.
Environment variables not loading:

Double-check that you have a .env file in the root of the project.
Verify the syntax: no quotes around values, and each key-value pair on its own line.
