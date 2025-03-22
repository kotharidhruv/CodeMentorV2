import time
from flask import Flask
from elasticsearch import Elasticsearch, ConnectionError
import tensorflow as tf
import numpy as np

# Elasticsearch configuration
es_host = {'host': 'localhost', 'port': 9200}
es = None
max_retries = 5
retry_delay = 10  # seconds

# Retry logic for Elasticsearch connection
for attempt in range(max_retries):
    try:
        es = Elasticsearch([es_host])
        if es.ping():
            print("Connected to Elasticsearch")
            break
    except ConnectionError:
        print(f"Connection to Elasticsearch failed. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)
else:
    raise Exception("Failed to connect to Elasticsearch after multiple attempts")

# Example TensorFlow model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Example data
x_train = np.random.rand(100, 10)
y_train = np.random.rand(100, 1)

# Train the model
model.fit(x_train, y_train, epochs=10)

# Your application code here
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
