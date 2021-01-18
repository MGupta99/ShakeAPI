schema = {
    "/apple/register": {
        "type": "object",
        "properties": {
            "user": {"type": "object"},
            "authorizationCode": {"type": "string"},
            "identityToken": {"type": "string"}
        },
        "required": ["user", "authorizationCode", "identityToken"]
    },

    "/apple/login": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "authorizationCode": {"type": "string"},
            "identityToken": {"type": "string"}
        },
        "required": ["id", "authorizationCode", "identityToken"]
    },

    "/password/otp/send": {
        "type": "object",
        "properties": {
            "phoneNumber": {"type": "string"}
        },
        "required": ["phoneNumber"]
    },

    "/password/register": {
        "type": "object",
        "properties": {
            "phoneNumber": {"type": "string"},
            "email": {"type": "string"},
            "code": {"type": "string"},
            "name": {"type": "object"},
            "password": {"type": "string"}
        },
        "required": ["phoneNumber", "email", "code", "name", "password"]
    },

    "/password/login": {
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "password": {"type": "string"}
        },
        "required": ["email", "password"]
    }
}
