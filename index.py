from flask import Flask, request, jsonify, render_template
from text_extracters import generate

app = Flask(__name__)
# Function to validate email
def email_valid(mail):
    print(mail)
    if " " in mail:
        print("space")
        return False
    if "@" not in mail:
        print("@")
        return False
    if "." not in mail:
        print(".")
        return False
    return True

# Function to validate phone number
def phone_valid(phone):
    import re
    if len(phone) != 10:
        return False
    # Only 0-9 digits should be there
    if not phone.isdigit():
        return False
    if re.match("^[0-9]*$", phone):
        return True

# Function to provide help messages
def help(area):
    if area == "name":
        return "Provide your full name. If getting an error, try giving the full name with spaces in between."
    if area == "email":
        return "Provide email id in proper format e.g., abcjnadbcj@gmail.com with no spaces in between."
    if area == "phone":
        return "Provide phone number in proper format e.g., 1234567890 with no spaces in between."
    if area == "position":
        return "Provide the role you are applying for, which should be the complete role name."
    if area == "experience":
        return "Provide the experience in years e.g., 2 years. If getting an error, try giving e.g., my experience is 2 years."
    if area == "exit":
        return "If you want to exit the chat, type exit."
    if area == "start":
        help_message = (
            "If you need assistance, you can provide your name, email, phone number, "
            "position you're applying for, and your experience in years. "
            "Type 'exit' to reset the form."
        )
        return help_message

# Predefined messages
t = "only give phone number no prefix or suffix"
s = "only give email id no prefix or suffix like 'EMAIL:'"
exp = "experience is"

# Dictionary to store user data
d = {
    "start": False,
    "name": "",
    "email": "",
    "phone": "",
    "position": "",
    "experience": "",
    "thankyou": ""
}

# Questions to ask the user
questions = {
    "name": "What's your name for the application?",
    "email": "What's your email address {}?".format(d["name"]),
    "phone": "What's your phone number {}?".format(d["name"]),
    "position": "What position are you applying for {}?".format(d["name"]),
    "experience": "What's your experience in years {}?".format(d["name"]),
    "thankyou": "Thank you for providing the information {}.".format(d["name"]),
}

@app.route('/')
def index():
    # Reset user data
    d["start"] = False
    d["name"] = ""
    d["email"] = ""
    d["phone"] = ""            
    d["position"] = ""
    d["experience"] = ""
    d["thankyou"] = ""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print(f"User Message: {user_message}")

    # Handle exit or reset commands
    if user_message.lower() in ["exit", "yes", "end", ""]:
        d["start"] = False
        d["name"] = ""
        d["email"] = ""
        d["phone"] = ""
        d["position"] = ""
        d["experience"] = ""
        d["thankyou"] = ""
        return jsonify({'response': 'exit'})

    # Start the conversation
    if d["start"] == False:
        d["start"] = True
        k = ''
        ka = ''
        kb = ''
        kc = ''
        hd = ''
        # Handle help command
        if user_message == "help":
            return jsonify({'response': help("start")})
        # Handle name input
        if d["name"] == "":
            k = generate.fetch(user_message, "name", "NAME_NOT_FOUND", "NAME")
        # Handle email input
        if d["email"] == "":
            ka = generate.fetch(user_message + s, "email", "Email_NOT_FOUND", "EMAIL")
            ka = ka.split(":")
            print(ka)
            # If email is not found, ask for email again
            if len(ka) > 1:
                ka = ka[1].strip()
            else:
                ka = ka[0].strip()
        # Handle phone input
        if d["phone"] == "":
            kb = generate.fetch(user_message + t, "phone", "PHONE_NUMBER_NOT_FOUND", "PHONE_NUMBER")
            kb.replace("PHONE_NUMBER: ", "")
            kb = kb.strip()
        if d["experience"] == "":
            hd = generate.fetch(user_message, "experience in months", "EXPERIENCE_NOT_FOUND", "EXPERIENCE")
        if k != "NAME_NOT_FOUND" and d["name"] == "":
            d["name"] = k
        if ka != "EMAIL_NOT_FOUND" and d["email"] == "" and email_valid(ka):
            d["email"] = ka
        if kb != "PHONE_NUMBER_NOT_FOUND" and d["phone"] == "" and phone_valid(kb):
            d["phone"] = kb
        if hd != "EXPERIENCE_NOT_FOUND" and d["experience"] == "":
            d["experience"] = hd
        questions = {
            "name": "What's your name for the application?",
            "email": "What's your email address {}?".format(d["name"]),
            "phone": "What's your phone number {}?".format(d["name"]),
            "position": "What position are you applying for {}?".format(d["name"]),
            "experience": "What's your experience in years {}?".format(d["name"]),
            "thankyou": "Thank you for providing the information {}.".format(d["name"]),
        }
        for i in d:
            if d[i] == "":
                return jsonify({'response': questions[i]})
        return jsonify({'response': "Thank you for providing the information {}. \n Do you want to exit? Press any button and send.".format(d["name"])})

    # Handle name input
    if d["name"] == "":
        if user_message == "help":
            return jsonify({'response': help("name")})
        k = generate.fetch(user_message, "name", "NAME_NOT_FOUND", "NAME")
        if d["email"] == "":
            ka = generate.fetch(user_message + s, "email", "EMAIL_NOT_FOUND", "EMAIL")
            ka = ka.split(" ")
            if len(ka) > 1:
                ka = ka[1].strip()
            else:
                ka = ka[0].strip()
        if d["phone"] == "":
            kb = generate.fetch(user_message + t, "phone", "PHONE_NUMBER_NOT_FOUND", "PHONE_NUMBER")
            kb = kb.replace("PHONE_NUMBER: ", "")
            kb = kb.strip()
        if d["experience"] == "":
            hd = generate.fetch(user_message, "experience in months", "EXPERIENCE_NOT_FOUND", "EXPERIENCE")
        if ka != "EMAIL_NOT_FOUND" and d["email"] == "" and email_valid(ka):
            d["email"] = ka
        if kb != "PHONE_NUMBER_NOT_FOUND" and d["phone"] == "" and phone_valid(kb):
            d["phone"] = kb
        if hd != "EXPERIENCE_NOT_FOUND" and d["experience"] == "":
            d["experience"] = hd
        if k == "NAME_NOT_FOUND":
            return jsonify({'response': "Name not found in the text. Please provide your name."})
        d["name"] = k
        questions = {
            "name": "What's your name for the application?",
            "email": "What's your email address {}?".format(d["name"]),
            "phone": "What's your phone number {}?".format(d["name"]),
            "position": "What position are you applying for {}?".format(d["name"]),
            "experience": "What's your experience in years {}?".format(d["name"]),
            "thankyou": "Thank you for providing the information {}.".format(d["name"]),
        }
        for i in d:
            if d[i] == "":
                return jsonify({'response': questions[i]})
        return jsonify({'response': "Thank you for providing the information {}. \n Do you want to exit? Press any button and send.".format(d["name"])})

    # Handle email input
    if d["email"] == "":
        if user_message == "help":
            return jsonify({'response': help("email")})
        k = generate.fetch(user_message + s, "email", "Email_NOT_FOUND", "EMAIL")
        k = k.split(" ")
        if len(k) > 1:
            k = k[1].strip()
        else:
            k = k[0].strip()
        print(k)
        if d["phone"] == "":
            kb = generate.fetch(user_message + t, "phone", "PHONE_NUMBER_NOT_FOUND", "PHONE_NUMBER")
            kb = kb.replace("PHONE_NUMBER: ", "")
            kb = kb.strip()
        if d["experience"] == "":
            hd = generate.fetch(user_message, "experience in months", "EXPERIENCE_NOT_FOUND", "EXPERIENCE")
        if kb != "PHONE_NUMBER_NOT_FOUND" and d["phone"] == "" and phone_valid(kb):
            d["phone"] = kb
        if hd != "EXPERIENCE_NOT_FOUND" and d["experience"] == "":
            d["experience"] = hd
        if k == "Email_NOT_FOUND":
            return jsonify({'response': "Email not found in the text. Please provide your email address properly."})
        print(email_valid(k))
        if not email_valid(k):
            return jsonify({'response': "Email not found in the text. Please provide your email address properly."})
        d["email"] = k
        questions = {
            "name": "What's your name for the application?",
            "email": "What's your email address {}?".format(d["name"]),
            "phone": "What's your phone number {}?".format(d["name"]),
            "position": "What position are you applying for {}?".format(d["name"]),
            "experience": "What's your experience in years {}?".format(d["name"]),
            "thankyou": "Thank you for providing the information {}.".format(d["name"]),
        }
        for i in d:
            if d[i] == "":
                return jsonify({'response': questions[i]})
        return jsonify({'response': "Thank you for providing the information {}. \n Do you want to exit? Press any button and send.".format(d["name"])})

    # Handle phone input
    if d["phone"] == "":
        if user_message == "help":
            return jsonify({'response': help("phone")})
        k = generate.fetch(user_message + t, "phone", "PHONE_NUMBER_NOT_FOUND", "PHONE_NUMBER")
        k = k.replace("PHONE_NUMBER: ", "")
        k = k.strip()
        if d["experience"] == "":
            hd = generate.fetch(user_message, "experience in months", "EXPERIENCE_NOT_FOUND", "EXPERIENCE")
        if hd != "EXPERIENCE_NOT_FOUND" and d["experience"] == "":
            d["experience"] = hd
        if k == "PHONE_NUMBER_NOT_FOUND":
            return jsonify({'response': "Phone number not found in the text. Please provide your phone number properly."})
        print(phone_valid(k))
        if not phone_valid(k):
            return jsonify({'response': "Phone number not found in the text. Please provide your phone number properly."})
        d["phone"] = k
        questions = {
            "name": "What's your name for the application?",
            "email": "What's your email address {}?".format(d["name"]),
            "phone": "What's your phone number {}?".format(d["name"]),
            "position": "What position are you applying for {}?".format(d["name"]),
            "experience": "What's your experience in years {}?".format(d["name"]),
            "thankyou": "Thank you for providing the information {}.".format(d["name"]),
        }
        for i in d:
            if d[i] == "":
                return jsonify({'response': questions[i]})
        return jsonify({'response': "Thank you for providing the information {}. \n Do you want to exit? Press any button and send.".format(d["name"])})

    # Handle position input
    if d["position"] == "":
        if user_message == "help":
            return jsonify({'response': help("position")})
        k = generate.fetch(user_message, "position", "ROLE_NOT_FOUND", "ROLE")
        if d["experience"] == "":
            hd = generate.fetch(user_message, "experience in months", "EXPERIENCE_NOT_FOUND", "EXPERIENCE")
        if hd != "EXPERIENCE_NOT_FOUND" and d["experience"] == "":
            d["experience"] = hd
        if k == "ROLE_NOT_FOUND":
            return jsonify({'response': "Role not found in the text. Please provide your role properly."})
        d["position"] = k
        questions = {
            "name": "What's your name for the application?",
            "email": "What's your email address {}?".format(d["name"]),
            "phone": "What's your phone number {}?".format(d["name"]),
            "position": "What position are you applying for {}?".format(d["name"]),
            "experience": "What's your experience in years {}?".format(d["name"]),
            "thankyou": "Thank you for providing the information {}.".format(d["name"]),
        }
        for i in d:
            if d[i] == "":
                return jsonify({'response': questions[i]})
        return jsonify({'response': "Thank you for providing the information {}. \n Do you want to exit? Press any button and send.".format(d["name"])})

    # Handle experience input
    if d["experience"] == "":
        if user_message == "help":
            return jsonify({'response': help("experience")})
        k = generate.fetch(exp + user_message, "experience in months", "EXPERIENCE_NOT_FOUND", "EXPERIENCE")
        if k == "EXPERIENCE_NOT_FOUND":
            return jsonify({'response': "Experience not found in the text. Please provide your experience properly."})
        d["experience"] = k
        questions = {
            "name": "What's your name for the application?",
            "email": "What's your email address {}?".format(d["name"]),
            "phone": "What's your phone number {}?".format(d["name"]),
            "position": "What position are you applying for {}?".format(d["name"]),
            "experience": "What's your experience in years {}?".format(d["name"]),
            "thankyou": "Thank you for providing the information {}.".format(d["name"]),
        }
        for i in d:
            if d[i] == "":
                return jsonify({'response': questions[i]})
        return jsonify({'response': "Thank you for providing the information {}. \n Do you want to exit? Press any button and send.".format(d["name"])})

    # Handle thank you message and reset conversation
    if d["thankyou"] == '':
        if user_message == "help":
            return jsonify({'response': help("exit")})
        d["start"] = False
        d["name"] = ""
        d["email"] = ""
        d["phone"] = ""
        d["position"] = ""
        d["experience"] = ""
        d["thankyou"] = ""
        return jsonify({'response': 'exit'})

if __name__ == '__main__':
    app.run(debug=True)