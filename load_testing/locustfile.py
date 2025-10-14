from locust import HttpUser, task


class APITestUser(HttpUser):
    """A user class for load testing the API endpoints."""

    @task
    def test_list_api(self):
        """Test the list of API endpoints."""

        self.client.get("/api/parameters/")
        self.client.get("/api/regions/")
        self.client.get("/api/monthly/")
        self.client.get("/api/seasonal/")
        self.client.get("/api/climate/")
