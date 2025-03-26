from geopy.geocoders import Nominatim
import googlemaps
import smtplib
from datetime import datetime, timedelta
from dotenv import load_dotenv 
import os
import requests
from requests.exceptions import RequestException


# Load environment variables from .env file
load_dotenv()

# Get the API key and email credentials from the .env file
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
geolocator = Nominatim(user_agent="hospital_locator")

# Mock database for storing appointments
appointments = []

# Specialty keywords dictionary
SPECIALTY_KEYWORDS = {
    "General Physical": [
        "normal, general, physical, checkup",
        "general checkup",
        "consult",
    ],
    "neurologist": [
        "neurologist",
        "neuro",
        "nerves",
        "brain doctor",
        "nerve specialist",
    ],
    "dermatologist": [
        "dermatologist",
        "derma",
        "skin",
        "skin specialist",
        "skin doctor",
    ],
    "cardiologist": ["cardiologist", "cardio", "heart doctor", "heart specialist"],
    "orthopedist": [
        "orthopedist",
        "orthopedic",
        "bone doctor",
        "joint specialist",
        "orthopedics",
    ],
    "pediatrician": [
        "pediatrician",
        "child doctor",
        "pediatrics",
        "children specialist",
    ],
    "gynecologist": ["gynecologist", "gyno", "obstetrician", "obgyn", "women's doctor"],
    "psychiatrist": [
        "psychiatrist",
        "mental health",
        "psych doctor",
        "mind specialist",
    ],
    "dentist": ["dentist", "dental", "teeth doctor", "oral care", "tooth specialist"],
    "oncologist": ["oncologist", "cancer specialist", "cancer doctor", "oncology"],
    "endocrinologist": ["endocrinologist", "hormone specialist", "gland doctor"],
    "ophthalmologist": [
        "ophthalmologist",
        "eye doctor",
        "vision specialist",
        "eye care",
    ],
    "urologist": ["urologist", "urinary specialist", "kidney doctor", "urinary care"],
    "gastroenterologist": [
        "gastroenterologist",
        "gastro",
        "stomach doctor",
        "digestive care",
    ],
    "pulmonologist": ["pulmonologist", "lung doctor", "respiratory specialist"],
    "ent": ["ENT", "ear nose throat", "ENT specialist", "otolaryngologist"],
    "rheumatologist": [
        "rheumatologist",
        "arthritis specialist",
        "joint care",
        "autoimmune specialist",
    ],
    "radiologist": ["radiologist", "imaging specialist", "radiology"],
    "nephrologist": ["nephrologist", "kidney doctor", "renal specialist"],
    "allergist": ["allergist", "immunologist", "allergy specialist", "immune care"],
    "surgeon": ["surgeon", "surgery specialist", "operation doctor"],
}


def get_hospitals(
    location=None, latitude=None, longitude=None, specialization="hospital"
):
    """
    Fetch nearby hospitals based on location or GPS coordinates and specialization.
    """
    try:
        # Validate specialization
        keywords = SPECIALTY_KEYWORDS.get(specialization.lower(), ["hospital"])

        if location:
            # Use location name to get coordinates
            try:
                geo_result = geolocator.geocode(location)
                if not geo_result:
                    return {"error": "Invalid location provided."}
                lat, lng = geo_result.latitude, geo_result.longitude
            except RequestException as e:
                return {"error": f"Failed to resolve location: {str(e)}"}
        elif latitude and longitude:
            # Use provided latitude and longitude
            lat, lng = latitude, longitude
        else:
            return {"error": "Either location or GPS coordinates are required."}

        all_hospitals = []

        # Search using each keyword
        for keyword in keywords:
            places_result = gmaps.places_nearby(
                location=(lat, lng), radius=5000, type="hospital", keyword=keyword
            )
            # Add hospitals to the result list
            for place in places_result.get("results", []):
                all_hospitals.append(
                    {
                        "name": place["name"],
                        "address": place.get("vicinity", ""),
                        "rating": place.get("rating", "N/A"),
                        "user_ratings_total": place.get("user_ratings_total", 0),
                    }
                )

        # Remove duplicates by converting the list of dictionaries to a set and back
        unique_hospitals = [dict(t) for t in {tuple(d.items()) for d in all_hospitals}]
        return {"hospitals": unique_hospitals}

    except Exception as e:
        return {"error": str(e)}


def book_appointment(hospital_name, user_name, user_email, slot):
    """
    Book an appointment and send confirmation email.
    """
    if not all([hospital_name, user_name, user_email, slot]):
        return {"error": "Hospital name, user name, user email, and slot are required."}

    try:
        # Save appointment in mock database
        appointment = {
            "user_name": user_name,
            "user_email": user_email,
            "hospital_name": hospital_name,
            "slot": slot,
            "reminders_sent": False,
        }
        appointments.append(appointment)

        # Send confirmation email
        send_email(
            to_email=user_email,
            subject="Appointment Confirmation",
            body=f"Hi {user_name},\n\nYour appointment at {hospital_name} has been confirmed for {slot}.\n\nThank you!",
        )

        return {"message": "Appointment booked successfully!"}

    except Exception as e:
        return {"error": str(e)}


def send_email(to_email, subject, body):
    """
    Utility function to send an email.
    """
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            email_message = f"Subject: {subject}\n\n{body}"
            server.sendmail(SENDER_EMAIL, to_email, email_message)
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_reminders():
    """
    Send appointment reminders 15-120 minutes before the appointment.
    """
    now = datetime.now()
    for appointment in appointments:
        if appointment["reminders_sent"]:
            continue

        slot_time = datetime.strptime(appointment["slot"], "%Y-%m-%d %H:%M")
        time_diff = slot_time - now

        if timedelta(minutes=15) <= time_diff <= timedelta(minutes=120):
            # Send reminder email
            send_email(
                to_email=appointment["user_email"],
                subject="Appointment Reminder",
                body=f"Hi {appointment['user_name']},\n\nThis is a reminder for your appointment at {appointment['hospital_name']} scheduled for {appointment['slot']}.\n\nThank you!",
            )
            appointment["reminders_sent"] = True
