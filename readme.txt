quick and dirty tool to randomly suggest machine replacement for flip frenzies
since it can't do it automatically and all hell seems to break loose whenever people do it wrong


setup:

    install requirements.txt with pip

    set up environment variables
        FLASK_SECRET_KEY = for security
        NEXT_MATCHPLAY_API_KEY = your api key you got from matchplay
        whatever else you need locally


    start the flask app


    browse to http://<servername>:<port>/active/<matchplay_tournament_id>

    it will show a list of active games and who is on them

    to reassign a game click "reassign"

    it will query the matchplay api for available games and suggest one randomly

    do what it says.   EXACTLY.

