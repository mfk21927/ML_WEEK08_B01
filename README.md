# ML_WEEK08_B01
# 🚀 ML-Internship

> **Name:** Muhammad Fahad 
> **Email:** [![Email](https://img.shields.io/badge/Email-mfk21927@gmail.com-red?style=flat-square&logo=gmail&logoColor=white)](mailto:mfk21927@gmail.com) 
> **LinkedIn:** [![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad%20Fahad-blue?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhammad-fahad-087057293) 
> **Start Date:** 20-12-2025 

---

![Internship](https://img.shields.io/badge/Status-Active-blue?style=for-the-badge)
![Batch](https://img.shields.io/badge/Batch-B01-orange?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![TFLite](https://img.shields.io/badge/TFLite-ai--edge--litert-orange?logo=tensorflow&logoColor=white)](https://ai.google.dev/edge/litert)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Project Overview
This repository documents my **Week 8 Machine Learning Internship tasks**, focused on **Flask Backend & API Development**.
It includes implementations of **RESTful APIs, ML model deployment, image classification with TFLite, database integration, Swagger documentation, and API key authentication**.

---

## 📈 Week 8 Tasks Overview

| Task | Title | Key Tech | Status |
| :--- | :--- | :--- | :--- |
| 8.1 | Flask Basics & First API | Flask, REST, CRUD | ✅ Completed |
| 8.2 | ML Model Deployment with Flask | Pickle, Scikit-Learn, HTML | ✅ Completed |
| 8.3 | Image Classification API with TFLite | TFLite, Pillow, NumPy | ✅ Completed |
| 8.4 | RESTful API with Database Integration | SQLAlchemy, Swagger, Auth | ✅ Completed |

---

## ✅ Task Details

### **Task 8.1: Flask Basics & First API**
- **File:** `flask_basics.py`
- **Steps Implemented:**
  - Installed Flask and created the application.
  - Initialized app with `Flask(__name__)`.
  - Created **GET `/`** endpoint returning a welcome message.
  - Created **GET `/data`** endpoint returning all items from in-memory storage.
  - Created **POST `/data`** endpoint to add new items.
  - Created **PUT `/data/<id>`** endpoint to update existing items.
  - Created **DELETE `/data/<id>`** endpoint to remove items.
  - Implemented in-memory data storage using a Python dictionary.
  - Tested all endpoints using Postman/curl.

**Endpoints:**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Welcome message |
| GET | `/data` | Get all items |
| POST | `/data` | Add new item |
| PUT | `/data/<id>` | Update item by ID |
| DELETE | `/data/<id>` | Delete item by ID |

**Example Request & Response:**
```bash
# POST /data
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"name": "item1"}'
# Response: {"message": "Item added", "item": {"name": "item1"}}
```

---

### **Task 8.2: ML Model Deployment with Flask**
- **Files:** `flask_ml_api.py`, `templates/index.html`
- **Steps Implemented:**
  - Trained and saved an Iris classifier model (`.pkl` file).
  - Created Flask app and loaded the model with `pickle.load()`.
  - Created **POST `/predict`** endpoint accepting JSON input.
  - Parsed input with `request.get_json()` and validated feature count.
  - Made predictions using `model.predict()` and returned JSON response.
  - Implemented error handling with try-except blocks.
  - Created an HTML form in `templates/index.html` for browser-based testing.
  - Added route to render the HTML form.

**Example Request & Response:**
```bash
# POST /predict
curl -X POST http://127.0.0.1:5001/predict -H "Content-Type: application/json" -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
# Response: {"prediction": "setosa"}
```

---

### **Task 8.3: Image Classification API with TFLite**
- **File:** `flask_image_api.py`
- **Model:** `fashion_mnist_model.tflite`
- **Steps Implemented:**
  - Installed `ai-edge-litert` (TFLite runtime) for model inference.
  - Loaded the TFLite model and created the interpreter.
  - Allocated tensors and retrieved input/output details.
  - Created **POST `/classify`** endpoint accepting image file uploads via `request.files`.
  - Preprocessed images: converted to grayscale, resized to 28×28, normalized to [0, 1].
  - Ran inference with `interpreter.invoke()` and extracted output tensor predictions.
  - Returned **top-5 predictions** with labels and probabilities.
  - Implemented **POST `/classify_batch`** for classifying multiple images at once.
  - Supports multiple image formats: JPG, PNG, WebP.
  - Added a styled home page with image preview, progress bars, and ranked results.

**Endpoints:**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Home page with upload form |
| POST | `/classify` | Classify a single image |
| POST | `/classify_batch` | Classify multiple images |

**Example Request & Response:**
```bash
# POST /classify
curl -X POST -F "image=@sandals.jpg" http://127.0.0.1:5002/classify
# Response:
# {
#   "top_5_predictions": [
#     {"label": "Sandal", "probability": "98.94%"},
#     {"label": "Sneaker", "probability": "0.51%"},
#     ...
#   ]
# }
```

---

### **Task 8.4: RESTful API with Database Integration**
- **Files:** `flask_rest_api.py`, `swagger.json`
- **Steps Implemented:**
  - Installed `flask-sqlalchemy` and `flask-swagger-ui`.
  - Created database models: `Prediction` (stores results) and `ApiKey` (stores API keys).
  - Initialized SQLite database with `db.create_all()`.
  - Implemented **POST `/predictions`** to save prediction records.
  - Implemented **GET `/predictions`** with **pagination** (`?page=1&per_page=10`).
  - Added **filtering** by date range (`?start_date=`, `?end_date=`), model name (`?model=`), and label (`?label=`).
  - Created **API key authentication** decorator checking `X-API-Key` header.
  - Implemented **request/response logging** to console and `api.log` file.
  - Created `swagger.json` OpenAPI 3.0 specification.
  - Added **Swagger UI** endpoint at `/swagger`.
  - Implemented full **CRUD**: Create, Read (single + list), Update, Delete.

**Endpoints:**

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| GET | `/` | No | API info & endpoint list |
| POST | `/api-keys` | No | Generate a new API key |
| POST | `/predictions` | Yes | Save a prediction |
| GET | `/predictions` | Yes | List predictions (paginated & filtered) |
| GET | `/predictions/<id>` | Yes | Get single prediction |
| PUT | `/predictions/<id>` | Yes | Update a prediction |
| DELETE | `/predictions/<id>` | Yes | Delete a prediction |
| GET | `/swagger` | No | Swagger UI documentation |

**Example Request & Response:**
```bash
# Generate API key
curl -X POST http://127.0.0.1:5003/api-keys -H "Content-Type: application/json" -d '{"owner": "developer"}'
# Response: {"api_key": "<generated-key>", "owner": "developer"}

# Save prediction
curl -X POST http://127.0.0.1:5003/predictions \
  -H "X-API-Key: <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{"predicted_label": "Sandal", "confidence": 98.94}'
# Response: {"message": "Prediction saved.", "prediction": {...}}

# Get predictions with pagination
curl -H "X-API-Key: <your-api-key>" "http://127.0.0.1:5003/predictions?page=1&per_page=5"
```

---

## 📁 Project Structure

```
ML_WEEK08_B01/
├── flask_basics.py              # Task 8.1 — Flask basics & CRUD API
├── flask_ml_api.py              # Task 8.2 — ML model deployment
├── flask_image_api.py           # Task 8.3 — TFLite image classification API
├── flask_rest_api.py            # Task 8.4 — REST API with DB & Swagger
├── train_model.py               # Model training script
├── fashion_mnist_model.tflite   # TFLite model file
├── swagger.json                 # OpenAPI 3.0 specification
├── templates/
│   └── index.html               # HTML form for Task 8.2
└── README.md
```

---

## 🧠 Key Concepts Covered

- Flask application setup & routing
- RESTful API design (GET, POST, PUT, DELETE)
- ML model serialization & deployment (Pickle, TFLite)
- Image preprocessing & classification inference
- SQLite database integration with SQLAlchemy ORM
- API key authentication & security
- Pagination, filtering & sorting
- Request/response logging
- Swagger/OpenAPI documentation

---

## 💻 Tech Stack
* **Languages:** Python, HTML, JavaScript, Markdown
* **Frameworks:** Flask, Flask-SQLAlchemy, Flask-Swagger-UI
* **ML/DL:** Scikit-Learn, TFLite (ai-edge-litert), NumPy, Pillow
* **Database:** SQLite
* **Tools:** Git, VS Code, Postman, Swagger UI

---

## 📜 License
This project is licensed under the MIT License.