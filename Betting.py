import random

class Betting:

    def __init__(self):
        self.playerStack = 1000
        self.botStack = 1000
        self.pot = 0
        #self.currentBet = 5
        self.isPlayerBB = random.choice([True, False])
        self.turn = not self.isPlayerBB
        self.bigBlind = 10
        self.smallBlind = 5
        self.stage = 0
        self.firstMove = True
        
        if self.isPlayerBB:
            self.betState = 'BOT_FACING_BET'
            self.playerBet = 10
            self.botBet = 5
            self.playerStack -= self.bigBlind
            self.botStack -= self.smallBlind
        else:
            self.betState = 'PLAYER_FACING_BET'
            self.playerBet = 5
            self.botBet = 10
            self.botStack -= self.bigBlind
            self.playerStack -= self.smallBlind

    def getPlayerStack(self):
        return self.playerStack
    
    def getBotStack(self):
        return self.botStack

    def getPot(self):
        return self.pot
    
    def getCurrentPot(self):
        return self.pot
    
    def getPlayerBet(self):
        return self.playerBet
    
    def getBotBet(self):
        return self.botBet
    
    def getIsPlayerBB(self):
        return self.isPlayerBB
    
    def getStage(self):
        return self.stage
    
    def getBetState(self):
        return self.betState
    
    def getFirstMove(self):
        return self.firstMove
    
    def updateBetState(self, action, amt=0):
        if action == 'PLAYER_CALL':
            #print(self.betState)
            assert self.betState == 'PLAYER_FACING_BET'
            
            self.playerStack -= self.botBet - self.playerBet
            self.playerBet = self.botBet


            if not self.firstMove:
                self.pot += self.playerBet + self.botBet
                self.playerBet = 0
                self.botBet = 0
                self.stage += 1
            
            #self.currentBet = 0
        

            if self.isPlayerBB or self.firstMove:
                self.betState = 'BOT_MOVE'
            else:
                self.betState = 'PLAYER_MOVE'
            
            self.firstMove = False

            #print(self.betState)
            return self.betState

        elif action == 'BOT_CALL':
            assert self.betState == 'BOT_FACING_BET'

            self.botStack -= self.playerBet - self.botBet
            self.botBet = self.playerBet

            if not self.firstMove:
                self.pot += self.playerBet + self.botBet
                self.playerBet = 0
                self.botBet = 0
                self.stage += 1

            if self.isPlayerBB and not self.firstMove:
                self.betState = 'BOT_MOVE'
            else:
                self.betState = 'PLAYER_MOVE'

            self.firstMove = False

            return self.betState
        elif action == 'PLAYER_CHECK':
            assert self.betState == 'PLAYER_MOVE'

            if self.isPlayerBB:
                self.stage += 1

            if self.playerBet != 0:
                self.pot += self.playerBet + self.botBet
                self.playerBet = 0
                self.botBet = 0

            self.firstMove = False

            if self.stage == 4:
                self.betState = 'ROUND_OVER'
                
            self.betState = 'BOT_MOVE'
        elif action == 'BOT_CHECK':
            assert self.betState == 'BOT_MOVE'

            if self.botBet != 0:
                self.pot += self.playerBet + self.botBet
                self.playerBet = 0
                self.botBet = 0

            if not self.isPlayerBB:
                self.stage += 1

            self.firstMove = False
                
            self.betState = 'PLAYER_MOVE'
        elif action == 'PLAYER_BET':
            assert self.betState == 'PLAYER_MOVE' or self.betState == 'PLAYER_FACING_BET'

            self.playerBet += amt
            self.playerStack -= amt

            self.firstMove = False
            
            self.betState = 'BOT_FACING_BET'
        elif action == 'BOT_BET':
            assert self.betState == 'BOT_MOVE' or self.betState == 'BOT_FACING_BET'

            self.botBet += amt
            self.botStack -= amt

            self.betState = 'PLAYER_FACING_BET'

            self.firstMove = False
        elif action == 'PLAYER_FOLD':
            assert self.betState == 'PLAYER_MOVE' or self.betState == 'PLAYER_FACING_BET'

            self.botStack += self.pot + self.playerBet + self.botBet

            self.betState = 'ROUND_OVER'
        elif action == 'BOT_FOLD':
            assert self.betState == 'BOT_MOVE' or self.betState == 'BOT_FACING_BET'

            print('works')

            self.playerStack += self.pot + self.playerBet + self.botBet

            self.betState = 'ROUND_OVER'


