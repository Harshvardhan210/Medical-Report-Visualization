import streamlit as st
from firebase_config import auth, db


def register_user(email, password):
    try:
        # Create user in Firebase Authentication
        user = auth.create_user(email=email, password=password)

        # Store user details in Firestore
        db.collection("users").document(user.uid).set({
            "email": email,
            "password": password  # (Not recommended in real apps, but for testing)
        })

        st.success("User registered successfully! Please login.")
        return user.uid
    except Exception as e:
        st.error(f"Error: {e}")


def login_user(email, password):
    try:
        users_ref = db.collection("users").where("email", "==", email).stream()

        for user in users_ref:
            user_data = user.to_dict()
            if user_data["password"] == password:  # Compare stored password
                return True  # Successful login

        st.error("Invalid credentials")
        return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False