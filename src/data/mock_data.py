# Updated mock vessel history data (including 2023-24 synthetic cases)
VESSEL_HISTORY = {
    "9123456": {  # MV Atlantic Voyager
        "incidents": [
            {"date": "2022-05-15", "description": "Minor collision with dock", "severity": "Low"},
            {"date": "2020-11-03", "description": "Engine failure", "severity": "Medium"},

            # — New 2023-24 incidents —
            {"date": "2023-11-15", "description": "Engine-room fire (25 days off-hire)", "severity": "High"},
            {"date": "2023-12-05", "description": "Bow collision with berthed vessel", "severity": "High"},
            {"date": "2024-03-18", "description": "Port-side crane impact while berthing", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2022-05-16", "amount":  25_000,   "status": "Paid",   "description": "Repairs for dock collision"},
            {"date": "2020-11-10", "amount":  75_000,   "status": "Paid",   "description": "Engine replacement"},

            # — New 2023-24 claims —
            {"date": "2023-11-25", "amount": 2_800_000, "status": "Paid",   "description": "Loss of hire due to fire"},
            {"date": "2023-12-20", "amount": 3_000_000, "status": "Open",   "description": "HM repairs for bow collision"},
            {"date": "2024-03-25", "amount": 1_100_000, "status": "Open",   "description": "HM repairs for crane impact"}
        ]
    },

    "9234567": {  # MV Pacific Explorer
        "incidents": [
            # — New 2023-24 incidents —
            {"date": "2024-01-08", "description": "Crane damage in heavy weather", "severity": "Medium"},
            {"date": "2024-05-20", "description": "Turbo-charger failure en route", "severity": "Medium"}
        ],
        "claims": [
            # — New 2023-24 claims —
            {"date": "2024-01-18", "amount": 1_300_000, "status": "Open", "description": "Loss of hire (14 days) – crane damage"},
            {"date": "2024-05-30", "amount":   950_000, "status": "Open", "description": "Loss of hire (12 days) – turbo-charger failure"}
        ]
    }
}

# Mock company history data
COMPANY_HISTORY = {
    "Bergen Shipping Company": {
        "incidents": [
            {"date": "2023-04-10", "description": "Environmental violation", "severity": "Medium"},
            {"date": "2021-09-22", "description": "Crew injury", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2023-04-15", "amount": 100000, "status": "Paid", "description": "Fine for environmental violation"},
            {"date": "2021-09-25", "amount": 50000, "status": "Paid", "description": "Medical expenses for injured crew"}
        ]
    }
}
