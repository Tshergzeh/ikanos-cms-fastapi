import httpx

from dotenv import load_dotenv
import os
load_dotenv()

class TestAuth:
    BASE_URL = os.getenv("base_url")
    LOGIN_URL = f"{BASE_URL}/api/auth/login"
    client = httpx.Client()

    wrong_username = client.post(LOGIN_URL, data={
        "username": "userv",
        "password": "password"
    })

    wrong_password = client.post(LOGIN_URL, data={
        "username": "user",
        "password": "password1"
    })

    correct_user_details = client.post(LOGIN_URL, data={
        "username": "user",
        "password": "password"
    })

    def test_wrong_username(self):
        # test wrong username
        assert self.wrong_username.status_code == 401

    def test_wrong_password(self):
        # test wrong password
        assert self.wrong_password.status_code == 401

    def test_correct_user_details(self):
        assert self.correct_user_details.status_code == 200
