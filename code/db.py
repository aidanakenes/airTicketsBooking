from datetime import datetime
import json

from helpers.decorators import with_connection
import models


@with_connection
async def create_booking(booking, *args, **kwargs):
    conn = kwargs.pop('connection')

    offer_details_id = await _insert_offer(conn, booking.offer)
    booking_id = await _insert_booking(conn, booking, offer_details_id)

    return booking_id


async def _insert_offer(conn, offer):
    stmt = """INSERT INTO offer_details (details)
            VALUES ($1) RETURNING offer_details_id;"""

    uid = await conn.fetchval(stmt, json.dumps(offer))

    return uid


async def _insert_booking(conn, booking, offer_details_id):
    stmt = """INSERT INTO booking (booking_id, phone, email, created_at, passengers, offer_details_id)
            VALUES ($1, $2, $3, $4, $5, $6) RETURNING booking_id;"""

    uid = await conn.execute(stmt, booking.booking_id, booking.phone, booking.email, datetime.now(),
                             json.dumps(booking.passengers), offer_details_id)

    return uid


@with_connection
async def get_booking(booking_id, *args, **kwargs):
    conn = kwargs.pop('connection')

    booking_data = await _select_booking(conn, booking_id)

    return booking_data


async def _select_booking(conn, booking_id):
    stmt = """SELECT b.booking_id, b.phone, b.email, od.details, b.passengers 
            FROM booking b
            INNER JOIN offer_details od ON b.offer_details_id=od.offer_details_id 
            WHERE b.booking_id=$1"""

    booking_records = await conn.fetchrow(stmt, booking_id)

    return models.Booking(booking_records)


@with_connection
async def get_bookings(email, phone, *args, **kwargs):
    conn = kwargs.pop('connection')
    stmt = """SELECT b.offer_id, b.phone, b.email, od.details, b.passengers 
            FROM booking b 
            INNER JOIN offer_details od ON b.offer_details_id=od.offer_details_id 
            WHERE b.email=$1 AND b.phone=$2;"""

    rows = await conn.fetch(stmt, email, phone)

    bookings = []
    for row in rows:
        bookings.append(models.Booking(row))

    return bookings
