from flask import Flask, request, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Declaring the check number functions
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % 1 == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return n == sum(d**len(digits) for d in digits)

def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

def get_number_fact(number):
    url = f"http://numbersapi.com/{number}/math?json=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("text", "No fact available")
    
    return "No fact available"

# MY API Endpoint
@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    number = request.args.get("number")
    
    # Input validation
    if not number or not number.isdigit():
        response_data = {
            "number": "alphabet",
            "error": True
        }
        response_json = json.dumps(response_data, indent=4)
        return Response(response_json, status=400, content_type="application/json")
        
    number = int(number)
    
    # properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")
    
    # Response
    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(number)),
        "fun_fact": get_number_fact(number)
    }
    
    response_json = json.dumps(response_data, indent=4)
    
    return Response(response_json, status=200, content_type="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)