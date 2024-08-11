<h2>what is this repo?</h2>
<p>The repository contains a dummy recommendation system which can be used as a base for developing models.</p>
<p>Models can be developed in a separate file and imported into the main script. You can also use externally developed
models.</p>
<p>Currently, a simple random generator (uniform distribution) is being used as the output of models.</p>

<h2>How to use?</h2>
<p>Everything is dockerized. Simply run the following commands on your terminal/powershell:</p>

```
# Build the Docker images
docker-compose build

# Start the containers
docker-compose up --build

```
<p>And you will have your server running.<br>
To Access it, use the link http://localhost:8000. </p>
<h2>endpoints</h2>

| Endpoint               | description                                                                                | methods     | parameters |
|------------------------|--------------------------------------------------------------------------------------------|-------------|------------|
| generator/{model_name} | generates an integer based on model name \[currently just random numbers\]                 | POST        | model_name |
| recommend/{user_id}    | recommeds 5 integers for the user, either from the previousely cached or newly generated   | GET         | user_id    |   


<h2>requirements</h2>

<p>You need Docker and docker-compose to run this repo. Refer to the Docker documentation.<br>Also, make sure you have the docker service running on your machine and you have the privileges to run the docker-compose utility.</p>


