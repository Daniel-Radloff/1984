import pickle
import tensorflow as tf
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.model_selection import train_test_split
import pandas as pd

C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_BLUE = "\033[94m"
C_ORANGE = "\033[93m"
C_RESET = "\033[0m"

#===== LOAD DATA =====#
print(C_ORANGE + "Loading data..." + C_RESET)
data = pd.read_csv('spam.csv', engine="python")
print(C_BLUE + "DATA:\n" + str(data.dtypes) + C_RESET)
messages = data['message'].values
labels = data['label'].values

#===== PREPROCESSING =====#
print(C_ORANGE + "Preprocessing..." + C_RESET)
tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(messages)
sequences = tokenizer.texts_to_sequences(messages)
paddedSeqs = pad_sequences(sequences, padding='post')

# Split data into training / test sets
print(C_ORANGE + "Splitting Train/Test..." + C_RESET)
X_train, X_test, Y_train, Y_test = train_test_split(
    paddedSeqs, labels,
    test_size=0.2
)

#====== DEFINE MODEL ======#
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(10000, 16, input_length=paddedSeqs.shape[1]),
    tf.keras.layers.Bidirectional(tf.keras.layers.GRU(32)),
    # tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#===== TRAIN MODEL =====#
print(C_ORANGE + "Training..." + C_RESET)
model.fit(X_train, Y_train, epochs=10, validation_data=(X_test, Y_test))

#===== SAVE DATA =====#
print(C_ORANGE + "Saving Data..." + C_RESET)

# Save model
model.save('spamDet.h5')

# Save tokenizer
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save padded sequences / labels
np.save("paddedSeqs.npy", paddedSeqs)
np.save("labels.npy", labels)

def predictSpam(model, tokenizer, text):
    sequence = tokenizer.texts_to_sequences([text])
    paddedSeq = pad_sequences(sequence, maxlen=paddedSeqs.shape[1])
    prediction = model.predict(paddedSeq)
    return prediction[0][0]

print(C_GREEN + "Predicting..." + C_RESET)
text = "New TEXTBUDDY Chat 2 horny guys in ur area 4 just 25p Free 2 receive Search postcode or at gaytextbuddy.com. TXT ONE name to 89693"
print(predictSpam(model, tokenizer, text))