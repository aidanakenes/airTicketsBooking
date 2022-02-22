from datetime import datetime
import json

from helpers.decorators import with_connection
import models


@with_connection
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


@with_connection
async def get_booking(booking_id, *args, **kwargs):
    conn = kwargs.pop('connection')

    booking_data = await _select_booking(conn, booking_id)

    booking_data.passengers = await _select_passengers(conn, booking_id)

    return booking_data


async def _select_booking(conn, booking_id):
    stmt = """SELECT b.offer_id, b.phone, b.email, od.details 
            FROM booking b
            INNER JOIN offer_details od ON b.offer_details_id=od.offer_details_id 
            WHERE offer_id=$1"""

    booking_records = await conn.fetchrow(stmt, booking_id)

    return models.Booking(booking_records)


async def _select_passengers(conn, booking_id):
    stmt = """SELECT p.gender, p.ticket_type, p.first_name, p.last_name, p.date_of_birth, 
            p.citizenship, p.numbers, p.expires_at, p.iin 
            FROM passenger p 
            INNER JOIN booking b ON p.passenger_id=b.passenger_id 
            WHERE b.offer_id=$1"""

    passenger_records = await conn.fetch(stmt, booking_id)

    passengers = []
    for p in passenger_records:
        passengers.append(models.Passenger(p))

    return passengers


@with_connection
async def get_bookings(email, phone, limit, *args, **kwargs):
    conn = kwargs.pop('connection')
    stmt = """SELECT * FROM booking b 
        INNER JOIN offer_details od ON b.offer_details_id=od.offer_details_id 
        WHERE b.email=$1 AND b.phone=$2 
        LIMIT $3;"""

    rows = await conn.fetch(stmt, email, phone, limit)

    bookings = []
    for row in rows:
        passengers = await _select_passengers(conn, row.get('offer_id'))

        bookings.append(models.Booking({
            'id': row.get('offer_id'),
            'phone': row.get('phone'),
            'email': row.get('email'),
            'offer': json.loads(row.get('details')),
            'passengers': passengers
        }))

        return bookings
