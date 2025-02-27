from flask import Flask, jsonify, Blueprint
import requests
from transformers import pipeline

get_study = Blueprint("fetch_result", __name__)

# Load a small but powerful AI model (Flan-T5 Small)
title_generator = pipeline("text2text-generation", model="google/flan-t5-small")

@get_study.route('/api_get', methods=['GET'])
def fetch_result():
    try:
        thesis_title = generate_thesis_title()  # Generate a thesis title

        # Fetch RRLs based on the generated title
        study_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={thesis_title}&limit=5"
        response = requests.get(study_url)

        related_rrls = []
        if response.status_code == 200:
            papers = response.json()
            if "data" in papers:
                related_rrls = [paper.get("title", "No title found") for paper in papers["data"]]

        return jsonify({"generated_thesis_title": thesis_title, "related_rrls": related_rrls})
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

def generate_thesis_title():
    prompt = f"Create a unique and research-worthy thesis title related to. Avoid repetition."
    result = title_generator(prompt, max_new_tokens=20, temperature=0.7, top_k=50)  
    
    return result[0]['generated_text'].strip()