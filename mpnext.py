"""quick and dirty interface to a few matchplay api functions"""

import logging
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)s %(module)s %(funcName)s %(levelname)s %(message)s')
logger.setLevel(logging.DEBUG)

BASE_URL = """https://next.matchplay.events/api"""


class MpNext():

    def __init__(self, api_key, debug=True):
        self.api_key = api_key
        self.debug = debug

        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    def _get_url(self, url, extra_headers={}, debug=True, **params):
        _headers = dict(self.headers)
        _headers.update(extra_headers)

        if debug:
            print(f"getting {url} {_headers=} {params=}")
        r = requests.get(url, headers=_headers, params=params)
        data = r.json()

        return data

    def _post_url(self, url, post_data={}, debug=True):
        r = requests.post(url, json=post_data)
        data = r.json()
        return data

    def get_tournament(self, tournament_tournament_id, **params):
        url = f'{BASE_URL}/tournaments/{tournament_tournament_id}'
        return self._get_url(url, tournament_tournament_id=tournament_tournament_id, **params)

    def get_tournament_games(self, tournament_tournament_id, **params):
        url = f'{BASE_URL}/tournaments/{tournament_tournament_id}/games'
        return self._get_url(url, tournament_tournament_id=tournament_tournament_id, **params)