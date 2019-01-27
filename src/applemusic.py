import os
import pprint

import sys
sys.path.append('src/apple-py-music')

from applepymusic import AppleMusicClient

class AppleMusic:
    def __init__(self):
        self.client = AppleMusicClient( os.environ['APPLEMUSIC_TEAMID'],
                                        os.environ['APPLEMUSIC_KEY'],
                                        str(os.environ['APPLEMUSIC_SECRET']).replace(r'\n', '\n'),
                                        access_token="AgtzQmglsdXAFX2GPW12mSpOr3rqIN/pd6/4zDE+RLWnk7UyhKJkbSizml7uYF7ROHSUPvBM6evJFbE5lP3GWgi38UHZ2c6xKZaKsMiDlGNJ/X60qU3gT/WjvGf7q1k4bJxqyrx/Rt7ZfiekXbt3nnvT/zzICHx+rxOFZBgt3nwNkP4ZpLrcIhRALWmq9g21gZZhga1bFPknykAyXFS0lIZ6WE6L7xH0yRLJ/ktzMx9oMXwNcQ=="
                                        )

    def sample_code(self):
        resp = self.client.get_songs_by_isrc('US2U61726301')
        pprint.pprint(resp)




    def get_user_playlist(self):
        resp = self.client.user_playlists(limit=5)
        pprint.pprint(resp)