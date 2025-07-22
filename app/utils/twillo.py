def extract_message(form):
    if not form or not form.get("Body"):
        return
    message = form.get("Body")
    return message


def extract_number(form):
    if not form or not form.get("From"):
        return
    number = form.get("From")
    return number
