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

inovationLab = (
            "Here's a clear and concise response for directing you to the Innovation Lab: "
            "Certainly! Assuming you're currently in Conference Room Besh, here's how you can get to the Innovation Lab: "
            "1. Exit the Conference Room and take a left. "
            "2. From there, you can choose to go either downside or upside (whichever is more convenient). "
            "3. Continue straight and then take a short left followed by a short right. "
            "4. You will reach Q Block. On your left side, you'll see the lift. "
            "5. Enter the lift and press the button for the 4th floor. "
            "6. Once on the 4th floor, head towards South Block. "
            "7. Go straight, and you will find the Innovation Lab on your right side. "
            "If you need further assistance, feel free to ask!")

admitionOff = ("To reach the Admission Office from the Conference Room: "
                "1. Exit the Conference Room and take a right. "
                "2. Continue straight until you see a stationery shop; this is D Block. "
                "3. A little further, on your left-hand side, you will see a lift. You can take the lift or use the stairs. "
                "4. Go to the first floor. "
                "5. Once on the first floor, take a right and then a left. "
                "6. You will see a series of chairs for visitors' comfort—that's the Admission Office. "
                "Feel free to go there to clarify any doubts you may have!")

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
