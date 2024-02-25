import mariadb

from operations import db
from operations.informationProcessing.helpers import validate_float_field, prompt_and_validate_string, \
    prompt_and_validate_date, prompt_and_validate_custom, validate_phone_field


def create_user_helper(email: str, first_name: str, last_name: str, subscription_fee: float, subscription_status: str,
                       phone: str, registration_date: str):
    """
    Helper function that takes parameters that are necessary to build SQL query and execute to create a new user
    :param email: email of user
    :param first_name: first name of user
    :param last_name: last name of user
    :param subscription_fee: subscription fee of user
    :param subscription_status: subscription status of user
    :param phone: phone number of user
    :param registration_date: registration date of user
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO User (email, firstName, lastName, subscriptionFee, "
                    f"statusOfSubscription, phone, registrationDate)"
                    f"Values('{email}', '{first_name}', '{last_name}', {subscription_fee},"
                    f"'{subscription_status}', {phone}, '{registration_date}')")
        conn.commit()

        print(f"User, {first_name} {last_name}, was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_user():
    """
    Function that prompts user for inputs necessary to create a new user
    """
    try:
        email = input("Enter email address: ")

        first_name = input("Enter first name: ")

        last_name = input("Enter last name: ")

        subscription_fee = input("Enter subscription fee: ")
        if validate_float_field(subscription_fee) is False:
            raise Exception("Not a number!")
        subscription_fee = float(subscription_fee)

        subscription_status = input("Enter subscription status (A or I): ")
        if subscription_status != "A" and subscription_status != "I":
            raise Exception("A or I was not entered in!")

        phone = input("Enter digit phone number up to 16 digits: ")
        if len(phone) > 16:
            raise Exception("This phone number is too long")

        registration_date = input("Enter in registration date (format: 2020-01-01): ")

        create_user_helper(email, first_name, last_name, subscription_fee, subscription_status, phone,
                           registration_date)
    except:
        print("Oops, something went wrong!")


def update_user_helper(field_name: str, field_value: str, email: str):
    """
    Helper function that takes a field to be updated and user email in order to execute SQL query
    necessary to update an existing user
    :param field_name: a column of the user schema
    :param field_value: value associated with field_name
    :param email: email of the user
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"UPDATE User SET {field_name} = {field_value} "
                    f"WHERE email = '{email}'")

        conn.commit()

        print(f"User, '{email}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_user():
    """
    Function that prompts user for inputs necessary to update a user
    """
    try:
        email = input("Enter email address: ")

        field_name = ""
        field_value = None
        print("\n\nList of fields:")
        print("email = e")
        print("first name = fn")
        print("last name = ln")
        print("subscription fee = sf")
        print("subscription status = ss")
        print("phone = p")
        print("registration date = rd")

        prompt_field = input("Which of the user fields would you like to update? ")

        match prompt_field.lower():
            case "e":
                field_name, field_value = prompt_and_validate_string("email")
            case "fn":
                field_name, field_value = prompt_and_validate_string("firstName")
            case "ln":
                field_name, field_value = prompt_and_validate_string("lastName")
            case "sf":
                field_name, field_value = prompt_and_validate_custom("subscriptionFee",
                                                                     "\n\nEnter in subscription fee: ",
                                                                     validate_float_field)

            case "ss":
                def validate_subscription(given_value):
                    if given_value != "A" and given_value != "I":
                        raise Exception("A or I was not entered in!")

                field_name, field_value = prompt_and_validate_custom("statusOfSubscription",
                                                                     "\n\nEnter subscription status (A or I): ",
                                                                     validate_subscription)
            case "p":
                field_name, field_value = prompt_and_validate_custom("phone",
                                                                     "\n\nEnter digit phone number up to 16 digits: ",
                                                                     validate_phone_field)
            case "rd":
                field_name, field_value = prompt_and_validate_date("registrationDate")

        update_user_helper(field_name=field_name, field_value=field_value, email=email)

    except:
        print("Oops, something went wrong!")


def delete_user_helper(email: str):
    """
    Helper function that uses email to create/execute query to delete an existing user
    :param email: email of user
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM User WHERE email = '{email}'")

        conn.commit()

        print(f"User with email, '{email}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_user():
    """
    Function that prompts user email necessary to delete an existing user
    """
    email = input("Enter email address: ")

    delete_user_helper(email=email)
