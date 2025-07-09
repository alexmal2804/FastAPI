from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = [
    {"username": "alice", "password": "qwerty123"},
    {"username": "john_doe", "password": "securepassword123"},
    {"username": "bob_smith", "password": "mypassword123"}
]
