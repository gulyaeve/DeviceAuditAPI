import re


def validate_to_reference(value, reference: str):
    if reference == "Да":
        if value.lower() == "да":
            result = True
        else:
            result = False
    elif reference.startswith(">="):
        if int(value) >= int(re.findall(r'\d+', reference)[0]):
            result = True
        else:
            result = False
    elif reference.startswith(">"):
        if int(value) > int(re.findall(r'\d+', reference)[0]):
            result = True
        else:
            result = False
    elif reference.startswith("<="):
        if int(value) <= int(re.findall(r'\d+', reference)[0]):
            result = True
        else:
            result = False
    elif reference.startswith("<"):
        if int(value) < int(re.findall(r'\d+', reference)[0]):
            result = True
        else:
            result = False
    elif len(re.findall(r'\d+', reference)) == 2:
        if int(re.findall(r'\d+', reference)[0]) <= int(value) <= int(re.findall(r'\d+', reference)[1]):
            result = True
        else:
            result = False
    else:
        result = None
    return result

