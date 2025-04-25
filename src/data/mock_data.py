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
    }
}

# Mock agreement data
AGREEMENT_DATA = {
    "Bergen Shipping Company": {
        "id": "231454-01-R1",
        "name": "Third Party Vessels",
        "validity": {
            "start_date": "2025-06-03",
            "end_date": "2026-06-03"
        },
        "products": ["H&M", "HULL INT", "LOH", "WAR", "WAR TLO", "WAR LOH"],
        "our_share": "100%",
        "installments": 4,
        "conditions": "Nordic Plan"
    },
    "Global Maritime Ltd": {
        "id": "231455-02-R2",
        "name": "Fleet Coverage",
        "validity": {
            "start_date": "2025-07-15",
            "end_date": "2026-07-15"
        },
        "products": ["H&M", "HULL INT", "LOH"],
        "our_share": "75%",
        "installments": 2,
        "conditions": "Nordic Plan"
    },
    "SeaWay Carriers": {
        "id": "231456-03-R3",
        "name": "Cargo Vessels",
        "validity": {
            "start_date": "2025-08-22",
            "end_date": "2026-08-22"
        },
        "products": ["H&M", "WAR", "WAR TLO"],
        "our_share": "50%",
        "installments": 3,
        "conditions": "Nordic Plan"
    }
}

# Mock premium data
PREMIUM_DATA = {
    "Bergen Shipping Company": {
        "gross_premium": 1838274,
        "brokerage_percent": 15,
        "net_premium": 1598499
    },
    "Global Maritime Ltd": {
        "gross_premium": 1250000,
        "brokerage_percent": 12,
        "net_premium": 1100000
    },
    "SeaWay Carriers": {
        "gross_premium": 2100000,
        "brokerage_percent": 18,
        "net_premium": 1722000
    }
}

# Mock accounting data
ACCOUNTING_DATA = {
    "Bergen Shipping Company": {
        "paid": 2097922,
        "amount_due": 293784,
        "remaining": 486378,
        "balance_percent": 62
    },
    "Global Maritime Ltd": {
        "paid": 750000,
        "amount_due": 150000,
        "remaining": 350000,
        "balance_percent": 60
    },
    "SeaWay Carriers": {
        "paid": 1200000,
        "amount_due": 300000,
        "remaining": 600000,
        "balance_percent": 57
    }
}

# Mock loss ratio data
LOSS_RATIO_DATA = {
    "Bergen Shipping Company": {
        "value_percent": 0,
        "claims": None,
        "premium": None
    },
    "Global Maritime Ltd": {
        "value_percent": 25,
        "claims": 275000,
        "premium": 1100000
    },
    "SeaWay Carriers": {
        "value_percent": 57,
        "claims": 980000,
        "premium": 1722000
    }
}

# Mock risk data
RISK_DATA = {
    "Bergen Shipping Company": {
        "values_by_id": {
            "04": 4,  # Technical condition
            "08": 3,  # Operational quality
            "12": 4,  # Crew quality
            "14": 5,  # Management quality
            "16": 6,  # Claims history
            "18": 7   # Financial stability
        }
    },
    "Global Maritime Ltd": {
        "values_by_id": {
            "04": 2,
            "08": 2,
            "12": 3,
            "14": 3,
            "16": 4,
            "18": 3
        }
    },
    "SeaWay Carriers": {
        "values_by_id": {
            "04": 6,
            "08": 5,
            "12": 7,
            "14": 6,
            "16": 8,
            "18": 5
        }
    }
}

# Mock reinsurance data
REINSURANCE_DATA = {
    "Bergen Shipping Company": {
        "net_tty": 17995,
        "net_fac": None,
        "net_retention": 1580504,
        "commission": None
    },
    "Global Maritime Ltd": {
        "net_tty": 12500,
        "net_fac": 55000,
        "net_retention": 1032500,
        "commission": 5.5
    },
    "SeaWay Carriers": {
        "net_tty": 21000,
        "net_fac": 86100,
        "net_retention": 1614900,
        "commission": 4.2
    }
}

# Mock objects data
OBJECTS_DATA = {
    "Bergen Shipping Company": [
        "Mercosul Line Navegação e Logística LTDA.",
        "Brown Water"
    ],
    "Global Maritime Ltd": [
        "Atlantic Voyager",
        "Pacific Explorer",
        "Nordic Trader"
    ],
    "SeaWay Carriers": [
        "Cargo Express",
        "Bulk Carrier I",
        "Bulk Carrier II",
        "Container Ship Alpha"
    ]
}

# Mock contacts data
CONTACTS_DATA = {
    "Bergen Shipping Company": [
        {
            "name": "John Smith",
            "role": "Claims Handler",
            "email": "john.smith@norclub.com",
            "phone": "+47 998 87 766"
        },
        {
            "name": "Emma Johnson",
            "role": "Account Manager",
            "email": "emma.johnson@norclub.com",
            "phone": "+47 998 12 345"
        },
        {
            "name": "Michael Brown",
            "role": "Risk Assessor",
            "email": "michael.brown@norclub.com",
            "phone": "+47 998 45 678"
        }
    ],
    "Global Maritime Ltd": [
        {
            "name": "Sarah Wilson",
            "role": "Claims Handler",
            "email": "sarah.wilson@norclub.com",
            "phone": "+47 998 23 456"
        },
        {
            "name": "David Lee",
            "role": "Account Manager",
            "email": "david.lee@norclub.com",
            "phone": "+47 998 34 567"
        }
    ],
    "SeaWay Carriers": [
        {
            "name": "Robert Taylor",
            "role": "Claims Handler",
            "email": "robert.taylor@norclub.com",
            "phone": "+47 998 56 789"
        },
        {
            "name": "Jennifer Davis",
            "role": "Risk Assessor",
            "email": "jennifer.davis@norclub.com",
            "phone": "+47 998 67 890"
        }
    ]
}