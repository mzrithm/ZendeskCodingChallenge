from datetime import datetime

"""Sample ticket dictionary for testing purposes."""

tickets = {
    0: {"requester_id": 23,
        "assignee_id": 26,
        "subject": "z is for zen",
        "description": "Discover the art of customer service maintenance with zendesk.",
        "tags": ["a", "giraffe", "rhino"],
        "API": datetime.now()
        },
    1: {"requester_id": 11,
        "assignee_id": 39,
        "subject": "a is for apple",
        "description": "Watch this fruit fall to discover the laws of gravity.",
        "tags": ["b", "giraffe", "hippo"],
        "API": datetime.now()
        },
    2: {"requester_id": 14,
        "assignee_id": 67,
        "subject": "m is for michelle",
        "description": "Stellar student looking for an internship for the summer of 2022.",
        "tags": ["c", "giraffe", "gazelle"],
        "API": datetime.now()
        }
}
