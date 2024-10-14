import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageFont, ImageOps
import PokerGame
import Betting
import BotDecisions
#import time

class GameWindow():
    
    def createWindow(self):
        root = tk.Tk()
        root.title("Jester PokerBot")

        root.geometry("1029x600")
        root.resizable(False, False)
        
        backgroundImage = Image.open("pokerTable.png")
        backgroundImage = backgroundImage.resize((1029, 600), Image.Resampling.LANCZOS)
        backgroundPhoto = ImageTk.PhotoImage(backgroundImage)

        canvas = tk.Canvas(root, width=1029, height=600)
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=backgroundPhoto, anchor="nw")

        game = PokerGame.PokerGame()
        player = game.dealPlayerCards()
        bot = game.dealPlayerCards()
        betting = Betting.Betting()
        botDecisions = BotDecisions.BotDecisions()


        broncoImageFont = ImageFont.truetype("/Users/dylandehnert/Desktop/PokerBot/BroncoPersonalUse", size=20)
        broncoFont = font.Font(family=broncoImageFont.getname()[0], size = 20)

        playerCard1Image = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(player, 0))
        playerCard1Image = playerCard1Image.resize((69, 105), Image.Resampling.LANCZOS)
        playerCard1Photo = ImageTk.PhotoImage(playerCard1Image)

        playerCard2Image = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(player, 1))
        playerCard2Image = playerCard2Image.resize((69, 105), Image.Resampling.LANCZOS)
        playerCard2Photo = ImageTk.PhotoImage(playerCard2Image)

        botCardImage = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/cardBack.png')
        botCardImage = botCardImage.resize((69, 105), Image.Resampling.LANCZOS)
        botCardPhoto = ImageTk.PhotoImage(botCardImage)


        #Pot
        potText = canvas.create_text(515, 350, text='Pot: $'+str(betting.getPot()),
                                            fill="#efb550", font=broncoFont)

        #Player
        canvas.create_image(442, 440, image=playerCard1Photo, anchor="nw")
        canvas.create_image(519, 440, image=playerCard2Photo, anchor="nw")

        playerBetText = canvas.create_text(515, 413, text='$'+str(betting.getPlayerBet()),
                                            fill="#efb550", font=broncoFont)
        playerStackText = canvas.create_text(515, 570, text='Stack: $'+str(betting.getPlayerStack()),
                                            fill="#efb550", font=broncoFont)

        #Bot
        canvas.create_image(442, 50, image=botCardPhoto, anchor="nw")
        canvas.create_image(519, 50, image=botCardPhoto, anchor="nw")
        
        botBetText = canvas.create_text(515, 188, text='$'+str(betting.getBotBet()),
                                           fill="#efb550", font=broncoFont)
        botStackText = canvas.create_text(515, 30, text='Stack: $'+str(betting.getBotStack()),
                                            fill="#efb550", font=broncoFont)
        botDecisionText = canvas.create_text(620, 188, text='',
                                            fill="red", font=broncoFont)


        #Grey Box
        greyBoxImage = Image.open('/Users/dylandehnert/Desktop/PokerBot/buttons/greyBox.png')
        greyBoxImage = greyBoxImage.resize((221, 123), Image.Resampling.LANCZOS)
        greyBoxPhoto = ImageTk.PhotoImage(greyBoxImage)
        canvas.create_image(595, 433, image=greyBoxPhoto, anchor="nw")


        #Call Button
        callButtonImage = Image.open('/Users/dylandehnert/Desktop/PokerBot/buttons/callButton.png')
        callButtonImage = callButtonImage.resize((70, 31), Image.Resampling.LANCZOS)
        callButtonPhoto = ImageTk.PhotoImage(callButtonImage)

        callButton = tk.Button(root, text='',image=callButtonPhoto, bd=0,
                               highlightbackground = "#303030", highlightthickness = 2.5,
                                command=lambda: self.playersMove(player, 'PLAYER_CALL', bot, game, canvas, betting, texts, botDecisions, buttons, buttonImages, slider))
        
        grayedCallImage = ImageTk.PhotoImage(ImageOps.grayscale(callButtonImage))
        callImages = [callButtonPhoto,grayedCallImage]
        #callButton.config(state=tk.DISABLED, image=grayedImage)
        canvas.create_window(620, 452, anchor="nw", window=callButton)


        #Fold Button
        foldButtonImage = Image.open('/Users/dylandehnert/Desktop/PokerBot/buttons/foldButton.png')
        foldButtonImage = foldButtonImage.resize((70, 31), Image.Resampling.LANCZOS)
        foldButtonPhoto = ImageTk.PhotoImage(foldButtonImage)

        foldButton = tk.Button(root, text='',image=foldButtonPhoto, bd=0,
                               highlightbackground = "#303030", highlightthickness = 2.5,
                                command=lambda: print('fold'))
        grayedFoldImage = ImageTk.PhotoImage(ImageOps.grayscale(foldButtonImage))
        foldImages = [foldButtonPhoto,grayedFoldImage]
        canvas.create_window(620, 501, anchor="nw", window=foldButton)


        #Bet Button
        betButtonImage = Image.open('/Users/dylandehnert/Desktop/PokerBot/buttons/betButton.png')
        betButtonImage = betButtonImage.resize((70, 31), Image.Resampling.LANCZOS)
        betButtonPhoto = ImageTk.PhotoImage(betButtonImage)

        betButton = tk.Button(root, text='',image=betButtonPhoto, bd=0,
                               highlightbackground = "#303030", highlightthickness = 2.5,
                                command=lambda: self.playersMove(player, 'PLAYER_BET', bot, game, canvas, betting, texts, botDecisions, buttons, buttonImages, slider))
        grayedBetImage = ImageTk.PhotoImage(ImageOps.grayscale(betButtonImage))
        betImages = [betButtonPhoto,grayedBetImage]
        canvas.create_window(710, 452, anchor="nw", window=betButton)

        # sliderText = canvas.create_text(820, 471, text='Bet: $0',
        #                                         fill="#efb550", font=broncoFont)
        slider = tk.Scale(root, from_=10, to=betting.getPlayerStack(), orient='horizontal', font=broncoFont, troughcolor='white',
                          cursor='dotbox', length=75, command='changing')
        slider.place(x=815, y=449)

        if betting.getBetState() == 'PLAYER_FACING_BET':
            slider.config(from_=2*betting.getBotBet())
        #elif betting.getBetState() == 'PLAYER_MOVE':
        
        #else:
        
        #Check Button
        checkButtonImage = Image.open('/Users/dylandehnert/Desktop/PokerBot/buttons/checkButton.png')
        checkButtonImage = checkButtonImage.resize((70, 31), Image.Resampling.LANCZOS)
        checkButtonPhoto = ImageTk.PhotoImage(checkButtonImage)

        checkButton = tk.Button(root, text='',image=checkButtonPhoto, bd=0,
                               highlightbackground = "#303030", highlightthickness = 2.5,
                                command=lambda: self.playersMove(player, 'PLAYER_CHECK', bot, game, canvas, betting, texts, botDecisions, buttons, buttonImages, slider))
        grayedCheckImage = ImageTk.PhotoImage(ImageOps.grayscale(checkButtonImage))
        checkImages = [checkButtonPhoto,grayedCheckImage]
        canvas.create_window(710, 501, anchor="nw", window=checkButton)

        buttonImages = [callImages, foldImages, betImages, checkImages]
        buttons = [callButton, foldButton, betButton, checkButton]
        texts = [playerBetText, botBetText, potText, playerStackText, botStackText, botDecisionText]
        #Update UI
        self.updateUI(betting, buttons, buttonImages, slider)

        if betting.isPlayerBB:
            self.botsMove(player, bot, game, canvas, betting, texts, botDecisions, buttons, buttonImages, slider)

        root.mainloop()
        
    
    def dealCards(self, player, bot, game, canvas):
        if len(game.getCommCards()) == 0:
            self.dealFlop(game, canvas)
        elif len(game.getCommCards()) == 3:
            self.dealTurnOrRiver(game, canvas, 3)
        elif len(game.getCommCards()) == 4:
            self.dealTurnOrRiver(game, canvas, 4)
        elif len(game.getCommCards()) == 5:
            self.determineWinner(player, bot, game, canvas)


    def dealFlop(self, game, canvas):
        game.flopCards()
        flop = game.getCommCards()

        flopCard1Image = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(flop, 0))
        flopCard1Image = flopCard1Image.resize((69, 105), Image.Resampling.LANCZOS)
        flopCard1Photo = ImageTk.PhotoImage(flopCard1Image)

        flopCard2Image = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(flop, 1))
        flopCard2Image = flopCard2Image.resize((69, 105), Image.Resampling.LANCZOS)
        flopCard2Photo = ImageTk.PhotoImage(flopCard2Image)

        flopCard3Image = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(flop, 2))
        flopCard3Image = flopCard3Image.resize((69, 105), Image.Resampling.LANCZOS)
        flopCard3Photo = ImageTk.PhotoImage(flopCard3Image)

        if not hasattr(self, 'flopCards'):
            self.flopCards = []
        self.flopCards.extend([flopCard1Photo, flopCard2Photo, flopCard3Photo])

        canvas.create_image(326, 225, image=flopCard1Photo, anchor="nw")
        canvas.create_image(403, 225, image=flopCard2Photo, anchor="nw")
        canvas.create_image(480, 225, image=flopCard3Photo, anchor="nw")

    def dealTurnOrRiver(self, game, canvas, pos):
        game.turnOrRiverCard()
        cards = game.getCommCards()

        nextCardImage = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(cards, pos))
        nextCardImage = nextCardImage.resize((69, 105), Image.Resampling.LANCZOS)
        nextCardPhoto = ImageTk.PhotoImage(nextCardImage)

        if not hasattr(self, 'turnRiverCards'):
            self.turnRiverCards = {}
        self.turnRiverCards[pos] = nextCardPhoto

        if pos == 3:
            canvas.create_image(557, 225, image=nextCardPhoto, anchor="nw")
        elif pos == 4:
            canvas.create_image(634, 225, image=nextCardPhoto, anchor="nw")

    def determineWinner(self, player, bot, game, canvas):
        botCard1Image = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(bot, 0))
        botCard1Image = botCard1Image.resize((69, 105), Image.Resampling.LANCZOS)
        botCard1Photo = ImageTk.PhotoImage(botCard1Image)

        botCard2Image = Image.open('/Users/dylandehnert/Desktop/PokerBot/cardImages/' + self.cardsToImg(bot, 1))
        botCard2Image = botCard2Image.resize((69, 105), Image.Resampling.LANCZOS)
        botCard2Photo = ImageTk.PhotoImage(botCard2Image)

        if not hasattr(self, 'botCards'):
            self.botCards = []
        self.botCards.extend([botCard1Photo, botCard2Photo])

        canvas.create_image(442, 50, image=botCard1Photo, anchor="nw")
        canvas.create_image(519, 50, image=botCard2Photo, anchor="nw")

        winner = game.determineWinner([player, bot])

        if isinstance(winner, int) or len(winner) == 1:
            if isinstance(winner, list):
                winner = winner[0]
            if winner == 0:
                canvas.create_text(515, 380, text="You Win!", fill="Green",
                                   font=font.Font(family= ImageFont.truetype("/Users/dylandehnert/Desktop/PokerBot/BroncoPersonalUse", size=24).getname()[0], size = 24))
            else:
                canvas.create_text(515, 380, text="You Lose!", fill="Red",
                                   font=font.Font(family= ImageFont.truetype("/Users/dylandehnert/Desktop/PokerBot/BroncoPersonalUse", size=24).getname()[0], size = 24))
        else:
            canvas.create_text(515, 380, text="You Tie!", fill="yellow",
                               font=font.Font(family= ImageFont.truetype("/Users/dylandehnert/Desktop/PokerBot/BroncoPersonalUse", size=24).getname()[0], size = 24))


    def cardsToImg(self, cards, pos):
        if cards[pos][0] == 14:
            return 'A' + cards[pos][1].upper() + '.png'
        elif cards[pos][0] == 13:
            return 'K' + cards[pos][1].upper() + '.png'
        elif cards[pos][0] == 12:
            return 'Q' + cards[pos][1].upper() + '.png'
        elif cards[pos][0] == 11:
            return 'J' + cards[pos][1].upper() + '.png'
        
        return str(cards[pos][0]) + cards[pos][1].upper() + '.png'
    
    def updateUI(self, betting, buttons, buttonImages, slider):
        if betting.getBetState() == 'BOT_MOVE' or betting.getBetState() == 'BOT_FACING_BET' or betting.getStage() == 4:
            buttons[0].config(state=tk.DISABLED, image=buttonImages[0][1])
            buttons[1].config(state=tk.DISABLED, image=buttonImages[1][1])
            buttons[2].config(state=tk.DISABLED, image=buttonImages[2][1])
            buttons[3].config(state=tk.DISABLED, image=buttonImages[3][1])
        elif betting.getBetState() == 'PLAYER_MOVE':
            buttons[0].config(state=tk.DISABLED, image=buttonImages[0][1])
            buttons[1].config(state=tk.DISABLED, image=buttonImages[1][1])
            buttons[2].config(state=tk.NORMAL, image=buttonImages[2][0])
            buttons[3].config(state=tk.NORMAL, image=buttonImages[3][0])
            slider.config(from_=10, to=betting.getPlayerStack())
        elif betting.getBetState() == 'PLAYER_FACING_BET':
            buttons[0].config(state=tk.NORMAL, image=buttonImages[0][0])
            buttons[1].config(state=tk.NORMAL, image=buttonImages[1][0])
            buttons[2].config(state=tk.NORMAL, image=buttonImages[2][0])
            buttons[3].config(state=tk.DISABLED, image=buttonImages[3][1])
            slider.config(from_=2*betting.getBotBet())
        elif betting.getBetState() == 'ROUND_OVER':
            buttons[0].config(state=tk.DISABLED, image=buttonImages[0][1])
            buttons[1].config(state=tk.DISABLED, image=buttonImages[1][1])
            buttons[2].config(state=tk.DISABLED, image=buttonImages[2][1])
            buttons[3].config(state=tk.DISABLED, image=buttonImages[3][1])
            slider.config(from_=0, state=tk.DISABLED)
    
    def playersMove(self, player, decision, bot, game, canvas, betting, texts, botDecisions, buttons, buttonImages, slider):
        amt = 0
        if decision == 'PLAYER_CALL':
            if not betting.getFirstMove() or betting.getIsPlayerBB():
                self.dealCards(player, bot, game, canvas)
        elif decision == 'PLAYER_CHECK':
            if betting.getIsPlayerBB():
                self.dealCards(player, bot, game, canvas)
        elif decision == 'PLAYER_BET':
            #if betting.getIsPlayerBB():
            #self.dealCards(player, bot, game, canvas)
            amt = slider.get()
            print('this is the amt: ' + str(amt))

        betting.updateBetState(decision, amt)
        
        self.updateAmts(canvas, betting, texts)
        self.updateUI(betting, buttons, buttonImages, slider)
        
        print(betting.getStage())

        canvas.itemconfig(texts[5], text='')
        if betting.getStage != 4 and betting.getBetState() == 'BOT_MOVE' or betting.getBetState() == 'BOT_FACING_BET':
            self.botsMove(player, bot, game, canvas, betting, texts, botDecisions, buttons, buttonImages, slider)
        


    def botsMove(self, player, bot, game, canvas, betting, texts, botDecisions, buttons, buttonImages, slider):
        if (betting.getBetState() == 'BOT_MOVE' or betting.getBetState() == 'BOT_FACING_BET') and betting.getStage() != 4:
            decision = botDecisions.chooseDecision(betting.getBetState())
            print('this is the dec:' + decision)

            amt = 0
            if decision == 'BOT_BET':
                if betting.getPot() == 0 or betting.getBetState() == 'BOT_FACING_BET':
                    amt = round(3 * betting.getPlayerBet())
                elif betting.getBetState() == 'BOT_MOVE':
                    amt = round(0.5 * betting.getPot())
                print(amt)
            
            if decision=='BOT_CALL' and (not betting.getFirstMove() or not betting.getIsPlayerBB()):
                self.dealCards(player, bot, game, canvas)
            elif decision=='BOT_CHECK' and not betting.getIsPlayerBB():
                self.dealCards(player, bot, game, canvas)

            betting.updateBetState(decision, amt)
            print(betting.getBetState())
            print('pot: ' + str(betting.getPot()))
            print('stage: ' + str(betting.getStage()))
            self.updateAmts(canvas, betting, texts)
            
            self.updateUI(betting, buttons, buttonImages, slider)
            
            if decision=='BOT_FOLD':
                canvas.itemconfig(texts[5], text='Jester folded.')
            elif decision=='BOT_CALL':
                canvas.itemconfig(texts[5], text='Jester called.')
            elif decision=='BOT_BET':
                canvas.itemconfig(texts[5], text='Jester raised to $' + str(betting.getBotBet()) + '.')
            elif decision=='BOT_CHECK':
                canvas.itemconfig(texts[5], text='Jester checked.')

    def updateAmts(self, canvas, betting, texts):
        canvas.itemconfig(texts[0], text='$' + str(betting.getPlayerBet()))
        canvas.itemconfig(texts[1], text='$' + str(betting.getBotBet()))
        canvas.itemconfig(texts[2], text='Pot: $' + str(betting.getPot()))
        canvas.itemconfig(texts[3], text='Stack: $' + str(betting.getPlayerStack()))
        canvas.itemconfig(texts[4], text='Stack: $' + str(betting.getBotStack()))

window = GameWindow()
window.createWindow()