from flask import Flask
from flask_ask import Ask, statement, question, session, request
import json

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
    return 'An Alexa skill for toggling Dyson settings'

@ask.launch
def start_skill():
    speech_text = "Eat more raspberry pie"
    return statement(speech_text)

@ask.intent('set_fan_settings')
def set_fan_settings():
# Can get slots this way, but does not automatically resolve synonyms
# def set_fan_settings(temp_mode, fan_num, degrees, power_mode):

    # Using sdk
    power_mode = get_slot_value("power_mode")
    temp_mode = get_slot_value("temp_mode")
    fan_num = get_slot_value("fan_num")
    degrees = get_slot_value("degrees")

    output = []

    if power_mode:
        output.append(f'Power was toggled to {power_mode}')
    # TODO: Temp mode does not resolve to hot and cold, can be warm or cool currently
    if temp_mode:
        output.append(f'Temp mode was toggled to {temp_mode}')
    if fan_num:
        output.append(f'Fan number was toggled to {fan_num}')
    if degrees:
        output.append(f'Fan was toggled to {degrees} degrees')

    output.append('Ending set fan settings intent handling')

    return statement(', '.join(output))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
