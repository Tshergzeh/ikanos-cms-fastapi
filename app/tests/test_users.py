import httpx

from dotenv import load_dotenv
import os
load_dotenv()

class TestServices:
    BASE_URL = os.getenv("base_url")
    client = httpx.Client()

    no_auth = client.post(f"{BASE_URL}/api/users", data={
        "username": "new_user",
        "password": "password",
        "is_admin": True
    })

    existing_user = client.post(f"{BASE_URL}/api/users", data={
        "username": "user",
        "password": "password",
        "is_admin": False
    })

    def test_no_auth(self):
        assert self.no_auth.status_code == 401
    