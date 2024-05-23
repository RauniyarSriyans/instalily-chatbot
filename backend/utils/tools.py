tools = [
    {
        "type": "function",
        "function": {
            "name": "get_model_details",
            "description": "Get the model info and its parts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_number": {
                        "type": "string",
                        "description": "The model number to fetch the info about.",
                    },
                },
                "required": ["model_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_part_details",
            "description": "Get the details of a part.",
            "parameters": {
                "type": "object",
                "properties": {
                    "partselect_number": {
                        "type": "string",
                        "description": "The part select number to fetch the info about.",
                    },
                },
                "required": ["partselect_number"],
            },
        },
    },
]
