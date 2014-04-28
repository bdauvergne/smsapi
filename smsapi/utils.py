class SMSError(Exception):
    pass

def is_int_phone_number(phone_number):
    if not phone_number.startswith('+'):
        return False
    if not phone_number[1:].isdigit():
        return False
    return True
