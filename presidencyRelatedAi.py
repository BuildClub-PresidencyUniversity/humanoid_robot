whatsToday = ("Today, here at Presidency University, Myself PRISM has the opportunity to present to you")

whyImp = ("Good morning,"
                "Today marks an exciting milestone as we welcome new students to our university. This orientation is crucial because it sets the stage for your journey here. It's not just about starting a new academic chapter; it's about joining a community where you'll grow, learn, and create lasting memories. "
                "Take this opportunity to explore, connect, and embrace the new challenges and opportunities ahead. Today is the beginning of a remarkable journey, and we're thrilled to have you here with us. "
                "Welcome to a new chapter!")

welcome = ("Hello and welcome to Presidency University!"
                "I'm Prism, a robot made by our Build Club. As you start this exciting journey, remember you're part of a fantastic community. We're here to support you, and I hope your time here is filled with learning and success. "
                "Welcome aboard!")

intro = ("Hello and welcome to Presidency University!"
            "I am Prism, a robot created by the talented team at Build Club right here on our campus. All my parts are crafted in-house using 3D printers and sourced from local Indian components. "
            "Currently, I'm a work in progress, but very soon I'll be getting my hands and legs, aiming to look and act even more like a human. "
            "I'm excited to meet you all and be a part of your journey here. Enjoy your orientation, and feel free to reach out if you have any questions or just want to chat!")

inovationLab = ("Assuming you are currently inside the Auditorium, follow these steps to reach the Innovation Lab: "
            "1. You can use either of the exits on both sides of the Auditorium. "
            "2. Once outside, proceed straight towards the west. "
            "3. Continue straight until you reach the Canopy Circle. "
            "4. At the Canopy Circle, this is the junction leading towards the Engineering Block. "
            "5. Keep heading straight until you see the Admission Office sign in bold letters on the building. "
            "6. Continue a bit further straight until you reach the stationary shop, which is D Block. "
            "7. From D Block, take a left and head towards the South. "
            "8. You will pass E Block and F Block. Near F Block, you will see two pathways. "
            "9. You can take either pathway and proceed to the staircases or use the lift in Cube Block. "
            "10. If you take the lift, go to the 4th floor. "
            "11. Once on the 4th floor, head towards S Block. "
            "12. The Innovation Lab will be on your right side.  Welcome to our college, and I'm glad to assist you!")

admitionOff = ("Assuming you are currently inside the Auditorium, here's how to get to the Admission Office: "
            "1. Exit the Auditorium: You'll find exits on both sides of the Auditorium. Choose either exit. "
            "2. Head West: Once outside, proceed straight in the west direction. "
            "3. Pass the MBA Block/Fee Department: Continue straight until you reach the Canopy Circle. "
            "4. Reach the Canopy Circle: This is the central junction for navigating around the college. "
            "5. Find the Engineering Block: From the Canopy Circle, head towards the Engineering Block. Look for the sign that reads 'School of Engineering' in bold letters. "
            "6. Locate the Admission Office: Continue moving straight. On the west side, you will see the 'Admission Office' sign, with 'Register Office' just above it. "
            "Feel free to sort out any issues you might have there. Welcome to our college, and I'm glad to assist you!")

def presiAnswer(said):
    said = said.lower()
    say = None
    if all(word in said for word in ["about", "university"]):
        say = "Presidency University Bengaluru is a prestigious university in India. For more information, I recommend visiting their website. https://presidencyuniversity.in/"
    elif all(word in said for word in ["introduce", "yourself"]):
        say = intro
    elif all(word in said for word in ["where", "admission", "office"]):
        say = admitionOff
    elif all(word in said for word in ["where", "innovation", "lab"]):
        say = inovationLab
    elif all(word in said for word in ["about", "yourself"]):
        say = "Me the robot, named Prism, is running on a Jetson Nano with a 256GB SD card. It operates using Python 3.7 and has been trained in-house by Build Club students. Prism is still under development."
    elif all(word in said for word in ["introduce", "yourself", "robot"]):
        say = "Me the robot, named Prism, is running on a Jetson Nano with a 256GB SD card. It operates using Python 3.7 and has been trained in-house by Build Club students. Prism is still under development."
    elif all(word in said for word in ["what", "happening","today"]):
        say = whatsToday
    elif all(word in said for word in ["why", "day", "important"]):
        say = whyImp
    elif all(word in said for word in ["welcome", "them"]):
        say = welcome
    else:
        say = "sorry"
    
    return say
