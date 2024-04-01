# Report monetary helpers
Adds in report's rendering context 2 methods for printing amount in words and
        1 method for formatting numbers represetnation/
        They are accesible from template like this:

        number2words(amount_variable, lang="en", to="cardinal")
        currency2words(amount_variable, lang="en", to="cardinal", currency="RUB")
        format_number(amount_variable, r_acc=2, dec_sep=",", div_by_3=False)

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

        "r_acc" attribute: Round accuracy for amount_variable, type int. Default is 2.

        "dec_sep" attribute: Decimal separator symbol to set, type str. Default is ",".

        "div_by_3" attribute: Bool flag to divide number's integer part by 3 digits with whitespaces. 
            Default is True.
