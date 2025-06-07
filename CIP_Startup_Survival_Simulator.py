"""
Startup Survival Simulator
--------------------------

A turn-based terminal game where the player acts as the founder of a tech startup. 
Each week, players must choose between strategic options—such as hiring developers, pitching to investors, or pushing the team for overtime—while managing limited cash, team morale, product progress, and investor confidence.

The objective is to successfully launch a minimum viable product (MVP) and maintain investor confidence before the startup runs out of resources.

This game was developed as the final project for Code in Place 2025.

Author: https://github.com/newhandlerdev/
Date: June 2025

Features:
- Custom startup name input
- Weekly strategic decision-making (hire, pitch, or overtime)
- Randomized events that simulate startup unpredictability
- Morale recovery system based on sustainable decision-making
- Cash reserve warnings and investor confidence penalties
- Win/loss conditions based on product readiness, morale, and investor trust

To play:
Run the script in a terminal and follow the prompts to guide your startup week by week.
"""
# ------------- Setup & Constants, Start -------------


import random

# Cash and related values

START_CASH = 100000
HIRE_DEV_COST = 10000
EMERGENCY_REPAIR = 6000
LOW_CASH_WARNING = 15000
GRANT = 20000

# Product progress gain & losses

START_PRODUCT = 0
HIRE_DEV_GAIN = 10
OVERTIME_PRODUCT_GAIN = 5
DEV_QUIT_PENALTY = 10
INVESTOR_VISIT_PROGRESS_THRESHOLD = 30

# Morale changes
START_MORALE = 100
PITCH_MORALE_CHANGE = 10
OVERTIME_MORALE_PENALTY = 20
MEETUP_BOOST = 10
INVESTOR_VISIT_MORALE_CHANGE = 5
MORALE_RECOVERY_AMOUNT = 3
MORALE_RECOVERY_INTERVAL = 4 #in weeks

# Investor confidence changes

START_CONFIDENCE = 100
PITCH_CONFIDENCE_GAIN = 10
NEWSLETTER_CONFIDENCE_BOOST = 15
INVESTOR_VISIT_CONFIDENCE_CHANCE = 5
LOW_CASH_PENALTY = 10

# Win or loss conditions

MAX_PRODUCT_PROGRESS = 100
MAX_MORALE = 100
MAX_CONFIDENCE = 100
WIN_CONFIDENCE_THRESHOLD = 70
MIN_MORALE = 0
MIN_CASH = 0

# Random event

RANDOM_EVENT_CHANCE = 0.40 #probability of triggering a random event

# Other variables
START_WEEK = 1

# ------------- Setup & Constants, End -------------


# ------------- Game Flow, Start -------------


def main():
   global startup_name # Declare startup_name as a global variable so it can be accessed across functions
   print("""
Startup Survival Simulator
--------------------------

A turn-based terminal game where the player acts as the founder of a tech startup. 
Each week, players must choose between strategic options—such as hiring developers, pitching to investors, or pushing the team for overtime—while managing limited cash, team morale, product progress, and investor confidence.

The objective is to successfully launch a minimum viable product (MVP) and maintain investor confidence before the startup runs out of resources.

This game was developed as the final project for Code in Place 2025.
""")
   startup_name = get_startup_name()
   print(f"Let's see if {startup_name} can survive the grind! \n")
   game_loop()
   game_summary()

# Dictionary to track key startup stats

startup = {
    "cash" : START_CASH,         #How much money the startup has
    "morale" : START_MORALE,          #How happy and motivated your team is
    "product" : START_PRODUCT,           #How close you are to MVP
    "week" : START_WEEK              #Which week you are on in the simulation
}

# Dictionary to track investor stat(s)
investor = {
    "confidence" : START_CONFIDENCE     #How much trust the investor has in your startup
}


def game_loop():

# Main game loop that executes weekly player choices, events, and check game status

    while True:
        story_block()
        choice = get_player_choice()
        apply_choice(choice)
        trigger_random_event()
        cash_reserve_check()
        morale_recovery(choice)
        cap_stats()
        startup['week'] += 1
    
        if check_game_end():
            break

def check_game_end():

# Check if the game is ending or should continue

    if startup['cash'] <= MIN_CASH:
        print(f"\n{startup_name} ran out of cash. Game over!")
        return True
    
    if startup['morale'] <= MIN_MORALE:
        print(f"\nYour team at {startup_name} burned out. Game over!")
        return True
    
    if startup['product'] >= MAX_PRODUCT_PROGRESS and investor['confidence'] >= WIN_CONFIDENCE_THRESHOLD:
        print(f"\n{startup_name} launched its MVP and secured investor support. You win!")
        return True
    return False # Game continues

def game_summary():

# Summarize performance and final outcome

    print(f"\nFINAL STATS for : {startup_name}")
    print(f"Weeks survived: {startup['week']}")
    print(f"Cash: ${startup['cash']:,}")
    print(f"Product Progress: {startup['product']}%")
    print(f"Team Morale: {startup['morale']}")
    print(f"Investor Confidence: {investor['confidence']}%")

# ------------- Game Flow, End -------------


# ------------- Player Interaction, Start -------------

def get_startup_name():

# Allow player to pick a name for the startup. If the name is empty, ask again.

    while True:
        startup_name = input("\nWhat is the name of your startup?: ")
        if startup_name:
            return startup_name
        else:
            print("Startup name cannot be empty. Please try again.")

def get_player_choice():

# Display all the player choices for each week

    print("\nChoose your strategy this week:")
    print(f"1. Hire a Developer (-${HIRE_DEV_COST:,}, +{HIRE_DEV_GAIN}% Product)")
    print(f"2. Pitch to Investors (+{PITCH_CONFIDENCE_GAIN}% Confidence, -{PITCH_MORALE_CHANGE} Morale)")
    print(f"3. Push Team Overtime (+{OVERTIME_PRODUCT_GAIN}% Product, -{OVERTIME_MORALE_PENALTY} Morale)")

    # Ensure you get a valid choice before moving to next step. If not, ask player to re-enter their choice
    valid_choices = ["1", "2", "3"]

    while True:
        choice = input("Enter Option 1, 2, or 3: ")
        if choice in valid_choices:
            return choice
        else:
            print("Invalid input. Please enter 1, 2, or 3")

def story_block():

# Display current stats

    print(f"\n---WEEK {startup['week']}--- | {startup_name}")
    print(f"Cash: ${startup['cash']:,}")
    print(f"Morale: {startup['morale']}")
    print(f"Product Progress: {startup['product']}%")
    print(f"Investor Confidence: {investor['confidence']}%")
            

# ------------- Player Interaction, End -------------

# ------------- Game Mechanics, Start -------------

def apply_choice(choice):

# Apply the effects of the player's weekly decision

    if choice == "1":
        startup['cash'] -= HIRE_DEV_COST
        startup['product'] += HIRE_DEV_GAIN
        print(f"\n{startup_name} hired a developer. Product progress increased!")
    elif choice == "2":
        investor['confidence'] += PITCH_CONFIDENCE_GAIN
        startup['morale'] -= PITCH_MORALE_CHANGE
        print("\nYou pitched to investors. Confidence increased, but your team is stressed.")
    elif choice == "3":
        startup['product'] += OVERTIME_PRODUCT_GAIN
        startup['morale'] -= OVERTIME_MORALE_PENALTY
        print("\nYou pushed for overtime. Progress improved, but morale dropped.")

def morale_recovery(choice):

# Allow the player to slowly gain some morale over time. However you can not gain morale when you select to overwork the team

    if startup['week'] % MORALE_RECOVERY_INTERVAL == 0 and choice != "3":
        startup['morale'] += MORALE_RECOVERY_AMOUNT
        print("Your team had a balanced week and regained some morale")

def cap_stats():

# Ensure no stat exceeds its maximum. If it exceeds, bring it back to maximum.

    if startup['morale'] > MAX_MORALE:
        startup['morale'] = MAX_MORALE
    if startup['product'] > MAX_PRODUCT_PROGRESS:
        startup['product'] = MAX_PRODUCT_PROGRESS
    if investor['confidence'] > MAX_CONFIDENCE:
        investor['confidence'] = MAX_CONFIDENCE

def cash_reserve_check():
# Check if cash is below warning threshold and penalize confidence
    if startup['cash'] < LOW_CASH_WARNING:
        print(f"Cash reserves are dangerously low. Confidence -{LOW_CASH_PENALTY}%")
        investor['confidence'] -= LOW_CASH_PENALTY

def trigger_random_event():
# Trigger random events to escalate the game
# No random event in this week if the random number generated is greater than the event probability identified.
    if random.random() > RANDOM_EVENT_CHANCE:
        return #no event this week

    # Roll and execute one of several random events
    event_roll = random.randint(1, 6)

    if event_roll == 1:
    # Random event 1, a developer quits
        print(f"{startup_name}'s developer quit for a competitor. Product progress -{DEV_QUIT_PENALTY}%")
        startup['product'] -= DEV_QUIT_PENALTY

    elif event_roll == 2:
    # Random event 2, startup is featured in a newsletter
        print(f"{startup_name} got featured in a major newsletter! Investor confidence +{NEWSLETTER_CONFIDENCE_BOOST}%")
        investor['confidence'] += NEWSLETTER_CONFIDENCE_BOOST
    
    elif event_roll == 3:
    # Random event 3, a business emergency drains cash
        print(f"Unexpected business emergency at {startup_name}! You had to spend ${EMERGENCY_REPAIR:,} to keep things running.")
        startup['cash'] -= EMERGENCY_REPAIR
    
    elif event_roll == 4:
    # Random event 4, team member spoke at a meetup
        print(f"A team member spoke at a local meetup. Morale +{MEETUP_BOOST}")
        startup['morale'] += MEETUP_BOOST
    
    elif event_roll == 5:
    # Random event 5, a past investor visits
        if startup['product'] >= INVESTOR_VISIT_PROGRESS_THRESHOLD:
        # If the investor is impressed, you see positive stats
            print(f"A past investor made a surprise check-in. They are impressed! Confidence +{INVESTOR_VISIT_CONFIDENCE_CHANCE}% and Morale +{INVESTOR_VISIT_MORALE_CHANGE}% ")
            investor['confidence'] += INVESTOR_VISIT_CONFIDENCE_CHANCE
            startup['morale'] += INVESTOR_VISIT_MORALE_CHANGE
        else:
        # If the investor is not impressed, you see negative stats
            print(f"A past investor made a surprise check-in. They are disappointed by the lack of progress! Confidence -{INVESTOR_VISIT_CONFIDENCE_CHANCE}% and Morale -{INVESTOR_VISIT_MORALE_CHANGE}% ")
            investor['confidence'] -= INVESTOR_VISIT_CONFIDENCE_CHANCE
            startup['morale'] -= INVESTOR_VISIT_MORALE_CHANGE
    elif event_roll == 6:
    # Random event 6, startup gets a grant
        print(f"{startup_name} won a competitive startup grant. +${GRANT:,} in funding")
        startup['cash']  += GRANT

# ------------- Game Mechanics, End -------------


# ------------- Execution, Start -------------

if __name__ == "__main__":
    main()

# ------------- Execution, End -------------
