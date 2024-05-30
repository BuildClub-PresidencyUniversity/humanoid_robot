def presiAnswer(said):
    said = said.lower()
    say = None
    if all(word in said for word in ["about", "university"]):
        say = "Presidency University Bengaluru is a prestigious university in India. For more information, I recommend visiting their website. https://presidencyuniversity.in/"
    elif all(word in said for word in ["where", "d", "block"]):
        say = "Assuming you're currently in the P Block Basement Floor (PB), you'll need to take the stairs to the First Floor. Once there, head left towards Blocks F and E. You'll find a stationary shop near your destination."
    elif all(word in said for word in ["where", "admission", "office"]):
        say = "Assuming you're currently in the P Block Basement Floor (PB), you'll need to take the stairs to the First Floor. Once there, head left towards Blocks F and E. You'll find a stationary shop near your destination."
    elif all(word in said for word in ["where", "qt", "block"]):
        say = "Assuming you're currently in the P Block Basement Floor (PB), take the lift to your right. Press the button for the 3rd floor. Once you arrive, turn slightly left and walk straight. Keep an eye on the block labels above to find QT Block."
    elif all(word in said for word in ["about", "yourself"]):
        say = "Me the robot, named Candy, is running on a Jetson Nano with a 256GB SD card. It operates using Python 3.7 and has been trained in-house by Build Club students. Candy is still under development."
    elif all(word in said for word in ["introduce", "yourself"]):
        say = "Me the robot, named Candy, is running on a Jetson Nano with a 256GB SD card. It operates using Python 3.7 and has been trained in-house by Build Club students. Candy is still under development."
    else:
        say = "sorry"
    
    return say
