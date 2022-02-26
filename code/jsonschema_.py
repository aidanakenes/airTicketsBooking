import jsonschema
from helpers import errors


async def validate(request, schema):
    try:
        jsonschema.validate(
            request.json,
            schema=schema,
        )
    except Exception as e:
        raise errors.InvalidParams()
