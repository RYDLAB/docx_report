{
    "name": "Report monetary helpers",
    "summary": """""",
    "description": """
        Adds in report's rendering context 2 methods for printing amount in words.
        They are accessible from template like this:

        number2words(amount_variable, lang="en", to="cardinal")
        currency2words(amount_variable, lang="en", to="cardinal", currency="RUB")

        "amount_variable" should be of "int", "float" or validate "string" type.

        Variants for "to" attribute:
            'cardinal', 'ordinal', 'ordinal_num', 'year', 'currency'.
            "cardinal" is default value.

        "lang" attribute. 25 languages are supported:
            'ar', 'en', 'en_IN', 'fr', 'fr_CH', 'fr_DZ', 'de', 'es', 'es_CO', 'es_VE',
            'id', 'lt', 'lv', 'pl', 'ru', 'sl', 'no', 'dk', 'pt_BR', 'he', 'it',
            'vi_VN', 'tr', 'nl', 'uk'.
            "ru" is default value.

        "currency" attribute: for russian language there are "RUB" and "EUR" currencies.
            "RUB" is default value.
            Full info about currencies features see in "num2words" python module.
    """,
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Technical",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "external_dependencies": {"python": ["num2words"]},
    "data": [],
}
