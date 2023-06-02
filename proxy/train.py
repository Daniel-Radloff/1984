from sklearn.model_selection import train_test_split
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
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

# Split data into training / test sets
print(C_ORANGE + "Splitting Train/Test..." + C_RESET)
X_train, X_test, Y_train, Y_test = train_test_split(
    messages, labels,
    test_size=0.2
)

#====== DEFINE MODEL ======#
model = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("nb", MultinomialNB())
])

#===== TRAIN MODEL =====#
print(C_ORANGE + "Training..." + C_RESET)

model.fit(X_train, Y_train)

#===== SAVE MODEL =====#
print(C_ORANGE + "Saving Model..." + C_RESET)
joblib.dump(model, "spamDet.joblib")

score = model.score(X_test, Y_test)
print("Test prediction accuracy: " + C_GREEN + str(score) + C_RESET)
