# One Catalogue
První pokus o zpracování zadání 
Test for One Catalogue Team @ Heureka
We want our test to be close to what you would actually be doing if accepted. Therefore we would like you to create a small Catalogue service. 
Our goal is to have the assignment easy enough to be doable within 6-8 hours, yet difficult enough so that you can showcase what you are capable of. If you think we aren’t meeting either of those goals, please let us know!
Assignment
Create a service in Python/Golang. Publish its source code on GitHub or GitLab.

Minimum requirements:
Consumes messages from Kafka (details below)
Stores data based on those messages (database of your choice) #- zvolil jsem MongoDB, pro správnou funkci je potřeba nainstalovat
Not all data are present in the messages, some need to be fetched from an existing API
When a product (see below) is matched with another, check how many parameters they have in common and how many differ, store that information 
Test your service
Optional:
Deploy the service, or make it as close to deployable as you can
Utilize CI/CD tools (Travis CI, Circle CI, GitLab CI...) as you see fit
Manage your python/golang dependencies the way you think is the best 
Make it easy to run your service locally
Expose prometheus metrics
Kafka
Bootstrap Server: pkc-4ygn6.europe-west3.gcp.confluent.cloud:9092
Security Protocol: SASL_SSL
Username: KTIDDULUPUETVKOR
Password: h0EsaIyNsFKrejrLmVsJZwOahA+2wgXBbSdHO/jJNyrEJ0p19LV+bdYeD2XR3gRU
SASL mechanism: PLAIN
Topic: catalogue_source
Data in Kafka
Every message is json and has the following format: {metadata: {type:”...”}, payload: {}}
There is no uniqueness guarantee, some messages might be present multiple times.
There are following types:
offer
Belongs to a category
Has ID
Has a name
Has a description
Has multiple parameters (nested inside)
Same ‘product’ can be found in other eshops, not included in data, information can be found through API
category
Has a name
Can have a parent category
API
Docker image, exposing the API at port 5000: <>
To run, use docker run -it -p 5000:5000 heurekaoc/testday-api:latest 
Required headers: {“Auth”: “827e8e1a-119c-48e2-af1c-cef81f933a5a”}
GET /offer-matches/<offer-id>
Returns a json with: {“matching_offers”: [“offer-1-id”, “offer-2-i







