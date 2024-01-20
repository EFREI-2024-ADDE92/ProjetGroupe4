from locust import HttpUser, task

class SimulatedUser(HttpUser):
    @task
    def send_request(self):
        self.client.get("/predict?sepL=5.1&petL=1.4&sepW=3.5&petW=0.1",name="/predict1")
        self.client.get("/predict?sepL=6.4&petL=5.3&sepW=2.3&petW=3.2",name="/predict2")
        self.client.get("/predict?sepL=5.1&petL=1.4&sepW=3.5&petW=0.1",name="/predict3")
        self.client.get("/predict?sepL=5.1&petL=1.4&sepW=3.5&petW=0.1",name="/predict4")

