from flask import Blueprint

# Define the blueprint
auth = Blueprint('auth', __name__)

# Import the routes for this blueprint
from . import views
