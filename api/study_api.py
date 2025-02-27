from flask import Flask, jsonify, Blueprint
import requests
import random
from transformers import pipeline
from tensorflow.keras.backend import clear_session
from requests.exceptions import RequestException

# Flask Blueprint
get_study = Blueprint("fetch_result", __name__)

# Load the title generator model
title_generator = pipeline("text2text-generation", model="google/flan-t5-large")

@get_study.route('/api_get', methods=['GET'])
def fetch_result():
    try:
        thesis_title = generate_thesis_title()
        related_rrls = fetch_related_rrls(thesis_title)

        return jsonify({
            "generated_thesis_title": thesis_title,
            "related_rrls": related_rrls
        })
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

def generate_thesis_title():
    """Generate an academic thesis title using a pre-trained AI model."""
    try:
        prompt = (
            "Generate an academic thesis title for a research study in the field of Information Technology or Computer Science. "
            "The title should be formal, concise, and research-oriented."
        )

        clear_session()  # Free up memory before generating the title
        
        result = title_generator(
            prompt, 
            max_new_tokens=30, 
            temperature=1.2, 
            top_k=50, 
            top_p=0.9, 
            do_sample=True
        )  

        return result[0].get('generated_text', 'No title generated').strip()

    except Exception as e:
        print(f"Error generating thesis title: {e}")
        return "Title generation failed"

def fetch_related_rrls(thesis_title, per_page=5):
    url = f"https://api.openalex.org/works?search={thesis_title}&per_page={per_page}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for HTTP issues

        data = response.json()
        results = data.get("results", [])  # Get results or an empty list if not found
        
        related_rrls = []
        for items in results:
            title = items.get("title", "No title found")
            doi = items.get("doi", "No DOI found")
            openalex_id = items.get("id", "No ID found")

            # Construct source link (prefer DOI, fallback to OpenAlex ID)
            source_link = f"https://doi.org/{doi}" if doi else openalex_id

            related_rrls.append({
                "title": title,  # Title comes first
                "source_link": source_link  # Source link comes second
            })

        return related_rrls

    except RequestException as e:
        print(f"Error fetching RRLs: {e}")  # Log errors for debugging
        return []
