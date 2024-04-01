from decimal import Decimal

from num2words import num2words
from num2words import CONVERTES_TYPES


# Can use params:
# ~ number: int, float or validate string
# ~ to: num2words.CONVERTES_TYPES
# ~ lang: num2words.CONVERTER_CLASSES
# ~ currency: num2words.CONVERTER_CLASSES.CURRENCY_FORMS


def num2words_(number, **kwargs):
    if _perform_convert(number):
        if "lang" not in kwargs:
            kwargs["lang"] = "ru"
        if "to" not in kwargs or kwargs["to"] not in CONVERTES_TYPES:
            kwargs["to"] = "cardinal"
        return num2words(number, **kwargs)


def num2words_currency(number, **kwargs):
    if _perform_convert(number):
        if "lang" not in kwargs:
            kwargs["lang"] = "ru"
        if "to" not in kwargs or kwargs["to"] not in CONVERTES_TYPES:
            kwargs["to"] = "currency"
        if "currency" not in kwargs:
            kwargs["currency"] = "RUB"
        result = num2words(number, **kwargs)
        total = result.split(",")[0]
        part_word = result.split()[-1]
        part_number = Decimal(str(number)) % 1
        return "{total}, {part_n} {part_w}".format(
            total=total.capitalize(),
            part_n="{:02d}".format(int(part_number * 100)),
            part_w=part_word,
        )


def _perform_convert(number):
    if isinstance(number, int) or isinstance(number, float):
        return True
    if isinstance(number, str):
        try:
            number = float(number)
            return True
        except ValueError:
            return False
    return False
