# Deephaven imports
from deephaven import DynamicTableWriter
from deephaven import dtypes as dht
from deephaven.learn import gather
from deephaven.csv import read
from deephaven import learn

# Machine learning imports
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Python imports
import numpy as np, random, threading, time

iris_raw = read("https://media.githubusercontent.com/media/deephaven/examples/main/Iris/csv/iris.csv")

classes = {}
num_classes = 0
def get_class_number(c):
    global classes, num_classes
    if c not in classes:
        classes[c] = num_classes
        num_classes += 1
    return classes[c]

iris = iris_raw.update(formulas = ["Class = (int)(byte)get_class_number(Class)"])

# Our neural network
model = Sequential()
model.add(Dense(16, activation = tf.nn.relu))
model.add(Dense(12, activation = tf.nn.relu))
model.add(Dense(3, activation = tf.nn.softmax))

# A function that trains the model
def train_model(X_train, Y_train):
    model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 0.01), loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True), metrics = ["accuracy"])
    model.fit(x = X_train, y = Y_train, epochs = 100)

# A function that gets the model's predictions on input data
def predict_with_model(features):
    if features.ndim == 1:
        features = np.expand_dims(features, 0)
    predictions = model.predict(features)
    return np.array([np.argmax(item) for item in predictions], dtype = np.intc)

# A function to gather data from table columns into a NumPy array of doubles
def table_to_array_double(rows, cols):
    return gather.table_to_numpy_2d(rows, cols, np_type = np.double)

# A function to gather data from table columns into a NumPy array of doubles
def table_to_array_int(rows, cols):
    return gather.table_to_numpy_2d(rows, cols, np_type = np.intc)

# A function to extract a list element and cast to an integer
def get_predicted_class(data, idx):
    return int(data[idx])


print('about to fail')
# Use the learn function to train our neural network
learn.learn(
    table = iris,
    model_func = train_model,
    inputs = [learn.Input(["SepalLengthCM", "SepalWidthCM", "PetalLengthCM", "PetalWidthCM"], table_to_array_double), learn.Input(["Class"], table_to_array_int)],
    outputs = None,
    batch_size = 150
)

print('didn\'t crash!')
print('numpy ' + np.__file__)
print('tensorflow ' + tf.__file__)
print('deephaven ' + deephaven.__file__)
exit(0)

