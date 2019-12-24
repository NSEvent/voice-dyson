from flask import Flask
from flask_ask import Ask, statement, question, session, request
import json

def send_power():
    """Use LIRC to send swivel signal."""
    return

def send_swivel():
    """Use LIRC to send swivel signal."""
    return

def set_temp_mode(temp_mode):
    """Use LIRC to send hot/cold signal
        Expects temp_mode = 'hot'/'cold'."""
    # # TODO:

def set_power_level(power_level):
    """Use LIRC to adjust to 1-9 fan level
        Expects power_level >= 1 and power_level <= 9."""
    # # TODO:

def set_temp_level(temp_level):
    """Use LIRC to adjust to 60-90 fan temperature
        Expects temp_level >= 60 and temp_level <= 90."""
    # # TODO:

def get_slot_value(slot_name):
    """Return canonical slot value (entity resolution)."""

    slots = request['intent']['slots']
    value = None

    slot = slots[slot_name]
    if 'value' in slot:
        value = slot['value']
        # Use canonical value (entity resolution) if exists
        if 'resolutions' in slot and slot['resolutions']['resolutionsPerAuthority'][0]['status']['code'] == 'ER_SUCCESS_MATCH':
            value = slot['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']

    return value


# Set Alexa endpoint to ngrok.link/voice_dyson
# Select second option for endpoint:
# "My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority."
app = Flask(__name__)
ask = Ask(app, '/voice_dyson')
app.config["ASK_APPLICATION_ID"] = "amzn1.ask.skill.e033e61a-290c-46cf-b4cb-679d9ec858a4"

@app.route('/')
def homepage():
    return 'An Alexa skill for toggling Dyson fan settings'

@ask.launch
def start_skill():
    speech_text = "You can ask me to change your Dyson fan settings"
    return statement(speech_text)

@ask.intent('toggle_power')
def toggle_power():
    send_power()
    return statement('Okay, ending toggle power intent handling')

@ask.intent('toggle_swivvle')
def toggle_swivvle():
    send_swivel()
    return statement('Okay, ending toggle swivel intent handling')

@ask.intent('set_fan_settings')
def set_fan_settings():
# Can get slots this way, but does not automatically resolve synonyms
# def set_fan_settings(temp_mode, power_level, temp_level, power_mode):

    # Using sdk
    temp_mode = get_slot_value("temp_mode") # 'hot' or 'cold'
    power_level = get_slot_value("power_level") # 1-9
    temp_level = get_slot_value("temp_level") # 60-90

    output = []

    if temp_mode:
        output.append(f'Temp mode was toggled to {temp_mode}')
        set_temp_mode(temp_mode)
    if power_level:
        output.append(f'Power level was toggled to {power_level}')
        set_power_level(power_level)
    if temp_level:
        output.append(f'Temp level was toggled to {temp_level} degrees')
        set_temp_level(temp_level)

    output.append('Ending set fan settings intent handling')

    return statement(', '.join(output))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
