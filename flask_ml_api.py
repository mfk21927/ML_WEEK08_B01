from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open('model.pkl', 'rb'))

# Route to render HTML form
@app.route('/')
def index():
    return render_template('index.html') 

# Predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # 1. Define the names corresponding to 0, 1, and 2
    class_names = ['Setosa', 'Versicolour', 'Virginica']
    
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        prediction_index = int(model.predict(features)[0])
        
        # 2. Get the name using the index
        flower_name = class_names[prediction_index]
        
        # 3. Return both the index and the name
        return jsonify({
            'prediction_index': prediction_index,
            'predicted_Flower': flower_name
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
        
        # Reshape features for prediction
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)
        
        return jsonify({'prediction': int(prediction[0])})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)