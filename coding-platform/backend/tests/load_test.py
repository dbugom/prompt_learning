"""
Load Testing Script using Locust
Run with: locust -f load_test.py --host=http://localhost:8000
"""

from locust import HttpUser, task, between
import random

class PlatformUser(HttpUser):
    """Simulated user for load testing"""

    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    token = None

    def on_start(self):
        """Register and login when user starts"""
        # Create unique user
        username = f"loadtest_user_{random.randint(1000, 9999)}"
        password = "testpass123"

        # Register
        response = self.client.post("/api/auth/register", json={
            "email": f"{username}@example.com",
            "username": username,
            "password": password
        })

        if response.status_code in [200, 201]:
            data = response.json()
            self.token = data.get("access_token")
        else:
            # Try to login if already exists
            response = self.client.post("/api/auth/login", data={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")

    def get_headers(self):
        """Get authorization headers"""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    @task(3)
    def view_home(self):
        """View home page"""
        self.client.get("/")

    @task(2)
    def health_check(self):
        """Check health endpoint"""
        self.client.get("/health")

    @task(5)
    def get_lessons(self):
        """Get lessons list"""
        self.client.get("/api/lessons", headers=self.get_headers())

    @task(4)
    def get_progress(self):
        """Get user progress"""
        self.client.get("/api/progress/overview", headers=self.get_headers())

    @task(3)
    def get_lesson_progress(self):
        """Get lessons with progress"""
        self.client.get("/api/progress/lessons", headers=self.get_headers())

    @task(1)
    def execute_code(self):
        """Execute simple Python code"""
        code = """
# Simple calculation
result = 2 + 2
print(result)
"""
        self.client.post(
            "/api/code/execute",
            headers=self.get_headers(),
            json={
                "code": code,
                "language": "python"
            }
        )

    @task(1)
    def get_submissions(self):
        """Get user submissions"""
        self.client.get("/api/code/submissions", headers=self.get_headers())

class AnonymousUser(HttpUser):
    """Simulated anonymous user (no authentication)"""

    wait_time = between(2, 5)

    @task(5)
    def view_home(self):
        """View home page"""
        self.client.get("/")

    @task(3)
    def health_check(self):
        """Check health endpoint"""
        self.client.get("/health")

    @task(1)
    def try_unauthorized_access(self):
        """Try to access protected endpoints without auth"""
        self.client.get("/api/lessons")
        self.client.get("/api/progress/overview")
