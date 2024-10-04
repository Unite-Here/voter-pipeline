from utils.data import validate_input


# Test validate_input returns valid
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
