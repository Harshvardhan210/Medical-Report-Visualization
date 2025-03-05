import firebase_admin
from firebase_admin import credentials, auth, firestore

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("ServiceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Firestore database reference