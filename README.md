# Jester PokerBot

This PokerBot, named "Jester," plays heads-up poker against a user player, utilizing an unexploitable GTO-style strategy. I used Python and TKinter to create a functional GUI where the user can input their decisions (calling, folding, etc.) to play against Jester. The decision-making for the bot utilizes the Monte Carlo Counterfactual Regret Minimization algorithm (MCCFR) to find a Nash Equilibrium based on abstracted game states. The user plays against Jester until one of them has $0 remaining.

![Alt text](git_pic.png)

## Hand Evalution

My hand evaluation algorithm determines whether the user or bot won in the following way:
- Determines what hand ranking each player has (i.e. straight, flush, one-pair) by combining their hole cards with the community cards
- Returns the player with the higher hand ranking
- If equivalent hand ranking, iterate over each value in that type of ranking until one value is higher than another.
  Ex. My algorithm handles this step differently for each hand ranking. For flushes, it compares the highest flush card value, then the next flush card value, and so on for all 5 flush cards. For two pair, it compares the higher pair value, then the lower pair value, and finally the kicker card value. It repeats similar procedures for the other hand ranks.
- Otherwise, both players have the same hand.
