from datetime import datetime
import json

import helpers
import models


@helpers.with_connection
async def create_booking(booking, *args, **kwargs):
    conn = kwargs.pop('connection')

    for passenger in booking.passengers:
        passenger_uid = await _insert_passenger(conn, passenger)
        offer_details_uid = await _insert_offer(conn, booking)
        booking_id = await _insert_booking(conn, booking, passenger_uid, offer_details_uid)

    return booking_id


async def _insert_passenger(conn, passenger):
    expires_at = datetime.strptime(passenger.date_of_birth, '%Y-%m-%d')
    date_of_birth = datetime.strptime(passenger.date_of_birth, '%Y-%m-%d')

    stmt = """INSERT INTO passenger (gender, ticket_type, first_name, last_name, date_of_birth, citizenship, numbers, expires_at, iin)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) 
            RETURNING passenger_id;"""

    uid = await conn.fetchval(stmt, passenger.gender, passenger.ticket_type, passenger.first_name,
                              passenger.last_name, date_of_birth, passenger.citizenship,
                              passenger.document_number, expires_at, passenger.document_iin)

    return uid


async def _insert_offer(conn, booking):
    stmt = """INSERT INTO offer_details (details)
            VALUES ($1) RETURNING offer_details_id;"""
    uid = await conn.fetchval(stmt, json.dumps(booking.offer))

    return uid


async def _insert_booking(conn, booking, passenger_id, offer_details_id):
    stmt = """INSERT INTO booking (offer_id, phone, email, offer_details_id, passenger_id)
            VALUES ($1, $2, $3, $4, $5) RETURNING offer_id;"""
    uid = await conn.execute(stmt, booking.booking_id, booking.phone, booking.email,
                             offer_details_id, passenger_id)

    return uid


@helpers.with_connection
async def get_booking(booking_id, *args, **kwargs):
    conn = kwargs.pop('connection')

    data = await conn.fetchrow("""select b.offer_id, b.phone, b.email, od.details from booking b
inner join offer_details od on b.offer_details_id=od.offer_details_id where offer_id=$1""", booking_id)

    passengers_data = await conn.fetch(
        """select p.gender, p.ticket_type, p.first_name, p.last_name, p.date_of_birth, p.citizenship, p.numbers, p.expires_at, p.iin from passenger p inner join booking b on p.passenger_id=b.passenger_id where b.offer_id=$1""",
        booking_id)
    passengers = []
    for p in passengers_data:
        passengers.append({
            'gender': p.get('gender'),
            'ticket_type': p.get('ticket_type'),
            'first_name': p.get('first_name'),
            'last_name': p.get('last_name'),
            'date_of_birth': p.get('date_of_birth'),
            'citizenship': p.get('citizenship'),
            'document': {
                'number': p.get('numbers'),
                'iin': p.get('iin'),
                'expires_at': p.get('expires_at')
            }
        })

    data = {
        'id': booking_id,
        'phone': data.get('phone'),
        'email': data.get('email'),
        'offer': json.loads(data.get('details')),
        'passengers': passengers
    }

    return models.Booking(data)


@helpers.with_connection
async def get_bookings(email, phone, *args, **kwargs):
    conn = kwargs.pop('connection')

    rows = await conn.fetch(
        "select * from booking b inner join offer_details od on b.offer_details_id=od.offer_details_id where b.email=$1 and b.phone=$2;",
        email, phone)
    print()
    bookings = []
    for row in rows:
        passengers_data = await conn.fetch(
            """select * from passenger p inner join booking b on p.passenger_id=b.passenger_id where b.offer_id=$1;""",
            row.get('offer_id'))
        passengers = []
        for p in passengers_data:
            passengers.append({
                'gender': p.get('gender'),
                'ticket_type': p.get('ticket_type'),
                'first_name': p.get('first_name'),
                'last_name': p.get('last_name'),
                'date_of_birth': p.get('date_of_birth'),
                'citizenship': p.get('citizenship'),
                'document': {
                    'number': p.get('numbers'),
                    'iin': p.get('iin'),
                    'expires_at': p.get('expires_at')
                }
            })

        bookings.append(models.Booking({
            'id': row.get('offer_id'),
            'phone': row.get('phone'),
            'email': row.get('email'),
            'offer': json.loads(row.get('details')),
            'passengers': passengers
        }))

        return bookings
