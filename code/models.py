from typing import List
import json


class Passenger:

    def __init__(self, raw_data):
        self.gender = raw_data.get('gender')
        self.ticket_type = raw_data.get('ticket_type') if raw_data.get('ticket_type') else raw_data.get('type')
        self.first_name = raw_data.get('first_name')
        self.last_name = raw_data.get('last_name')
        self.date_of_birth = raw_data.get('date_of_birth')
        self.citizenship = raw_data.get('citizenship')
        self.document_number = dict(raw_data.get('document')).get('number') if not raw_data.get(
            'numbers') else raw_data.get('numbers')
        self.document_expires_at = dict(raw_data.get('document')).get('expires_at') if not raw_data.get(
            'expires_at') else raw_data.get('expires_at')
        self.document_iin = dict(raw_data.get('document')).get('iin') if not raw_data.get('iin') else raw_data.get(
            'iin')


class Booking:

    def __init__(self, raw_data):
        self.booking_id = raw_data.get('id') or raw_data.get('offer_id')
        self.phone = raw_data.get('phone')
        self.email = raw_data.get('email')
        self.offer = raw_data.get('offer') if raw_data.get('details') is None else json.loads(raw_data.get('details'))
        self.passengers: List[Passenger]

        if raw_data.get('passengers') is not None:
            self.passengers = [Passenger(row) if type(row) is not Passenger else row for row in
                               raw_data.get('passengers')]

    def __dict__(self):
        return {
            'id': self.booking_id,
            'phone': self.phone,
            'email': self.email,
            'offer': self.offer,
            'passengers': [p.__dict__ for p in self.passengers]
        }
