class Passenger:

    def __init__(self, raw_data):
        self.gender = raw_data.get('gender')
        self.ticket_type = raw_data.get('ticket_type') if raw_data.get('ticket_type') else raw_data.get('type')
        self.first_name = raw_data.get('first_name')
        self.last_name = raw_data.get('last_name')
        self.date_of_birth = raw_data.get('date_of_birth')
        self.citizenship = raw_data.get('citizenship')
        self.document_number = dict(raw_data.get('document')).get('number')
        self.document_expires_at = dict(raw_data.get('document')).get('expires_at')
        self.document_iin = dict(raw_data.get('document')).get('iin')


class Booking:

    def __init__(self, raw_data):
        self.booking_id = raw_data.get('id') or raw_data.get('offer_id')
        self.phone = raw_data.get('phone')
        self.email = raw_data.get('email')
        self.offer = raw_data.get('offer')
        self.passengers = [Passenger(row) for row in raw_data.get('passengers')]

    def __dict__(self):
        return {
            'id': self.booking_id,
            'phone': self.phone,
            'email': self.email,
            'offer': self.offer,
            'passengers': [p.__dict__ for p in self.passengers]
        }

