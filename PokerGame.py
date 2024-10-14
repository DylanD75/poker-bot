import random
import itertools

STRAIGHT_FLUSH = 9
QUADS = 8
FULL_HOUSE = 7
FLUSH = 6
STRAIGHT = 5
TRIPS = 4
TWO_PAIR = 3
PAIR = 2
HIGH_CARD = 1

class PokerGame:
    def __init__(self):
        self.suits = ['c', 'd', 'h', 's']
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.deck = list(itertools.product(self.values, self.suits))
        random.shuffle(self.deck)
        self.commCards = []
    
    def reset(self):
        self.deck = list(itertools.product(self.values, self.suits))
        random.shuffle(self.deck)
        self.commCards = []

    def getDeck(self):
        return self.deck
    
    def getCommCards(self):
        return self.commCards
    
    def setCommCards(self, commCards):
        self.commCards = commCards
    
    def getValues(self, cards):
        assert len(cards) > 0

        values = []
        for card in cards:
            values.append(card[0])
        values = sorted(values)
        return values
    
    def getSuits(self, cards):
        assert len(cards) > 0

        suits = []
        for card in cards:
            suits.append(card[1])
        return suits
    
    def getValsOfSuits(self, cards, suit):
        assert suit in self.suits
        
        vals = []
        for card in cards:
            if card[1] == suit:
                vals.append(card[0])
        vals = sorted(vals)
        return vals

    def dealPlayerCards(self):
        return [self.deck.pop(), self.deck.pop()]
    
    def flopCards(self):
        self.commCards = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        return self.commCards

    def turnOrRiverCard(self):
        self.commCards.append(self.deck.pop())
        return self.commCards
    
    def isStraight(self, vals):
        #Cards can be values or cards
        #Returns straight value and cards involved in straight, otherwise -1
        assert len(vals) >= 5

        max = 0
        vals = list(set(vals))

        for i in range(len(vals) - 4):
            if vals[i+4] - vals[i] == 4:
                if vals[i+4] > max:
                    max = vals[i+4]
            elif 2 in vals and 3 in vals and 4 in vals and 5 in vals and 14 in vals:
                if 5 > max:
                    max = 5
        if not (max == 0 or max ==5):
            return [STRAIGHT, max-4, max-3, max-2, max-1, max]
        if max == 5:
            return [STRAIGHT, 14, 2, 3, 4, 5]
        return -1
    
    def isFlush(self, cards):
        #Returns list with flush value and cards of that suit present in the cards if flush exists, otherwise -1
        assert len(cards) >= 5

        suitsInCards = self.getSuits(cards)

        for suit in self.suits:
            if suitsInCards.count(suit) >= 5:
                vals = self.getValsOfSuits(cards, suit)
                vals.insert(0, FLUSH)
                return vals
        return -1
    
    def isQuads(self, vals):
        assert len(vals) >= 5

        valsNoDups = list(set(vals))

        for val in valsNoDups:
            if vals.count(val) == 4:
                return [QUADS, val, max(item for item in valsNoDups if item != val)]
        return -1

    def isStraightFlush(self, cards):
        assert len(cards) >= 5

        vals = self.isFlush(cards)

        if vals == -1:
            return -1
        
        vals = vals[1:len(vals)]

        if not self.isStraight(vals)  == -1:
            vals.insert(0, STRAIGHT_FLUSH)
            return vals
        return -1
    
    def isPairOrTwo(self, vals):
        assert len(vals) >= 5

        valsNoDups = list(set(vals))
        count = []

        for val in valsNoDups:
            if vals.count(val) == 2:
                count.append(val)

        if len(count) == 1:
            ans = [PAIR, count[0]]
            
            rest = valsNoDups
            rest.remove(count[0])

            #error
            for i in range(3):
                ans.append(rest[len(rest) - 3 + i])
            
            return ans
        elif len(count) >= 2:
            max1 = max(count)
            max2 = max(item for item in count if item != max1)
            max3 = max(item for item in valsNoDups if item != max1 and item != max2)

            return [TWO_PAIR, max1, max2, max3]

        return -1
    
    def isFullHouse(self, vals):
        assert len(vals) >= 5

        valsNoDups = list(set(vals))
        tripsCount = []
        pairCount = []

        for val in valsNoDups:
            if vals.count(val) == 3:
                tripsCount.append(val)
            elif vals.count(val) == 2:
                pairCount.append(val)

        if len(tripsCount) >= 1:
            max1 = max(tripsCount)
            tripsCount.remove(max1)

            try:
                max2 = max(tripsCount + pairCount)
            except:
                max2 = 0

            if max2 != 0:
                return [FULL_HOUSE, max1, max2]
    
        return -1
    
    def isTrips(self, vals):
        assert len(vals) >= 5

        valsNoDups = list(set(vals))
        tripsCount = []

        for val in valsNoDups:
            if vals.count(val) == 3:
                tripsCount.append(val)

        if len(tripsCount) == 1:
            max1 = max(tripsCount)
            max2 = max(item for item in valsNoDups if item != max1)
            max3 = max(item for item in valsNoDups if item != max1 and item != max2)
            return [TRIPS, max1, max3, max2]
    
        return -1
    
    def evaluateCards(self, cards):
        assert len(cards) == 7

        vals = self.getValues(cards)

        hand = self.isStraightFlush(cards)
        if hand != -1: return hand

        hand = self.isQuads(vals)
        if hand != -1: return hand

        hand = self.isFullHouse(vals)
        if hand != -1: return hand

        hand = self.isFlush(cards)
        if hand != -1: return hand

        hand = self.isStraight(vals)
        if hand != -1: return hand

        hand = self.isTrips(vals)
        if hand != -1: return hand

        hand = self.isPairOrTwo(vals)
        if hand != -1: return hand

        vals = vals[len(vals)-5:len(vals)]
        return [HIGH_CARD, vals[0], vals[1], vals[2], vals[3], vals[4]]
    
    def determineWinner(self, playerHands):
        assert len(self.commCards) == 5

        playerRanks = [self.evaluateCards(hand + self.commCards) for hand in playerHands]
        highestRank = max(playerRanks, key=lambda x: x[0])[0]

        ranks = {}
        for i in range(len(playerRanks)):
            if playerRanks[i][0] == highestRank:
                ranks[i] = playerRanks[i]
        
        if len(ranks) == 1:
            winner = next(iter(ranks))
            return winner

        if highestRank == 1:
            return self.iterDesc(ranks)
        
        if highestRank == 2:
            return self.compareFirstThenRest(ranks)
        
        if highestRank == 3:
            firstPairVal = max(value[1] for value in ranks.values())
            keys = list(ranks.keys())
            for pos in keys:
                if ranks[pos][1] != firstPairVal:
                   del ranks[pos]
            if len(ranks) == 1:
                winner = next(iter(ranks))
                return winner
            
            secondPairVal = max(value[2] for value in ranks.values())
            keys = list(ranks.keys())
            for pos in keys:
                if ranks[pos][2] != secondPairVal:
                   del ranks[pos]
            if len(ranks) == 1:
                winner = next(iter(ranks))
                return winner
            return self.iterDesc(ranks)

        if highestRank == 4:
            return self.compareFirstThenRest(ranks)

        if highestRank == 5:
            straightHigh = max(value[-1] for value in ranks.values())

            keys = list(ranks.keys())
            for pos in keys:
                if ranks[pos][5] != straightHigh:
                   del ranks[pos]
            return list(ranks.keys())
        
        if highestRank == 6:
            return self.iterDesc(ranks)
        
        if highestRank == 7:
            return self.compareFirstThenRest(ranks)
        
        if highestRank == 8:
            return self.compareFirstThenRest(ranks)
        
        if highestRank == 9:
            straightHigh = max(value[-1] for value in ranks.values())

            keys = list(ranks.keys())
            for pos in keys:
                if ranks[pos][5] != straightHigh:
                   del ranks[pos]
            return list(ranks.keys())
    
    def compareFirstThenRest(self, ranks):
        val = max(value[1] for value in ranks.values())
        keys = list(ranks.keys())
        for pos in keys:
            if ranks[pos][1] != val:
                del ranks[pos]
        if len(ranks) == 1:
            winner = next(iter(ranks))
            return winner
        return self.iterDesc(ranks)

    def highestValDesc(self, ranks):
        high = max(value[-1] for value in ranks.values())

        keys = list(ranks.keys())
        for pos in keys:
            if ranks[pos][-1] != high:
                del ranks[pos]
        return ranks
    
    def iterDesc(self, ranks):
        length = min(len(value) for value in ranks.values())
        rem = self.highestValDesc(ranks)
        newRanks = ranks
        i = 0
        while len(rem) > 1 and i < length - 1:
            newRanks = {key: value[:-1] for key, value in newRanks.items()}
            rem = self.highestValDesc(newRanks)
            i += 1
        return list(rem.keys())


#game = PokerGame()

# playerWins = [0, 0, 0, 0, 0, 0]
# num = 0

# for i in range(1000):
#     game.reset()
#     player1 = game.dealPlayerCards()
#     player2 = game.dealPlayerCards()
#     player3 = game.dealPlayerCards()
#     player4 = game.dealPlayerCards()
#     player5 = game.dealPlayerCards()
#     player6 = game.dealPlayerCards()

#     game.flopCards()
#     game.turnOrRiverCard()
#     game.turnOrRiverCard()

#     winners = game.determineWinner([player1, player2, player3, player4, player5, player6])
#     num += 1

#     if isinstance(winners, int):
#         playerWins[winners] += 1
#     else:
#         for pos in winners:
#             playerWins[pos] += (1/len(winners))
# playerWins = [player / num for player in playerWins]
# print(playerWins)





# player1 = [[14, 'd'], [8, 'c']]

# player2 = [[13, 'd'], [13, 'c']]
# # player2 = game.dealPlayerCards()

# print('')
# print('P1: ' + str(player1))
# print('P2: ' + str(player2))

# print('')
# #print('Flop: ' + str(game.flopCards()))
# #print('Turn: ' + str(game.turnOrRiverCard()))
# #print('River: ' + str(game.turnOrRiverCard()))
# game.setCommCards([[3, 'c'], [4, 'd'], [5, 's'], [2, 'd'], [13, 'h']])
# print('River: ' + str(game.getCommCards()))
# print('')
# print('P1 Hand:' + str(game.evaluateCards(player1 + game.getCommCards())))
# print('')
# print('P2 Hand:' + str(game.evaluateCards(player2 + game.getCommCards())))
# print('')
# print("Winner: Player(-1) " + str(game.determineWinner([player1, player2])))
# print('')

# #print("Test Flush: " + str(game.determineWinner([[[3, 'd'], [3, 'h']], [[3, 'c'], [3, 's']]])))