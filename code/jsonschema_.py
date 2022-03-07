import jsonschema
from code.helpers import errors


async def validate(request_data, schema):
    try:
        jsonschema.validate(
            request_data,
            schema=schema,
        )
    except Exception as e:
        raise errors.InvalidParams()
