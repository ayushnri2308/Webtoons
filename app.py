from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import db, Webtoon, webtoon_schema,User
from marshmallow import ValidationError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
from flask_caching import Cache


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


# Redis connection
redis_connection = Redis(host='localhost', port=6379, db=0)

# Set up rate limiting with Redis as the backend
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379",
    default_limits=["200 per day", "50 per hour"],
)

# Configuration (from config.py)
app.config.from_pyfile('config.py')

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

# Fetch all webtoons
@app.route('/webtoons', methods=['GET'])
@cache.cached(timeout=60)  # Cache results for 60 seconds
def get_webtoons():
    webtoons = Webtoon.query.all()
    return jsonify([webtoon.to_dict() for webtoon in webtoons])

# Add a new webtoon (JWT protected)
@app.route('/webtoons', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def add_webtoon():
    data = request.get_json()

    # Validate incoming data using Marshmallow
    try:
        validated_data = webtoon_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Find the lowest available ID
    result = db.session.query(Webtoon.id).order_by(Webtoon.id).all()
    ids = [r.id for r in result]
    lowest_id = next((i for i in range(1, len(ids) + 2) if i not in ids), len(ids) + 1)

    # Create the new webtoon entry with the lowest ID
    new_webtoon = Webtoon(id=lowest_id, title=validated_data['title'], summary=validated_data['summary'], characters=validated_data['characters'])
    db.session.add(new_webtoon)
    db.session.commit()

    return jsonify({'message': 'Webtoon added successfully', 'id': lowest_id}), 201

# Fetch a specific webtoon by ID
@app.route('/webtoons/<int:webtoon_id>', methods=['GET'])
def get_webtoon(webtoon_id):
    with db.session() as session:
        webtoon = session.get(Webtoon, webtoon_id)
        if webtoon is None:
            return jsonify({'error': 'Webtoon not found'}), 404
        return jsonify(webtoon.to_dict())

# Delete a webtoon by ID (JWT protected)
@app.route('/webtoons/<int:webtoon_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("10 per minute")
def delete_webtoon(webtoon_id):
    with db.session() as session:
        webtoon = session.get(Webtoon, webtoon_id)
        if webtoon is None:
            return jsonify({'error': 'Webtoon not found'}), 404

        session.delete(webtoon)
        session.commit()

    return jsonify({'message': 'Webtoon deleted successfully!'}), 200

# Generate JWT token for testing
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
