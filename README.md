# flux_task_generator
Problem 1:
Kapacitor provides a way to monitor and configure alerts according to the usecase. But all the alerts created by Kapacitor is by using TICK scripts which are are not suitable for writing complex queries and scaling.

Approach:
But flux tasks can be used to not only write complex queries but also very easy to scale to multiple sites and for multiple use cases just by changing some parts of the query.
To create a flux task and create an alert, one has to write the flux query along with frequency by which the query has to run(every 1 minute, 5 minute) along with the influx credentials and deploy it on kapacitor.
To create an alert out of this set a condition where kapcitor should raise an alert along with the endpoint where this alert should be directed to with the alert message. 

Problem 2:
While scaling the flux tasks it becomes cumbersome to manually changes all the attributes to scale the same flux task to different sites. It is also time consuming process to configure an alert for different usecases(example:wrong command,deadman)

Approach:
The Flux task generator solves this problem by automatically configuring an alert by using the meta information of the alert queried from the database and deploys it on kapcitor as an alert.

To run the application, following need to be done:

1. create an .env file with all the attributes mentioned in env.example
2. Run the commands given below.

pip3 install requirements.txt

python3 src/main.py
