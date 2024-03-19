**Open-telemetry with Prometheus and Grafana using a simple Python flask app.**


**Step 1: Write code for a flask app.**

**Step 2: Create a Dockerfile for the flask app.**

**Step 3: Create a file named requirements.txt which includes all the packages that need to be installed.**

**Step 4: Create a docker compose file for flask-app, prometheus and jaeger. Prometheus will export metrics and Jaeger will export traces.**

**Step 5: Create a Prometheus folder with a prometheus.yml configuration file as shown below.**

**Step 6: Run and start all the containers in the background using the below command.**
$ docker-compose up -d


**Step 7: Visualization and monitoring. Now, we can run the following in the browser at:**
Flask Application: https://localhost:5000
For prometheus: http://localhost:9090
and jaeger: http://localhost:16686

**Note: Use the machine's IP address on which these services run.**


**Step 8: Now, run Grafana in a docker container and access it in a browser at http://localhost:3000.**

You can add Prometheus and jaeger as data sources and visualize the metrics and traces in the Grafana.
