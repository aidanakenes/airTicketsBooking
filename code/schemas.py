SEARCH_SCHEMA = {
    'type': 'object',
    'properties': {
        'provider': {
            'type': 'string'
        },
        'cabin': {
            'type': 'string'
        },
        'origin': {
            'type': 'string'
        },
        'destination': {
            'type': 'string'
        },
        'dep_at': {
            'type': 'string'
        },
        'arr_at': {
            'type': 'string'
        },
        'adults': {
            'type': 'integer'
        },
        'children': {
            'type': 'integer'
        },
        'infants': {
            'type': 'integer'
        },
        'currency': {
            'type': 'string'
        },
    },
    'required': {
        'provider',
        'cabin',
        'origin',
        'destination',
        'dep_at',
        'adults',
        'currency',
    }
}

BOOKING_DETAILS_SCHEMA = {
    'type': 'object',
    'properties': {
        'offer_id': {
            'type': 'uuint'
        },
        'phone': {
            'type': 'string'
        },
        'email': {
            'type': 'string'
        },
        'passengers': {
            'type': 'object',
            'properties': {
                'gender': {
                    'type': 'string'
                },
                'type': {
                    'type': 'string'
                },
                'first_name': {
                    'type': 'string'
                },
                'last_name': {
                    'type': 'string'
                },
                'date_of_birth': {
                    'type': 'string'
                },
                'citizenship': {
                    'type': 'string'
                },
                'document': {
                    'type': 'object',
                    'properties': {
                        'number': {
                            'type': 'string'
                        },
                        'expires_at': {
                            'type': 'string'
                        },
                        'iin': {
                            'type': 'string'
                        }
                    },
                    'required': {
                        'number',
                        'expires_at',
                        'iin'
                    }
                }
            },
            'required': {
                'gender',
                'type',
                'first_name',
                'last_name',
                'date_of_birth',
                'citizenship',
                'document'
            }

        },
    },
    'required': {
        'offer_id',
        'phone',
        'email',
        'passengers'
    }
}
