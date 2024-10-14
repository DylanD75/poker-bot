# poker-bot

This PokerBot, named "Jester," plays heads-up poker against a user player, utilizing an unexploitable GTO-style strategy. I used Python and TKinter to create a functional GUI where the user can input their decisions (calling, folding, etc.) to play against Jester. The decision-making for the bot utilizes the Monte Carlo Counterfactual Regret Minimization algorithm (MCCFR) to find a Nash Equilibrium based on abstracted game states. The user plays against Jester until one of them has $0 remaining.

![Alt text](git_pic.png)
