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

