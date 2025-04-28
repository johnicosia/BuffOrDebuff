from game import Game

# Display Game Title
print("~"*100)
print(" "*40 + "Buff or Debuff!")
print("~"*100)

# Ask for Player Name
player_name: str = input("Enter your name: ")
print(f"Welcome {player_name}\n")

TOTAL_ROUNDS: int = 4

# Play game
play: bool = True
while play:
    game: Game = Game(player_name, TOTAL_ROUNDS)
    game.play()
    play_again: str = input("\nWould you like to play again? y/n? (exits on non y value) ")
    if play_again.lower() != "y":
        play = False