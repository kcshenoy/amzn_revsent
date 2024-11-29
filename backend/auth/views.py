from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from . import auth
from .forms import SignupForm
from .models import User  # Import the User model

# Route for the signup page
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':  # Explicitly check for POST request
        # Check if form is valid
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            # Check if the user already exists
            if User.get_user_by_email(email):
                return jsonify({"error": "User already exists!"}), 400

            # Create the user via the model
            User.create_user(email, password)

            return jsonify({"message": "User registered successfully!"}), 201

        # Return validation errors if form is invalid
        return jsonify({"error": "Form validation failed", "messages": form.errors}), 400

    # For testing purposes, when accessing via GET, just render a message (or template)
    return jsonify({"message": "Signup form is ready"})


# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the credentials are correct
        if User.check_password(email, password):
            # Create JWT token for the user
            access_token = create_access_token(identity=email)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401

    return render_template('login.html')
