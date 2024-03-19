**Open-telemetry with Prometheus and Grafana using simple python flask app.**


**Step 1: Write code for a flask app.**

**Step 2: Create a Dockerfile for the flask app.**

**Step 3: Create a file named as requirements.txt which includes all the packages that needs to be installed.**

**Step 4: Create a docker compose file for flask-app, prometheus and jaeger. Prometheus will export metrics and jaeger exports traces.**

**Step 5: Create a prometheus folder with a prometheus.yml configuration file as shown below.**
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
