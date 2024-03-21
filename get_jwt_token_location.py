from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Assuming JWT_TOKEN_LOCATION has been previously configured
jwt_token_location = app.config.get('JWT_TOKEN_LOCATION')

print("JWT Token Location:", jwt_token_location)