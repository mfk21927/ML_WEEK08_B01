"""
Task 8.4: RESTful API with Database Integration
Complete REST API with SQLite database for storing model predictions.
Features: CRUD operations, pagination, filtering, logging, API key auth, Swagger UI.
"""

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps
from datetime import datetime, timezone
import logging
import os
import uuid
import json

# ──────────────────────────────────────────────
# App & Database Configuration
# ──────────────────────────────────────────────

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Step 1: Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# ──────────────────────────────────────────────
# Step 8: Logging Configuration
# ──────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Step 2: Database Models
# ──────────────────────────────────────────────

class Prediction(db.Model):
    """Stores model prediction results."""
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False, default='fashion_mnist')
    input_filename = db.Column(db.String(255), nullable=True)
    predicted_label = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    top_5 = db.Column(db.Text, nullable=True)  # JSON string of top-5 predictions
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'model_name': self.model_name,
            'input_filename': self.input_filename,
            'predicted_label': self.predicted_label,
            'confidence': self.confidence,
            'top_5': json.loads(self.top_5) if self.top_5 else None,
            'created_at': self.created_at.isoformat() + 'Z'
        }


class ApiKey(db.Model):
    """Stores valid API keys."""
    __tablename__ = 'api_keys'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# ──────────────────────────────────────────────
# Step 7: API Key Authentication Decorator
# ──────────────────────────────────────────────

def require_api_key(f):
    """Decorator that checks for a valid API key in the X-API-Key header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            logger.warning('Request missing API key from %s', request.remote_addr)
            return jsonify({'error': 'Missing API key. Provide X-API-Key header.'}), 401

        key_record = ApiKey.query.filter_by(key=api_key, is_active=True).first()
        if not key_record:
            logger.warning('Invalid API key attempt: %s...', api_key[:8])
            return jsonify({'error': 'Invalid or inactive API key.'}), 403

        g.api_key_owner = key_record.owner
        return f(*args, **kwargs)
    return decorated

# ──────────────────────────────────────────────
# Step 8: Request Logging Middleware
# ──────────────────────────────────────────────

@app.before_request
def log_request():
    logger.info('%s %s from %s', request.method, request.path, request.remote_addr)


@app.after_request
def log_response(response):
    logger.info('Response %s for %s %s', response.status_code, request.method, request.path)
    return response

# ──────────────────────────────────────────────
# Step 4: POST /predictions — Save a prediction
# ──────────────────────────────────────────────

@app.route('/predictions', methods=['POST'])
@require_api_key
def create_prediction():
    """Create a new prediction record."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    required_fields = ['predicted_label', 'confidence']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    prediction = Prediction(
        model_name=data.get('model_name', 'fashion_mnist'),
        input_filename=data.get('input_filename'),
        predicted_label=data['predicted_label'],
        confidence=float(data['confidence']),
        top_5=json.dumps(data['top_5']) if 'top_5' in data else None
    )
    db.session.add(prediction)
    db.session.commit()

    logger.info('Prediction #%d saved by %s', prediction.id, g.api_key_owner)
    return jsonify({'message': 'Prediction saved.', 'prediction': prediction.to_dict()}), 201

# ──────────────────────────────────────────────
# Step 5 & 6: GET /predictions — Pagination & Filtering
# ──────────────────────────────────────────────

@app.route('/predictions', methods=['GET'])
@require_api_key
def get_predictions():
    """
    List predictions with pagination and filtering.

    Query params:
        page      (int)  — page number, default 1
        per_page  (int)  — items per page, default 10 (max 100)
        model     (str)  — filter by model_name
        label     (str)  — filter by predicted_label
        start_date (str) — filter predictions after this ISO date
        end_date   (str) — filter predictions before this ISO date
        sort       (str) — 'asc' or 'desc' by created_at, default 'desc'
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    query = Prediction.query

    # Step 6: Filtering by model
    model_filter = request.args.get('model')
    if model_filter:
        query = query.filter(Prediction.model_name.ilike(f'%{model_filter}%'))

    # Filtering by label
    label_filter = request.args.get('label')
    if label_filter:
        query = query.filter(Prediction.predicted_label.ilike(f'%{label_filter}%'))

    # Step 6: Filtering by date range
    start_date = request.args.get('start_date')
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(Prediction.created_at >= start_dt)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use ISO 8601.'}), 400

    end_date = request.args.get('end_date')
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(Prediction.created_at <= end_dt)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use ISO 8601.'}), 400

    # Sorting
    sort_order = request.args.get('sort', 'desc')
    if sort_order == 'asc':
        query = query.order_by(Prediction.created_at.asc())
    else:
        query = query.order_by(Prediction.created_at.desc())

    # Pagination
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'predictions': [p.to_dict() for p in paginated.items],
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    })

# ──────────────────────────────────────────────
# GET /predictions/<id> — Single prediction
# ──────────────────────────────────────────────

@app.route('/predictions/<int:pred_id>', methods=['GET'])
@require_api_key
def get_prediction(pred_id):
    """Get a single prediction by ID."""
    prediction = db.session.get(Prediction, pred_id)
    if not prediction:
        return jsonify({'error': 'Prediction not found.'}), 404
    return jsonify({'prediction': prediction.to_dict()})

# ──────────────────────────────────────────────
# PUT /predictions/<id> — Update a prediction
# ──────────────────────────────────────────────

@app.route('/predictions/<int:pred_id>', methods=['PUT'])
@require_api_key
def update_prediction(pred_id):
    """Update an existing prediction."""
    prediction = db.session.get(Prediction, pred_id)
    if not prediction:
        return jsonify({'error': 'Prediction not found.'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    if 'model_name' in data:
        prediction.model_name = data['model_name']
    if 'input_filename' in data:
        prediction.input_filename = data['input_filename']
    if 'predicted_label' in data:
        prediction.predicted_label = data['predicted_label']
    if 'confidence' in data:
        prediction.confidence = float(data['confidence'])
    if 'top_5' in data:
        prediction.top_5 = json.dumps(data['top_5'])

    db.session.commit()
    logger.info('Prediction #%d updated by %s', pred_id, g.api_key_owner)
    return jsonify({'message': 'Prediction updated.', 'prediction': prediction.to_dict()})

# ──────────────────────────────────────────────
# DELETE /predictions/<id> — Delete a prediction
# ──────────────────────────────────────────────

@app.route('/predictions/<int:pred_id>', methods=['DELETE'])
@require_api_key
def delete_prediction(pred_id):
    """Delete a prediction by ID."""
    prediction = db.session.get(Prediction, pred_id)
    if not prediction:
        return jsonify({'error': 'Prediction not found.'}), 404

    db.session.delete(prediction)
    db.session.commit()
    logger.info('Prediction #%d deleted by %s', pred_id, g.api_key_owner)
    return jsonify({'message': f'Prediction #{pred_id} deleted.'}), 200

# ──────────────────────────────────────────────
# Utility: Generate API Key
# ──────────────────────────────────────────────

@app.route('/api-keys', methods=['POST'])
def create_api_key():
    """Generate a new API key. Provide {"owner": "your_name"} in JSON body."""
    data = request.get_json()
    if not data or 'owner' not in data:
        return jsonify({'error': 'Provide {"owner": "your_name"} in JSON body.'}), 400

    new_key = uuid.uuid4().hex
    api_key = ApiKey(key=new_key, owner=data['owner'])
    db.session.add(api_key)
    db.session.commit()

    logger.info('New API key created for %s', data['owner'])
    return jsonify({
        'message': 'API key created. Store it securely — it cannot be retrieved later.',
        'api_key': new_key,
        'owner': data['owner']
    }), 201

# ──────────────────────────────────────────────
# Steps 9-11: Swagger UI
# ──────────────────────────────────────────────

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Fashion MNIST Predictions API'}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/static/swagger.json')
def swagger_spec():
    """Serve the Swagger/OpenAPI specification."""
    spec_path = os.path.join(os.path.dirname(__file__), 'swagger.json')
    with open(spec_path, 'r') as f:
        return jsonify(json.load(f))

# ──────────────────────────────────────────────
# Home page
# ──────────────────────────────────────────────

@app.route('/')
def home():
    return jsonify({
        'message': 'Fashion MNIST Predictions REST API',
        'endpoints': {
            'POST /api-keys': 'Generate a new API key',
            'POST /predictions': 'Save a prediction (requires API key)',
            'GET /predictions': 'List predictions with pagination & filtering (requires API key)',
            'GET /predictions/<id>': 'Get single prediction (requires API key)',
            'PUT /predictions/<id>': 'Update prediction (requires API key)',
            'DELETE /predictions/<id>': 'Delete prediction (requires API key)',
            'GET /swagger': 'Swagger UI documentation'
        }
    })

# ──────────────────────────────────────────────
# Step 3: Initialize database & run
# ──────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed a default API key for testing
        if not ApiKey.query.first():
            default_key = 'test-api-key-12345'
            db.session.add(ApiKey(key=default_key, owner='developer'))
            db.session.commit()
            logger.info('Default API key seeded: %s', default_key)

    app.run(debug=True, port=5003)
