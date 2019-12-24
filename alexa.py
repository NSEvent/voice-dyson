from flask import Flask
from flask_ask import Ask, statement, question, session
import json

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
def set_fan_settings(temp_mode, fan_num, degrees, power_mode):

    # Using sdk
    # power_mode = get_slot_value(handler_input=handler_input, slot_name="power_mode")
    # temp_mode = get_slot_value(handler_input=handler_input, slot_name="temp_mode")
    # fan_num = get_slot_value(handler_input=handler_input, slot_name="fan_num")
    # degrees = get_slot_value(handler_input=handler_input, slot_name="degrees")

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
