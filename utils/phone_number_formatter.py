def phone_number_formatter(number: str) -> str:
    formatted_number = number.strip()
    if formatted_number.startswith("0") and len(formatted_number) == 10:
        formatted_number = number.replace("0", "+254")
    return formatted_number


def format_phone_number(args):
    str_input = str(args)
    if str_input.startswith("254"):
        return str_input
    if len(str_input) == 10 and str_input.startswith("0"):
        return str_input.replace("0", "254")
