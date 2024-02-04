from flask import Flask, request, jsonify , render_template 
import joblib

app = Flask(__name__,static_url_path='/static')

# Load the trained Random Forest model
model = joblib.load('fraud_detection_model.joblib')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data sent from the frontend
        data = request.json
        print("Received data:", data)

        # Extract the input features from the JSON data
        features = [
            data.get('step', 0),
            data.get('amount', 0),
            data.get('oldbalanceOrg', 0),
            data.get('newbalanceOrg', 0),
            data.get('oldbalanceDest', 0),
            data.get('newbalancedest', 0),
            data.get('isFlaggedFraud', 0),
            data.get('cashout'),
            data.get('debit'),
            data.get('payment'),
            data.get('transfer')
        ]
        print("Input features:", features)
        # Make the prediction
        prediction = model.predict([features])[0]

        # Return the prediction result as JSON
        return jsonify({'prediction': int(prediction)}), 200
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
