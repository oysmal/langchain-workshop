# Mock vessel history data
VESSEL_HISTORY = {
    "9123456": {
        "incidents": [
            {"date": "2022-05-15", "description": "Minor collision with dock", "severity": "Low"},
            {"date": "2020-11-03", "description": "Engine failure", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2022-05-16", "amount": 25000, "status": "Paid", "description": "Repairs for dock collision"},
            {"date": "2020-11-10", "amount": 75000, "status": "Paid", "description": "Engine replacement"}
        ]
    },
    "9234567": {
        "incidents": [],
        "claims": []
    },
    "9345678": {
        "incidents": [
            {"date": "2023-01-20", "description": "Fire in cargo hold", "severity": "High"},
            {"date": "2021-07-12", "description": "Piracy attempt", "severity": "High"},
            {"date": "2019-03-30", "description": "Navigation equipment failure", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2023-01-25", "amount": 500000, "status": "Paid", "description": "Fire damage repairs"},
            {"date": "2021-07-15", "amount": 150000, "status": "Paid", "description": "Security upgrades after piracy attempt"},
            {"date": "2019-04-05", "amount": 50000, "status": "Paid", "description": "Navigation equipment replacement"}
        ]
    },
    # GB Shipping Vessels from Excel files
    "9700001": {  # GB Pathfinder
        "incidents": [
            {"date": "2020-08-05", "description": "North Sea main-engine damage", "severity": "High"}
        ],
        "claims": [
            {"date": "2020-08-05", "amount": 5500000, "status": "Paid", "description": "North Sea main-engine damage repairs"}
        ]
    },
    "9700002": {  # GB Horizon
        "incidents": [
            {"date": "2020-12-12", "description": "Grounding at River Humber", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2020-12-12", "amount": 4700000, "status": "Paid", "description": "Grounding at River Humber repairs"},
            {"date": "2020-12-12", "amount": 380000, "status": "Paid", "description": "Loss of hire due to grounding"}
        ]
    },
    "9700003": {  # GB Explorer
        "incidents": [
            {"date": "2021-04-11", "description": "Cargo-hold flooding", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2021-04-11", "amount": 3300000, "status": "Pending", "description": "Cargo-hold flooding repairs"},
            {"date": "2021-04-11", "amount": 575000, "status": "Pending", "description": "Loss of hire due to cargo-hold flooding"}
        ]
    },
    "9700004": {  # GB Atlas
        "incidents": [
            {"date": "2021-02-18", "description": "Crane failure at Immingham", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2021-02-18", "amount": 2500000, "status": "Paid", "description": "Crane failure repairs"}
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
    },
    "Global Maritime Ltd": {
        "incidents": [],
        "claims": []
    },
    "SeaWay Carriers": {
        "incidents": [
            {"date": "2022-12-05", "description": "Cargo damage due to improper stowage", "severity": "Medium"},
            {"date": "2022-02-18", "description": "Delay due to mechanical issues", "severity": "Low"},
            {"date": "2020-06-30", "description": "Collision with another vessel", "severity": "High"}
        ],
        "claims": [
            {"date": "2022-12-10", "amount": 200000, "status": "Paid", "description": "Compensation for damaged cargo"},
            {"date": "2022-02-20", "amount": 30000, "status": "Paid", "description": "Penalty for delay"},
            {"date": "2020-07-05", "amount": 750000, "status": "Paid", "description": "Repairs and liability for collision"}
        ]
    },
    "GB Shipping": {
        "incidents": [
            {"date": "2020-08-05", "description": "Vessel Pathfinder main-engine damage", "severity": "High"},
            {"date": "2020-12-12", "description": "Vessel Horizon grounding at River Humber", "severity": "Medium"},
            {"date": "2021-02-18", "description": "Vessel Atlas crane failure", "severity": "Medium"},
            {"date": "2021-04-11", "description": "Vessel Explorer cargo-hold flooding", "severity": "Medium"}
        ],
        "claims": [
            {"date": "2020-08-05", "amount": 5500000, "status": "Paid", "description": "Vessel Pathfinder repairs"},
            {"date": "2020-12-12", "amount": 4700000, "status": "Paid", "description": "Vessel Horizon repairs"},
            {"date": "2020-12-12", "amount": 380000, "status": "Paid", "description": "Vessel Horizon loss of hire"},
            {"date": "2021-02-18", "amount": 2500000, "status": "Paid", "description": "Vessel Atlas repairs"},
            {"date": "2021-04-11", "amount": 3300000, "status": "Pending", "description": "Vessel Explorer repairs"},
            {"date": "2021-04-11", "amount": 575000, "status": "Pending", "description": "Vessel Explorer loss of hire"}
        ]
    }
}
