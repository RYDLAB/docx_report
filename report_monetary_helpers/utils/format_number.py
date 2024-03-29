from math import modf

from odoo.exceptions import ValidationError


def _validate_number_arg(number: int or float or str) -> int or float:
    """
    Raise ValidationError if number have wrong type or string is not a valid number.
    Returns int or float.
    """
    if type(number) == str:
        check_comma = number.split(",")
        check_dot = number.split(".")
        if len(check_comma) in (1, 2) and all([part.isdigit() for part in check_comma]):
            return float(".".join(check_comma))
        elif len(check_dot) in (1, 2) and all([part.isdigit() for part in check_dot]):
            return float(number)
        else:
            raise ValidationError(
                f"'format_number' method got an argument of string type which is not valid number: {number}"
            )
    if type(number) in (int, float):
        return number
    raise ValidationError(
        f"'format_number' method got an argument of wrong type '{type(number)}'"
    )


def format_number(
    number: int or float or str,
    r_acc: int = 2,
    dec_sep: str = ",",
    div_by_3: bool = True,
) -> str:
    """
    Formats float and int values representation. Returns string.

    :param r_acc: int, Round accuracy, default is 2.
    :param dec_sep: str, separator between integer and fractional parts
    :param div_by_3: bool, inserts space after each 3 digits in integer part.
    }
    """
    valid_number = _validate_number_arg(number)
    fract_part, int_part = modf(valid_number)
    new_fract_part = str(round(fract_part, r_acc))[2:].ljust(r_acc, "0")
    if div_by_3:
        # convert to str, cut off ".0" and reverse
        int_part = str(int_part)[:-2][::-1]
        counter_3 = 0
        new_int_part = ""
        for num in int_part:
            if counter_3 < 3:
                divider = ""
            else:
                divider = " "
                counter_3 = 0
            new_int_part = divider.join([new_int_part, num])
            counter_3 += 1
        # Reverse backward
        new_int_part = new_int_part[::-1]
    else:
        new_int_part = str(int_part)[:-2]
    return dec_sep.join([new_int_part, new_fract_part])
