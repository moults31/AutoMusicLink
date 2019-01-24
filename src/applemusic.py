import os
import pprint

import sys
sys.path.append('src/apple-py-music')

from applepymusic import AppleMusicClient

class AppleMusic:
    def __init__(self):
        self.client = AppleMusicClient( os.environ['APPLEMUSIC_TEAMID'],
                                        os.environ['APPLEMUSIC_KEY'],
                                        str(os.environ['APPLEMUSIC_SECRET']).replace(r'\n', '\n'))

    def sample_code(self):
        resp = self.client.get_songs_by_isrc('US2U61726301')
        pprint.pprint(resp)
