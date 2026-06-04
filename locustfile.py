from locust import HttpUser, task, between
import random

class RateLimiterUser(HttpUser):
    # Simulates a user waiting 0.1 to 0.5 seconds between requests
    wait_time = between(0.1, 0.5)

    @task
    def hit_api(self):
        # Generate a random user ID to bypass the 10-request limit 
        # and test the system's overall capacity
        user_id = f"test-user-{random.randint(1, 2000)}"
        
        # Send the GET request to the root endpoint with the fake API key
        self.client.get("/", headers={"X-API-Key": user_id})