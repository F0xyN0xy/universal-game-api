from gameapi import GameAPI, PlayerNotFoundError
api = GameAPI()
try:
    api.player(game='chess_com', identifier='this-user-should-not-exist-xyz123')
except PlayerNotFoundError as e:
    print('Correctly caught:', e)