# TODO: Replace with pydantic model
def get_features() -> dict:
    """
    Is needed for creating the app-insert-layout. Depends on the dtype of a column (number or select).
    Number is for numeric columns and select is for categorical columns.

    :return: Expected features of the selected model
    :rtype: dict
    """
    return {
        "age": {
            "type": "number",
            "min_value": 16,
            "max_value": 91,
            "help": "How old are you? Accepted age: 16-91",
        },
        "workclass": {
            "type": "select",
            "options": [
                'Private',
                'Local-gov',
                'Self-emp-not-inc',
                'Federal-gov',
                'State-gov'
                'Self-emp-inc',
                'Without-pay',
                'Never-worked'
            ],
            "help": "Select your workclass to represent your employment status.",
        },
        "fnlwgt": {
            "type": "number",
            "min_value": 10000,
            "max_value": 1500000,
            "help": "Insert your final weight. In other words, the number of people the census believes the entry represents. 10.000-1.500.000",
        },
        "education": {
            "type": "select",
            "options": [
                '11th',
                'HS-grad',
                'Assoc-acdm',
                'Some-college',
                '10th',
                'Prof-school'
                '7th-8th',
                'Bachelors',
                'Masters',
                'Doctorate',
                '5th-6th',
                'Assoc-voc',
                '9th',
                '12th',
                '1st-4th',
                'Preschool'
            ],
            "help": "Select your highest education-level archieved.",
        },
        "educational_num": {
            "type": "number",
            "min_value": 1,
            "max_value": 16,
            "help": "The highest level of education achieved in numerical form. 1-16",
        },
        "marital_status": {
            "type": "select",
            "options": [
                'Never-married',
                'Married-civ-spouse',
                'Widowed',
                'Divorced',
                'Separated',
                'Married-spouse-absent',
                'Married-AF-spouse'
            ],
            "help": "Select your marital status.",
        },
        "occupation": {
            "type": "select",
            "options": [
                'Machine-op-inspct',
                'Farming-fishing',
                'Protective-serv',
                'Other-service',
                'Prof-specialty',
                'Craft-repair',
                'Adm-clerical',
                'Exec-managerial',
                'Tech-support',
                'Sales',
                'Priv-house-serv',
                'Transport-moving',
                'Handlers-cleaners',
                'Armed-Forces'
            ],
            "help": "Select your general type of occupation.",
        },
        "relationship": {
            "type": "select",
            "options": [
                'Own-child',
                'Husband',
                'Not-in-family',
                'Unmarried',
                'Wife',
                'Other-relative'
            ],
            "help": "Select your relationship.",
        },
        "race": {
            "type": "select",
            "options": [
                'Black',
                'White',
                'Asian-Pac-Islander',
                'Other',
                'Amer-Indian-Eskimo'
            ],
            "help": "Select your race.",
        },
        "gender": {
            "type": "select",
            "options": [
                "Male",
                "Female"
            ],
            "help": "Select your gender.",
        },
        "capital_gain": {
            "type": "number",
            "min_value": 0,
            "max_value": 100000,
            "help": "Insert your capital gain.0-100.000",
        },
        "capital_loss": {
            "type": "number",
            "min_value": 0,
            "max_value": 5000,
            "help": "Insert your capital loss. 0-5.000",
        },
        "hours_per_week": {
            "type": "number",
            "min_value": 1,
            "max_value": 65,
            "help": "Insert your hours per week you work at. 1-65",
        },
        "native_country": {
            "type": "select",
            "options": ['United-States',
                        'Peru',
                        'Guatemala',
                        'Mexico',
                        'Dominican-Republic',
                        'Ireland',
                        'Germany',
                        'Philippines',
                        'Thailand',
                        'Haiti',
                        'El-Salvador',
                        'Puerto-Rico',
                        'Vietnam',
                        'South',
                        'Columbia',
                        'Japan',
                        'India',
                        'Cambodia',
                        'Poland',
                        'Laos',
                        'England',
                        'Cuba',
                        'Taiwan',
                        'Italy',
                        'Canada',
                        'Portugal',
                        'China',
                        'Nicaragua',
                        'Honduras',
                        'Iran',
                        'Scotland',
                        'Jamaica',
                        'Ecuador',
                        'Yugoslavia',
                        'Hungary',
                        'Hong',
                        'Greece',
                        'Trinadad&Tobago',
                        'Outlying-US(Guam-USVI-etc)',
                        'France',
                        'Holand-Netherlands'
                        ],
            "help": "Insert your country of origin.",
        },
    }
