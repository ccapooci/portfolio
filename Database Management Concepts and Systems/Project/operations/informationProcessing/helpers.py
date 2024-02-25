from typing import Callable


def validate_number_field(field):
    """ Function that checks if a field is a number. Throws an exception if not
    """
    if field.isnumeric() is False:
        raise Exception("Not a number!")


def validate_float_field(num):
    """ Function that checks if a field is a float. Throws an exception if not
    """
    try:
        float(num)
    except ValueError:
        raise Exception("Not a float!")


def validate_phone_field(given_field: str):
    """ Function that checks if a field is within 16 characters long. Throws an exception if greater
    """
    if len(given_field) > 16:
        raise Exception("This phone number is too long")


def prompt_and_validate_string(field_name: str) -> (str, str):
    """ Function that prompts user for a value and returns the field name and field value as a tuple
    """
    field_value = input(f"\n\nWhat is the new value for {field_name}?: ")
    return field_name, f"'{field_value}'"


def prompt_and_validate_date(field_name: str) -> (str, str):
    """ Function that prompts user for a date value and returns the field name and field value as a tuple
    """
    field_value = input(f"Enter in {field_name} (format: 2020-01-01): ")
    return field_name, f"'{field_value}'"


def prompt_and_validate_custom(field_name: str, question: str, validator: Callable[[str], None]) -> (str, str):
    """ Generic function that prompts user for a value and returns the field name and field value as a tuple
    with custom logic checking via validator callback function
    """
    field_value = input(question)
    validator(field_value)
    return field_name, f"'{field_value}'"
