from datetime import datetime
import json

from helpers.decorators import with_connection
import models


@with_connection
async def create_booking(booking, *args, **kwargs):
    conn = kwargs.pop('connection')
    booking_id = -1

    for passenger in booking.passengers:
        passenger_id = await _insert_passenger(conn, passenger)
        offer_details_id = await _insert_offer(conn, booking)
        booking_id = await _insert_booking(conn, booking, passenger_id, offer_details_id)

    return booking_id


async def _insert_passenger(conn, passenger):
    stmt = """INSERT INTO passenger (info)
            VALUES ($1) RETURNING passenger_id;"""

    uid = await conn.fetchval(stmt, json.dumps(passenger))

    return uid


async def _insert_offer(conn, booking):
    stmt = """INSERT INTO offer_details (details)
            VALUES ($1) RETURNING offer_details_id;"""

    uid = await conn.fetchval(stmt, json.dumps(booking.offer))

    return uid


async def _insert_booking(conn, booking, passenger_id, offer_details_id):
    stmt = """INSERT INTO booking (booking_id, phone, email, offer_details_id, passenger_id)
            VALUES ($1, $2, $3, $4, $5) RETURNING booking_id;"""

    uid = await conn.execute(stmt, booking.booking_id, booking.phone, booking.email,
                             offer_details_id, passenger_id)

    return uid


@with_connection
async def get_booking(booking_id, *args, **kwargs):
    conn = kwargs.pop('connection')

    booking_data = await _select_booking(conn, booking_id)

    return booking_data


async def _select_booking(conn, booking_id):
    stmt = """SELECT b.booking_id, b.phone, b.email, od.details, p.info 
            FROM booking b
            INNER JOIN offer_details od ON b.offer_details_id=od.offer_details_id 
            INNER JOIN passenger p ON b.passenger_id=p.passenger_id 
            WHERE b.booking_id=$1"""

    booking_records = await conn.fetchrow(stmt, booking_id)

    return models.Booking(booking_records)


@with_connection
async def get_bookings(email, phone, *args, **kwargs):
    conn = kwargs.pop('connection')
    stmt = """SELECT b.offer_id, b.phone, b.email, od.details, p.info 
            FROM booking b 
            INNER JOIN offer_details od ON b.offer_details_id=od.offer_details_id 
            INNER JOIN passenger p ON b.passenger_id=p.passenger_id 
            WHERE b.email=$1 AND b.phone=$2;"""

    rows = await conn.fetch(stmt, email, phone)

    bookings = []
    for row in rows:
        bookings.append(models.Booking(row))

    return bookings
