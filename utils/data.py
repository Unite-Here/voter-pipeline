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
    valid = any(in_val in validate_input for item in valid_input)
    return valid
