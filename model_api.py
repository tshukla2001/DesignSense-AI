from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the model and encoders
model = tf.keras.models.load_model("design_suggestion_model.h5")

# Load tokenizer and encoders
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
with open("font_encoder.pkl", "rb") as f:
    font_encoder = pickle.load(f)
with open("palette_encoder.pkl", "rb") as f:
    palette_encoder = pickle.load(f)

# Initialize Flask App
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    description = data.get('description', '')

    # Preprocess input
    sequence = tokenizer.texts_to_sequences([description])
    padded_sequence = pad_sequences(sequence, maxlen=20, padding='post')

    # Make predictions
    font_pred, palette_pred = model.predict(padded_sequence)
    suggested_font = font_encoder.inverse_transform([font_pred.argmax()])[0]
    suggested_palette = palette_encoder.inverse_transform([palette_pred.argmax()])[0]

    # Send response
    return jsonify({
        "font": suggested_font,
        "palette": suggested_palette
    })

if __name__ == '__main__':
    app.run(debug=True)
