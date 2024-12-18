from flask import Flask, request, jsonify
import pickle
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Load the pre-trained model
MODEL_PATH = "model.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Define the route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions.
    Expects JSON input with 'sepal_length', 'sepal_width', 'petal_length', 'petal_width'.
    """
    try:
        # Parse input JSON
        data = request.get_json()
        sepal_length = data['sepal_length']
        sepal_width = data['sepal_width']
        petal_length = data['petal_length']
        petal_width = data['petal_width']

        # Create feature array
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        # Make prediction
        prediction = model.predict(features)
        predicted_class = prediction[0]

        # Return response
        return jsonify({
            'prediction': predicted_class,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        })

# Define a health check route
@app.route('/', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the app is running.
    """
    return jsonify({'message': 'Iris Prediction API is running', 'success': True})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
