from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = Flask(__name__)
api = Api(app)

# Explicit Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)

# Define the path to the model directory
MODEL_DIR = "model/"

# Load tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
except Exception as e:
    raise RuntimeError(f"Failed to load tokenizer or model: {e}")

# Define labels for toxicity categories
labels = ["abuse", "severe_abuse", "obscene", "threat", "insult", "identity_attack"]

def get_toxicity_scores(texts):
    """
    Predicts toxicity scores for a list of text inputs.
    
    :param texts: List of text strings or single string
    :return: List of dictionaries containing toxicity scores
    """
    if isinstance(texts, str):
        texts = [texts]

    try:
        inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.sigmoid(logits).tolist()
        results = [dict(zip(labels, [round(prob, 2) for prob in probs])) for probs in probabilities]
        return results
    except Exception as e:
        raise

class ToxicityAnalysis(Resource):
    def get(self):
        """
        Predict the toxicity of the given text.
        ---
        tags:
          - Toxicity Prediction
        parameters:
          - name: text
            in: query
            type: string
            required: true
            description: The text to analyze for toxicity
        responses:
          200:
            description: Prediction results for the provided text
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    original_text:
                      type: string
                      description: The original input text
                    toxicity_results:
                      type: object
                      properties:
                        Prob (Abuse):
                          type: number
                          description: Probability of the text being abusive
                        Prob (Severe Abuse):
                          type: number
                          description: Probability of severe abuse
                        Prob (Obscene):
                          type: number
                          description: Probability of the text being obscene
                        Prob (Threat):
                          type: number
                          description: Probability of the text being a threat
                        Prob (Insult):
                          type: number
                          description: Probability of the text being an insult
                        Prob (Identity Attack):
                          type: number
                          description: Probability of identity-based attack
          400:
            description: Input text is missing or invalid
          500:
            description: Server error during prediction
        """
        text = request.args.get('text', '').strip()

        if not text:
            return jsonify({"error": "Text is required"}), 400

        # Basic input validation
        if len(text) > 10000:
            return jsonify({"error": "Text is too long (max 10,000 characters)"}), 400

        try:
            # Get toxicity scores
            results = get_toxicity_scores(text)
            toxicity_results = {
                f"Prob ({label.replace('_', ' ').title()})": score
                for label, score in results[0].items()
            }

            # Prepare response
            response = {
                'original_text': text,
                'toxicity_results': toxicity_results
            }
            return jsonify(response)

        except Exception as e:
            return jsonify({"error": f"Error during prediction: {e}"}), 500

# Adding the resource to the API
api.add_resource(ToxicityAnalysis, "/toxicityanalysis")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)