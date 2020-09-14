SENSOR_DIV_TEMPLATE = '<div style="%s"><h1>%i</h1></div>'

# huge thanks to https://developer.mozilla.org/en-US/docs/Learn/CSS/Howto/create_fancy_boxes
CIRCLE_DIV = "text-align: center; padding: 1.5em; border: 0.5em solid black; width: 10em; height: 10em; border-radius: 100%;"

GREEN_CIRCLE = CIRCLE_DIV + "background-color: #16e031"
YELLOW_CIRCLE = CIRCLE_DIV + "background-color: #e0de3a"
ORANGE_CIRCLE = CIRCLE_DIV + "background-color: #d49528"
RED_CIRCLE = CIRCLE_DIV + "background-color: #e33c22"
PURPLE_CIRCLE = CIRCLE_DIV + "background-color: #6c2b8f"

def sensor_div(reading):
    if reading < 50:
        # good
        return SENSOR_DIV_TEMPLATE % (GREEN_CIRCLE, reading)
    elif (reading >= 50) and (reading < 100):
        # moderate
        return SENSOR_DIV_TEMPLATE % (YELLOW_CIRCLE, reading)
    elif (reading >= 100) and (reading < 150):
        # bad
        return SENSOR_DIV_TEMPLATE % (ORANGE_CIRCLE, reading)
    elif (reading >= 150) and (reading < 200):
        # real bad
        return SENSOR_DIV_TEMPLATE % (RED_CIRCLE, reading)
    elif (reading >= 200) and (reading < 250):
        # real real bad
        return SENSOR_DIV_TEMPLATE % (PURPLE_CIRCLE, reading)
    elif (reading >= 250) and (reading < 300):
        # yikes
        return SENSOR_DIV_TEMPLATE % (PURPLE_CIRCLE, reading)
    else:
        # nightmarish hellscape
        return SENSOR_DIV_TEMPLATE % (PURPLE_CIRCLE, reading)


