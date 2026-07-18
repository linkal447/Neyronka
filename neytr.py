import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Embedding,
    LSTM,
    Dense
)


# Загружаем датасет

data = pd.read_csv("dataset.csv")


texts = data["text"]


# жанр

genre_encoder = LabelEncoder()

genres = genre_encoder.fit_transform(
    data["genre"]
)


# параметры

difficulty_encoder = LabelEncoder()

difficulty = difficulty_encoder.fit_transform(
    data["difficulty"]
)


enemies = data["enemies"].astype(int)
obstacles = data["obstacles"].astype(int)
coins = data["coins"].astype(int)



# перевод текста в числа

tokenizer = Tokenizer(
    num_words=5000
)

tokenizer.fit_on_texts(texts)


X = tokenizer.texts_to_sequences(texts)

X = pad_sequences(
    X,
    maxlen=40
)



# модель

input_layer = Input(
    shape=(40,)
)


x = Embedding(
    5000,
    64
)(input_layer)


x = LSTM(64)(x)


# несколько выходов

genre_output = Dense(
    3,
    activation="softmax",
    name="genre"
)(x)


difficulty_output = Dense(
    3,
    activation="softmax",
    name="difficulty"
)(x)


enemy_output = Dense(
    1,
    activation="sigmoid",
    name="enemy"
)(x)


obstacle_output = Dense(
    1,
    activation="sigmoid",
    name="obstacle"
)(x)


coin_output = Dense(
    1,
    activation="sigmoid",
    name="coin"
)(x)



model = Model(
    input_layer,
    [
        genre_output,
        difficulty_output,
        enemy_output,
        obstacle_output,
        coin_output
    ]
)


model.compile(
    optimizer="adam",

    loss=[
        "sparse_categorical_crossentropy",
        "sparse_categorical_crossentropy",
        "binary_crossentropy",
        "binary_crossentropy",
        "binary_crossentropy"
    ],

    metrics=["accuracy"]
)



model.fit(
    X,
    [
        genres,
        difficulty,
        enemies,
        obstacles,
        coins
    ],
    epochs=50
)



model.save(
    "game_ai.keras"
)


print("Обучение завершено")