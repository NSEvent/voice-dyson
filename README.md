# voice-dyson
A custom Alexa skill paired with a Raspberry Pi to control a [Dyson Pure Hot+Cool HP01 purifying heater + fan](https://www.dyson.com/purifiers/dyson-pure-hot-cool-purifier.html)

## About
This repo contains code to run a custom Alexa skill on the Alexa Skills Kit Developer Console and a Flask web server on your Raspberry Pi to control a Dyson fan via IR signals.

Although this setup is intended for a specific device, these files may be modified to use Alexa to control any device that can be controlled with an IR remote.

*User speech command -> Alexa skill -> JSON with parsed arguments -> Flask server -> LIRC -> Dyson fan changes state*

Tested with Python 3.7 running [Raspbian Buster 2019-06-20](https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-06-24/) using an [IR Remote Shield v1.0](http://www.raspberrypiwiki.com/index.php/Raspberry_Pi_IR_Control_Expansion_Board)

## Setup
### Alexa skill
The `alexa-voice-model` directory contains everything needed to configure your custom Alexa skill.

1. [Create a new skill](https://developer.amazon.com/alexa/console/ask/create-new-skill) - choose *Custom* for model and *Provision your own* for backend resources
2. In the Alexa Skills Kit Developer Console, find your new skill, and click on *View Skill ID*. Save this string somewhere as we will need it for later for authentification
3. Go to *Edit->Interaction Model->JSON Editor*
4. Copy `interaction_model.json` to the *JSON Editor* and save model
5. Go to *Invocation* and change *Skill Invocation Name* if desired. This will be the phrase that Alexa will listen for to activate your custom skill
6. Go to *Interaction Model->Intent* and click on the new custom intents
7. Under *Sample Utterances*, select *Bulk Edit*
8. Upload `<intent_name>_sample_utterances.csv` for the respective intents, submit, and save model

### Raspberry Pi
The following instructions will be performed on the Raspberry Pi command line.

Note that [IR Remote Shield v1.0](http://www.raspberrypiwiki.com/index.php/Raspberry_Pi_IR_Control_Expansion_Board) needs to be attached to the GPIO pins for IR signals to send.

1. `git clone https://github.com/kvntng17/voice-dyson`
2. `cd voice-dyson`
1. `pip install -r requirements.txt`
2. Follow the instructions listed [here](https://gist.github.com/billpatrianakos/cb72e984d4730043fe79cbe5fc8f7941) to install LIRC for Raspbian Buster 4.19. It also contains instructions to create a custom config for your IR remote if desired
3. `sudo mv dyson.lircd.conf /etc/lirc/lircd.conf`
3. Open `listen_alexa.py` and locate the line that contains `app.config["ASK_APPLICATION_ID"] = "amzn1.ask.skill.e033e61a-290c-46cf-b4cb-679d9ec858a4"`. Paste your own Skill ID here.
4. `sudo apt install tmux`
5. `tmux`
6. `./bin/start_ngrok`
7. Copy the `https://<unique_id>.ngrok.io` address displayed on your screen. Save this address somewhere as we will need to supply it to our Alexa skill so our server can receive information from Alexa.
8. Enter *Ctrl-b* and *d* to detach from this tmux session
9. `tmux`
10. `python listen_alexa.py`
11. Enter *Ctrl-b* and *d* to detach from this tmux session

### Link Alexa skill and Raspberry Pi
1. Open the Alexa Skills Kit Developer Console
2. Go to *Edit->Endpoint*
3. Ensure *HTTPS* is selected
4. Under *Default Region*, paste your ngrok address followed by `/voice_dyson`. It should look like `https://<unique_id>.ngrok.io/voice_dyson`
5. Under the dropdown box, select *My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority*
6. *Save Endpoints*
7. Go to *Intents* and *Save Model* and *Build Model*

Your setup should now be done! Make sure your *ir-tx* IR LED is pointed towards your device, and try a few commands. 

## Sample Commands
"Alexa, ask my fan to turn on."

"Alexa, ask my fan to turn off."

"Alexa, ask my fan to swivel."

"Alexa, ask my fan to change to hot."

"Alexa, ask my fan to change to hot at seventy degrees."

"Alexa, ask my fan to turn to eighty degrees."

"Alexa, ask my fan to change to cold."

"Alexa, ask my fan to change to cold on power level three."

"Alexa, ask my fan to turn to power level five."

## Author
Kevin Tang
