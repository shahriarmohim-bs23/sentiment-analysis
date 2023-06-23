from flask import Flask, request, jsonify
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import torch

model_name = "StatsGary/setfit-ft-sentinent-eval"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    try:
        
        text = request.json.get("text")

        
        if text is None:
            error_message = "Missing 'text' parameter in the request"
            return jsonify({"error": error_message}), 400

        
        inputs = tokenizer(text, return_tensors="pt")

        
        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits).item()
        sentiment = ["negative", "neutral", "positive"][predicted_class]

        
        response = {"sentiment": sentiment}

        return jsonify(response)

    except Exception as e:
        
        error_message = "An error occurred while analyzing the sentiment"
        return jsonify({"error": error_message}), 500
if __name__ == "__main__":
    app.run()
