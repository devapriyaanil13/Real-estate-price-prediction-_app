from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import json

app = Flask(__name__)

# Load trained model
model = pickle.load(open('m.pkl', 'rb'))

# Load feature columns with 'location' first
with open('columns.json', 'r') as f:
    data_columns = json.load(f)['data_columns']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_location_names')
def get_location_names():
    # Return only location names (exclude last 3: sqft, bath, bhk)
    return jsonify({'locations': data_columns[:-3]})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        location = data['location'].strip().lower()
        sqft = float(data['sqft'])
        bath = int(data['bath'])
        bhk = int(data['bhk'])

        # Initialize feature vector
        x = np.zeros(len(data_columns), dtype=np.float64)

        # One-hot encode location
        if location in data_columns:
            loc_index = data_columns.index(location)
            x[loc_index] = 1

        # Assign numerical features by name
        if 'total_sqft' in data_columns:
            x[data_columns.index('total_sqft')] = sqft
        if 'bath' in data_columns:
            x[data_columns.index('bath')] = bhk
        if 'bhk' in data_columns:
            x[data_columns.index('bhk')] = bath

        # DEBUG LOGS
        print("======== DEBUG LOG ========")
        print("Input received:")
        print(f"Location: {location}, Sqft: {sqft}, Bath: {bath}, BHK: {bhk}")
        print("Non-zero values in feature vector:")
        for i, val in enumerate(x):
            if val != 0:
                print(f"{data_columns[i]} => {val}")
        print("===========================")

        prediction = model.predict([x])[0]
        return jsonify({'price': round(prediction, 2)})

    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
