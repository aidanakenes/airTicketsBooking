from typing import List
import json


class Booking:

    def __init__(self, raw_data):
        self.booking_id = raw_data.get('booking_id')
        self.phone = raw_data.get('phone')
        self.email = raw_data.get('email')
        self.offer = raw_data.get('offer') if raw_data.get('details') is None else json.loads(raw_data.get('details'))
        self.passengers = raw_data.get('passenger') if raw_data.get('info') is None else json.loads(
            raw_data.get('info'))

    def __dict__(self):
        return {
            'id': self.booking_id,
            'phone': self.phone,
            'email': self.email,
            'offer': self.offer,
            'passengers': self.passengers
        }
