import pickle
import numpy as np
import tensorflow as tf
from keras.utils import pad_sequences

tf.get_logger().setLevel("ERROR")
tf.autograph.set_verbosity(1)

def predictSpam(model, tokenizer, text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=padded_sequences.shape[1])
    prediction = model.predict(padded_sequence)
    return prediction[0][0]

def loadSpamData():
    global model, tokenizer, padded_sequences
    # Load the model
    model = tf.keras.models.load_model('spamDet.h5')

    # Load the tokenizer
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # Load padding sequences
    padded_sequences = np.load("paddedSeqs.npy")


loadSpamData()

# Make a prediction
text = "New TEXTBUDDY Chat 2 horny guys in ur area 4 just 25p Free 2 receive Search postcode or at gaytextbuddy.com. TXT ONE name to 89693"
print(predictSpam(model, tokenizer, text))
