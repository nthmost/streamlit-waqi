# huge thanks to https://developer.mozilla.org/en-US/docs/Learn/CSS/Howto/create_fancy_boxes
CIRCLE_DIV = "text-align: center; margin: 1em; padding: 1.5em; border: 0.5em solid black; width: {size}em; height: {size}em; border-radius: 100%; background-color: {color};"

SENSOR_DIV_TEMPLATE = '<div style="%s"><h2>{reading}</h2></div>' % CIRCLE_DIV

GREEN = "#16e031"
YELLOW = "#e0de3a"
ORANGE = "#d49528"
RED = "#e33c22"
PURPLE = "#6c2b8f"

def sensor_div(reading, circle_size=8):
    if reading < 50:
        # good
        return SENSOR_DIV_TEMPLATE.format(color=GREEN, reading=reading, size=circle_size)
    elif (reading >= 50) and (reading < 100):
        # moderate
        return SENSOR_DIV_TEMPLATE.format(color=YELLOW, reading=reading, size=circle_size)
    elif (reading >= 100) and (reading < 150):
        # bad
        return SENSOR_DIV_TEMPLATE.format(color=ORANGE, reading=reading, size=circle_size)
    elif (reading >= 150) and (reading < 200):
        # real bad
        return SENSOR_DIV_TEMPLATE.format(color=RED, reading=reading, size=circle_size)
    elif (reading >= 200) and (reading < 250):
        # real real bad
        return SENSOR_DIV_TEMPLATE.format(color=PURPLE, reading=reading, size=circle_size)
    elif (reading >= 250) and (reading < 300):
        # yikes
        return SENSOR_DIV_TEMPLATE.format(color=PURPLE, reading=reading, size=circle_size)
    else:
        # nightmarish hellscape
        return SENSOR_DIV_TEMPLATE.format(color=PURPLE, reading=reading, size=circle_size)


