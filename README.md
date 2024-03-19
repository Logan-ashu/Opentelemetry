**Open-telemetry with Prometheus and Grafana using simple python flask app.**


**Step 1: Write code for a flask app.**

from flask import Flask, render_template, request, redirect, url_for, flash
from prometheus_flask_exporter import PrometheusMetrics
from flask_opentracing import FlaskTracing
from jaeger_client import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key

metrics = PrometheusMetrics(app)

# Jaeger configuration
config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
    },
    service_name='flask-app',
)
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # Place your data processing or saving logic here
        print(f"Received submission: {name}, {email}")  # Placeholder for saving data

        with jaeger_tracer.start_span('form-submit') as span:
            span.log_kv({'event': 'form-submit', 'name': name, 'email': email})

        flash('Form submitted successfully!', 'success')
        # Stay on the same page without redirecting
        return render_template('form.html')

    # Even if it's a GET request, we want to trace it
    with jaeger_tracer.start_span('hello-world') as span:
        span.log_kv({'event': 'hello-world', 'value': 'user accessed /'})

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)


Step 2: Create a Dockerfile for the flask app.

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]



Step 3: 
Create a file named as requirements.txt which includes all the packages that needs to be installed.


Step 4: Create a docker compose file for flask-app, prometheus and jaeger. Prometheus will export metrics and jaeger exports traces.

**
version: '3.7'
services:
  flask-app:
    build: ./flask-app
    ports:
      - "5000:5000"
    environment:
      JAEGER_AGENT_HOST: jaeger
      JAEGER_AGENT_PORT: 6831

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - flask-app

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "6831:6831/udp"

**

Step 5: Create a prometheus folder with a prometheus.yml configuration file as shown below.

**
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask-app'
    static_configs:
      - targets: ['flask-app:5000', 'localhost:9090', '10.0.0.130:16686']

**

Step 6: Run and start all the containers in the background using the below command.

$ docker-compose up -d


Step 7: Visualization and monitoring. Now, we can run the flask application by running it in the browser at:
https://localhost:5000
For prometheus: http://localhost:9090
and jaeger: http://localhost:16686

**Note: Use IP address of the machine on which these services are running.**


Step 8: Now, run grafana in a docker container and access it in a browser at: http://localhost:3000.
You can add prometheus and jaeger as data source and visualize the metrics and traces in the grafana.
