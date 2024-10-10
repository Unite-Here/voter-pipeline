import pytest

from lib.utils.data import filter_lists, format_date_mdy_to_ymd, validate_input


# Test filter_lists returns difference
def test_filter_lists():
    # Fake variables
    fake_known = [{"fruit": "apricot"}, {"fruit": "blueberry"}, {"fruit": "cranberry"}]
    fake_unknown = [{"fruit": "apricot"}, {"fruit": "blueberry"}, {"fruit": "cranberry"}, {"fruit": "durian"}]

    # Call filter_lists
    response = filter_lists(fake_known, fake_unknown)

    expected = [{"fruit": "durian"}]

    assert response == expected

# Test validate_input returns true if input is None
def test_validate_input_none():
    # Fake variables
    fake_input = None
    fake_valid_list = ["Orange", "Lime", "Lemon", "Grapefruit"]

    # Call validate_input
    response = validate_input(fake_valid_list, fake_input)

    # Assert input is valid
    assert response == True


# Test validate_input returns true
def test_validate_input_valid():
    # Fake variables
    fake_input = "Lime"
    fake_valid_list = ["Orange", "Lime", "Lemon", "Grapefruit"]

    # Call validate_input
    response = validate_input(fake_valid_list, fake_input)

    # Assert input is valid
    assert response == True


# Test validate_input returns not valid
def test_validate_input_not_valid():
    # Fake variables
    fake_input = "Coconut"
    fake_valid_list = ["Orange", "Lime", "Lemon", "Grapefruit"]

    # Call validate_input
    response = validate_input(fake_valid_list, fake_input)

    # Assert input is not valid
    assert response == False


# Test format_date_mdy_to_ymd returns yyyy-mm-dd
def test_format_date_mdy_to_ymd_success():
    # Fake variables
    fake_input = "01/01/2000"
    
    # Expected result
    expected = "2000-01-01"

    # Call format_date_mdy_to_ymd
    result = format_date_mdy_to_ymd(fake_input)

    # Assert result is correct
    assert result == expected


# Test format_date_mdy_to_ymd returns input on exception
def test_format_date_mdy_to_ymd_fail():
    # Fake variables
    fake_input = "2000.01.01"

    # Call format_date_mdy_to_ymd
    result = format_date_mdy_to_ymd(fake_input)

    # Assert result equals input
    assert result == fake_input
