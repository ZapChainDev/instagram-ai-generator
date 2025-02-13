import os
import csv
import requests
from flask import Flask, request, jsonify, render_template, send_file
import subprocess

app = Flask(__name__)

# ✅ Use your real Pexels API key
PEXELS_API_KEY = "lz7a3aOc6TjmvuOCWTd5uGX6T6TYHrcSD5LQwlmTM3JsqMFJ6kdjfk0l"
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

# List of available Ollama models
AVAILABLE_MODELS = ["mistral", "gemma", "llama3"]

# Function to generate captions using Ollama
def generate_instagram_caption(topic, model):
    prompt = f"Generate a catchy Instagram caption for a post about {topic}. Make it engaging, under 150 characters, and include emojis."
    
    if model not in AVAILABLE_MODELS:
        return "Error: Invalid model selected"

    try:
        result = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip()
        else:
            print("Ollama error:", result.stderr)
            return "Error: Failed to generate caption"
    except Exception as e:
        print("Ollama subprocess error:", str(e))
        return "Error: Ollama AI not responding"

# Function to generate hashtags using Ollama
def generate_hashtags(topic, model):
    prompt = f"Suggest 5 trending Instagram hashtags related to {topic}. Only provide the hashtags, separated by spaces."

    if model not in AVAILABLE_MODELS:
        return "Error: Invalid model selected"

    try:
        result = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip()
        else:
            print("Ollama error:", result.stderr)
            return "Error: Failed to generate hashtags"
    except Exception as e:
        print("Ollama subprocess error:", str(e))
        return "Error: Ollama AI not responding"

# Function to save data in a CSV file
def save_to_csv(topic, caption, hashtags, model):
    file_path = "captions.csv"
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([topic, caption, hashtags, model])
    print(f"Saved to {file_path}")

@app.route('/')
def index():
    return render_template('index.html', models=AVAILABLE_MODELS)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get("topic")
    model = data.get("model", "mistral")  # Default to 'mistral' if no model is selected

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    caption = generate_instagram_caption(topic, model)
    hashtags = generate_hashtags(topic, model)

    # Save to CSV file
    save_to_csv(topic, caption, hashtags, model)

    return jsonify({"caption": caption, "hashtags": hashtags})

@app.route('/captions')
def show_captions():
    captions_list = []
    try:
        with open("captions.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 4:
                    captions_list.append({"topic": row[0], "caption": row[1], "hashtags": row[2], "model": row[3]})
    except FileNotFoundError:
        captions_list = []

    return render_template('captions.html', captions=captions_list)

@app.route('/download_csv')
def download_csv():
    file_path = "captions.csv"

    if not os.path.exists(file_path):
        return "No captions available to download.", 404

    return send_file(file_path, as_attachment=True, download_name="captions.csv", mimetype="text/csv")

# ✅ Function to fetch AI-generated images from Pexels API
def generate_ai_images(topic):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": topic, "per_page": 3}  # Fetch 3 images

    try:
        response = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params)
        data = response.json()

        if "photos" in data and len(data["photos"]) > 0:
            image_urls = [img["src"]["medium"] for img in data["photos"]]
            return image_urls
        else:
            print("No images found for topic:", topic)
            return []

    except Exception as e:
        print(f"Pexels API Error: {str(e)}")
        return []

@app.route('/generate_images', methods=['POST'])
def generate_images():
    data = request.json
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    image_urls = generate_ai_images(topic)
    return jsonify({"images": image_urls})

if __name__ == "__main__":
    app.run(debug=True)
