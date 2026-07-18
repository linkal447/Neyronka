from flask import Flask, request, jsonify
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = Flask(__name__)


model = tf.keras.models.load_model(
    "genre_model.keras"
)


with open("tokenizer.pkl","rb") as f:
    tokenizer = pickle.load(f)


with open("encoder.pkl","rb") as f:
    encoder = pickle.load(f)



@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    text = data["text"]


    seq = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(
        seq,
        maxlen=20
    )


    prediction = model.predict(padded)


    index = prediction.argmax()


    genre = encoder.inverse_transform(
        [index]
    )[0]


    return jsonify({
        "genre": genre
    })



app.run(
    host="0.0.0.0",
    port=5000
)