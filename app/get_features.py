def get_features() -> dict:
    return {
        "age": {"type": "number", "min_value": 0, "max_value": 200, "help": "Insert your age."},
        "workclass": {"type": "select", "options": ["Private", "Local-gov"], "help": "Select your workclass."},
        "fnlwgt": {"type": "number", "min_value": 1, "max_value": 10000000, "help": "Insert your fnlwgt."},
        "education": {"type": "select", "options": ["HS-grad", "Some-college"], "help": "Select your education."},
        "educational_num": {"type": "number", "min_value": 1, "max_value": 16,
                            "help": "Insert your educational-num."},
        "marital_status": {"type": "select", "options": ["Married-civ-spouse", "Divorced"],
                           "help": "Select your marital status."},
        "occupation": {"type": "select", "options": ["Exec-managerial", "Craft-repair"],
                       "help": "Select your occupation."},
        "relationship": {"type": "select", "options": ["Husband", "Wife"], "help": "Select your relationship."},
        # "race": {"type": "select", "options": ["Black", "White"], "help": "Select your race."},
        "gender": {"type": "select", "options": ["Male", "Female"], "help": "Select your gender."},
    }