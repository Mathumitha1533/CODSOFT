# rps_game.py - Rock-Paper-Scissors Game
# CODSOFT Python Programming Internship - Task 4

import random
import json
import os
from datetime import datetime

# File to store game statistics
STATS_FILE = "rps_stats.json"
game_history = []

# ========== FILE HANDLING ==========

def load_stats():
    """Load game statistics from file"""
    global game_history
    
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as file:
                game_history = json.load(file)
                print("Loaded " + str(len(game_history)) + " game records")
        except:
            print("Error loading stats. Starting fresh.")
            game_history = []
    else:
        print("No saved stats found. Starting fresh.")
        game_history = []

def save_stats():
    """Save game statistics to file"""
    try:
        with open(STATS_FILE, 'w') as file:
            json.dump(game_history, file, indent=4)
        print("Stats saved successfully!")
    except:
        print("Error saving stats!")

# ========== GAME LOGIC ==========

def get_computer_choice():
    """Generate random choice for computer"""
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)

def get_winner(player_choice, computer_choice):
    """Determine the winner"""
    if player_choice == computer_choice:
        return "tie"
    
    # Winning combinations
    if player_choice == "rock" and computer_choice == "scissors":
        return "player"
    elif player_choice == "scissors" and computer_choice == "paper":
        return "player"
    elif player_choice == "paper" and computer_choice == "rock":
        return "player"
    else:
        return "computer"

def display_choices(player_choice, computer_choice):
    """Display both choices"""
    print("\nYou chose: " + player_choice.upper())
    print("Computer chose: " + computer_choice.upper())

# ========== SCORE TRACKING ==========

def update_scores(scores, winner):
    """Update scores based on winner"""
    if winner == "player":
        scores["player"] += 1
        scores["total_games"] += 1
    elif winner == "computer":
        scores["computer"] += 1
        scores["total_games"] += 1
    else:
        scores["ties"] += 1
        scores["total_games"] += 1
    return scores

def display_scores(scores):
    """Display current scores"""
    print("\n" + "="*40)
    print("CURRENT SCORES")
    print("="*40)
    print("You: " + str(scores["player"]) + " wins")
    print("Computer: " + str(scores["computer"]) + " wins")
    print("Ties: " + str(scores["ties"]))
    print("Total: " + str(scores["total_games"]) + " games")
    print("="*40)

def display_final_result(scores):
    """Display final result of the game session"""
    print("\n" + "="*50)
    print("GAME OVER - FINAL RESULTS")
    print("="*50)
    print("You: " + str(scores["player"]) + " wins")
    print("Computer: " + str(scores["computer"]) + " wins")
    print("Ties: " + str(scores["ties"]))
    print("Total: " + str(scores["total_games"]) + " games")
    
    if scores["player"] > scores["computer"]:
        print("\nCONGRATULATIONS! YOU WON THE GAME!")
    elif scores["computer"] > scores["player"]:
        print("\nGAME OVER! COMPUTER WON! Better luck next time!")
    else:
        print("\nIT'S A TIE! Well played!")
    print("="*50)

# ========== SAVE TO HISTORY ==========

def save_to_history(player_choice, computer_choice, winner, scores):
    """Save game result to history"""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "player_choice": player_choice,
        "computer_choice": computer_choice,
        "winner": winner,
        "score_player": scores["player"],
        "score_computer": scores["computer"],
        "score_ties": scores["ties"]
    }
    game_history.append(entry)
    save_stats()

# ========== GAME PLAY FUNCTION ==========

def play_round(scores):
    """Play one round of Rock-Paper-Scissors"""
    print("\n" + "="*40)
    print("ROCK-PAPER-SCISSORS")
    print("="*40)
    
    # Get player choice
    print("\nChoose your move:")
    print("   1. Rock")
    print("   2. Paper")
    print("   3. Scissors")
    
    valid_choices = {"1": "rock", "2": "paper", "3": "scissors"}
    
    while True:
        choice = input("\nEnter your choice (1/2/3): ")
        if choice in valid_choices:
            player_choice = valid_choices[choice]
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")
    
    # Get computer choice
    computer_choice = get_computer_choice()
    
    # Display choices
    display_choices(player_choice, computer_choice)
    
    # Determine winner
    winner = get_winner(player_choice, computer_choice)
    
    # Update scores
    scores = update_scores(scores, winner)
    
    # Display result
    if winner == "player":
        print("\nYOU WIN! " + player_choice.upper() + " beats " + computer_choice.upper() + "!")
    elif winner == "computer":
        print("\nCOMPUTER WINS! " + computer_choice.upper() + " beats " + player_choice.upper() + "!")
    else:
        print("\nIT'S A TIE! Both chose " + player_choice.upper() + "!")
    
    # Save to history
    save_to_history(player_choice, computer_choice, winner, scores)
    
    return scores

# ========== HISTORY FUNCTIONS ==========

def view_history():
    """View game history"""
    if not game_history:
        print("\nNo game history yet!")
        return
    
    print("\n" + "="*70)
    print("GAME HISTORY")
    print("="*70)
    
    # Show last 10 games only
    games_to_show = min(10, len(game_history))
    start_index = len(game_history) - games_to_show
    
    for i in range(start_index, len(game_history)):
        entry = game_history[i]
        winner_text = "PLAYER" if entry["winner"] == "player" else ("COMPUTER" if entry["winner"] == "computer" else "TIE")
        print(str(i+1) + ". " + entry['timestamp'])
        print("   You: " + entry['player_choice'] + " | Computer: " + entry['computer_choice'])
        print("   Winner: " + winner_text)
        print("   Score: You " + str(entry['score_player']) + " - " + str(entry['score_computer']) + " Computer")
        print("-"*60)

def clear_history():
    """Clear game history"""
    global game_history
    
    if not game_history:
        print("History is already empty!")
        return
    
    confirm = input("Are you sure you want to clear ALL history? (y/n): ")
    if confirm.lower() == 'y':
        game_history = []
        save_stats()
        print("Game history cleared!")
    else:
        print("Operation cancelled.")

def show_statistics():
    """Show game statistics"""
    if not game_history:
        print("No games played yet!")
        return
    
    print("\n" + "="*50)
    print("GAME STATISTICS")
    print("="*50)
    
    total_games = len(game_history)
    player_wins = sum(1 for g in game_history if g["winner"] == "player")
    computer_wins = sum(1 for g in game_history if g["winner"] == "computer")
    ties = sum(1 for g in game_history if g["winner"] == "tie")
    
    print("Total games played: " + str(total_games))
    print("Your wins: " + str(player_wins) + " (" + str(round(player_wins/total_games*100, 1)) + "%)")
    print("Computer wins: " + str(computer_wins) + " (" + str(round(computer_wins/total_games*100, 1)) + "%)")
    print("Ties: " + str(ties) + " (" + str(round(ties/total_games*100, 1)) + "%)")
    
    # Win streak analysis
    if total_games > 0:
        recent_wins = sum(1 for g in game_history[-5:] if g["winner"] == "player")
        print("\nLast 5 games: " + str(recent_wins) + "/5 won by you")
    
    # Most common choices
    player_choices = [g["player_choice"] for g in game_history]
    if player_choices:
        most_common = max(set(player_choices), key=player_choices.count)
        print("\nYour most common choice: " + most_common.upper())
    
    print("="*50)

# ========== MAIN MENU ==========

def main():
    """Main program loop"""
    load_stats()
    
    # Initialize scores
    scores = {
        "player": 0,
        "computer": 0,
        "ties": 0,
        "total_games": 0
    }
    
    # Load previous scores from history if exists
    if game_history:
        last_game = game_history[-1]
        scores["player"] = last_game["score_player"]
        scores["computer"] = last_game["score_computer"]
        scores["ties"] = last_game["score_ties"]
        scores["total_games"] = len(game_history)
    
    while True:
        print("\n" + "="*50)
        print("ROCK-PAPER-SCISSORS GAME")
        print("="*50)
        print("1. Play Game")
        print("2. View Scores")
        print("3. View History")
        print("4. View Statistics")
        print("5. Clear History")
        print("6. Exit")
        print("="*50)
        
        choice = input("Choose option (1-6): ")
        
        if choice == '1':
            scores = play_round(scores)
            display_scores(scores)
            
            # Ask to play again
            play_again = input("\nPlay another round? (y/n): ").lower()
            if play_again == 'y':
                continue
            else:
                display_final_result(scores)
                save_stats()
                print("\nThanks for playing!")
                break
                
        elif choice == '2':
            display_scores(scores)
            
        elif choice == '3':
            view_history()
            
        elif choice == '4':
            show_statistics()
            
        elif choice == '5':
            clear_history()
            # Reset scores if history cleared
            if not game_history:
                scores = {
                    "player": 0,
                    "computer": 0,
                    "ties": 0,
                    "total_games": 0
                }
            
        elif choice == '6':
            save_stats()
            print("\nGoodbye! Thanks for playing Rock-Paper-Scissors!")
            break
        else:
            print("Invalid option! Please choose 1-6.")

if __name__ == "__main__":
    main()