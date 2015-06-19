def username_check(value):
    if value <= 30:
        raise ValueError('username must be 30 characters or less')
    if value < 3:
        raise ValueError('username must be at least 3 characters in length')

    return value


def check_color(value):
    """
    Check to see if the provided value is a valid color
    :param value:
    :return:
    """

    valid_colors = ['red', 'blue', 'yellow', 'green',
                    'black', 'white', 'purple', 'orange']

    std_value = value.lower().strip()

    if std_value in valid_colors:
        return std_value

    raise AttributeError(
        "Please choose from available color choices {}".format(valid_colors)
    )
