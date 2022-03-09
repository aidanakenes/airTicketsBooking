import pytest

from code import db


@pytest.mark.asyncio
async def test_create_booking(pool_database, booking_obj):
    uid = await db.create_booking(pool_database, booking_obj)

    assert booking_obj.booking_id == str(uid)


@pytest.mark.asyncio
async def test_get_booking(pool_database, booking_id):
    booking_result = await db.get_booking(pool_database, booking_id)

    assert booking_result.booking_id
    assert booking_result.email
    assert booking_result.phone


@pytest.mark.asyncio
async def test_get_bookings(pool_database, filters):
    booking_results = await db.get_bookings(pool_database, filters.get('email'), filters.get('phone'))

    for booking in booking_results:
        assert booking.email == filters.get('email')
        assert booking.phone == filters.get('phone')

