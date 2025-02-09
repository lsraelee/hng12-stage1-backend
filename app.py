from flask import Flask, request, Response
from flask_cors import CORS
import requests
import json
import re

app = Flask(__name__)
CORS(app)

# Utility functions
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    if n < 0:
        return False
    digits = [int(d) for d in str(abs(n))]
    return n == sum(d**len(digits) for d in digits)

def is_perfect(n):
    if n <= 0:
        return False
    return n == sum(i for i in range(1, n) if n % i == 0)

def get_number_fact(number):
    url = f"http://numbersapi.com/{number}/math?json=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("text", "No fact available")
    return "No fact available"

def sanitize_input(value):
    # Treat "null" as "0" (case insensitive)
    value = value.lower().replace("null", "0")
    
    # Match valid integer patterns, including negative numbers
    match = re.fullmatch(r"-?\d+", value)
    if match:
        return int(match.group())
    
    # Invalid input
    return None

# API Endpoint
@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    number = request.args.get("number")
    
    # Input validation and sanitization
    if number is None:
        response_data = {
            "number": "alphabet",
            "error": True
        }
        response_json = json.dumps(response_data, indent=4)
        return Response(response_json, status=400, content_type="application/json")

    sanitized_number = sanitize_input(number)
    if sanitized_number is None:
        response_data = {
            "number": "alphabet",
            "error": True
        }
        response_json = json.dumps(response_data, indent=4)
        return Response(response_json, status=400, content_type="application/json")

    # Properties
    properties = []
    if is_armstrong(sanitized_number):
        properties.append("armstrong")
    properties.append("odd" if sanitized_number % 2 != 0 else "even")
    
    # Calculate digit sum (negative numbers included as `-2 + 3 + 4`)
    digits = [int(d) if i == 0 and str(sanitized_number)[0] == '-' else int(d) 
              for i, d in enumerate(str(abs(sanitized_number)))]
    digit_sum = sum(digits)

    # Response
    response_data = {
        "number": sanitized_number,
        "is_prime": is_prime(sanitized_number),
        "is_perfect": is_perfect(sanitized_number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": get_number_fact(sanitized_number)
    }
    
    response_json = json.dumps(response_data, indent=4)
    return Response(response_json, status=200, content_type="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)