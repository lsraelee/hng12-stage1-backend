# Number Classification API

## Description

The **Number Classification API** is a Flask-based application that takes a number as input and returns its interesting mathematical properties along with a fun fact retrieved from the Numbers API. This API supports JSON responses, handles CORS, and is publicly accessible.

---

## Features

- Classifies numbers into **prime**, **perfect**, and **Armstrong** categories.
- Identifies **odd** or **even** properties of the number.
- Calculates the **digit sum** of the number.
- Provides a fun fact about the number from the Numbers API.
- Input validation and error handling for invalid inputs.
- Deployed to a publicly accessible endpoint.

---

## API Endpoint

### **GET /api/classify-number**

#### Query Parameters:
- `number` (required): The integer to classify.

#### Example Request:
```bash
GET /api/classify-number?number=371
