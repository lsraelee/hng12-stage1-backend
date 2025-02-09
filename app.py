from flask import Flask, request, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Functions to classify numbers
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(abs(n)**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]
    return abs(n) == sum(d**len(digits) for d in digits)

def is_perfect(n):
    return abs(n) == sum(i for i in range(1, abs(n)) if abs(n) % i == 0)

def get_number_fact(number):
    url = f"http://numbersapi.com/{number}/math?json=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("text", "No fact available")
    return "No fact available"

def calculate_digit_sum(n):
    # If number is negative, include the negative sign only for the first digit
    digits = [-int(str(abs(n))[0])] + [int(d) for d in str(abs(n))[1:]] if n < 0 else [int(d) for d in str(n)]
    return sum(digits)

# API endpoint
@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    number = request.args.get("number")

    # Validate the input: Ensure it's a valid number
    if not number or not (number.lstrip('-').isdigit() and '-' not in number.lstrip('-')):
        response_data = {
            "number": "alphabet",
            "error": True
        }
        response_json = json.dumps(response_data, indent=4)
        return Response(response_json, status=400, content_type="application/json")

    # Convert to integer for processing
    number = int(number)

    # Determine properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    # Response data
    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": calculate_digit_sum(number),
        "fun_fact": get_number_fact(number)
    }

    response_json = json.dumps(response_data, indent=4)
    return Response(response_json, status=200, content_type="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
