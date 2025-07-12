import httpx

from dotenv import load_dotenv
import os
load_dotenv()

class TestServices:
    BASE_URL = os.getenv("base_url")
    client = httpx.Client()

    no_auth = client.patch(f"{BASE_URL}/api/admin/services/1/approve")

    def test_no_auth(self):
        assert self.no_auth.status_code == 401
