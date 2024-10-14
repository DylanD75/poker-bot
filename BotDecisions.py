import random

class BotDecisions:
    def __init__(self):
        self.moves = ['BOT_CALL', 'BOT_FOLD', 'BOT_BET', 'BOT_CHECK']
        self.facingBetDec = [1/3, 1/3, 1/3, 0]
        self.moveDec = [0, 0, 0.5, 0.5]
    
    def chooseDecision(self, bettingState):
        if bettingState == 'BOT_MOVE':
            return random.choices(self.moves, self.moveDec, k=1)[0]
        elif bettingState == 'BOT_FACING_BET':
            return random.choices(self.moves, self.facingBetDec, k=1)[0]