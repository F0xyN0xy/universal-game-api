from gameapi import GameAPI
api = GameAPI()
player = api.player(game='chess_com', identifier='hikaru')
print(player.name, player.rank.tier, player.rank.rating)
print(player.stats)
for m in api.matches(game='chess_com', identifier='hikaru', limit=3):
    print(m.result, m.opponent, m.played_at)
board = api.leaderboard(game='chess_com')
print([(e.position, e.name) for e in board.entries[:5]])
api.close()
