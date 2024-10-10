from datetime import datetime


def filter_lists(known: list, unknown: list) -> list:
    """
    Find items in unknown that are not in known
    """

    def fun(var):
        if var in known:
            return False
        else:
            return True

    difference = []
    filtered = filter(fun, unknown)
    for item in filtered:
        difference.append(item)

    return difference


def format_date_mdy_to_ymd(data: str) -> str:
    """
    Format date from mm/dd/yyyy to yyyy-mm-dd
    Only use with inputs of format mm/dd/yyyy and yyyy-mm-dd

    Parameters
    ----------
    data : string

    Returns
    -------
    string
        If input not mm/dd/yyyy then input is returned, assumed to already be yyyy-mm-dd
    """
    try:
        dt = datetime.strptime(data, "%m/%d/%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        return data


def validate_input(valid_input: list, in_val) -> bool:
    """
    See if value exists in list of valid input

    Parameters
    ----------
    valid_input : list
    in_val : any
    
    Returns
    -------
    bool
        If in_val matches an item in valid_input then returns True, else False
    """

    if in_val == None:
        return True
    else:
        valid = any(in_val in valid_input for item in valid_input)
        return valid
