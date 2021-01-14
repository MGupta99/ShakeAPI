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
            "code": {"type": "string"},
            "name": {"type": "object"},
            "password": {"type": "string"}
        },
        "required": ["phoneNumber", "code", "name", "password"]
    },

    "/password/login": {
        "type": "object",
        "properties": {
            "phone": {"type": "string"},
            "password": {"type": "string"}
        },
        "required": ["password"]
    }
}
