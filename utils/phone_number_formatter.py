def phone_number_formatter(number: str) -> str:
    formatted_number = number.strip()
    if formatted_number.startswith("0") and len(formatted_number) == 10:
        formatted_number = number.replace("0", "+254")
    return formatted_number
