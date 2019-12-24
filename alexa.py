from flask import Flask
from flask_ask import Ask, statement, question, session
import json

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

    if power_mode:
        statement(f'Power was toggled to {power_mode}')
    if temp_mode:
        statement(f'Temp mode was toggled to {temp_mode}')
    if fan_num:
        statement(f'Fan number was toggled to {fan_num}')
    if degrees:
        statement(f'Fan was toggled to {degrees} degrees')

    speech_text = "Ending set fan settings intent handling"

    return statement(speech_text)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
