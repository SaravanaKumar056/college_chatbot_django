import requests
from textblob import TextBlob
import time
import re

def normalize_input(user_input):
    return re.sub(r'[^\w\s]', '', user_input.lower().strip())

def correct_spelling(user_input):
    keywords_to_protect = ["saravana", "kumar", "hindustan", "hicas", "kalaiyarkovil"]

    # Split sentence into words and only correct words not in keywords
    corrected_words = []
    for word in user_input.split():
        if word.lower() in keywords_to_protect:
            corrected_words.append(word)
        else:
            corrected_words.append(str(TextBlob(word).correct()))
    return " ".join(corrected_words)


API_TOKEN = os.getenv("HF_TOKEN ")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def query_mistral(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "stop": ["You:"]
        }
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()  # Assuming the response is JSON, extract the text
    except requests.exceptions.Timeout:
        return "⚠️ The AI model took too long to respond. Please try again."
    except requests.exceptions.RequestException as e:
        return f" API Request failed: {e}"
    except Exception as e:  # Catch any other exception and return None
        print(f"An error occured in query_mistral: {e}")  # Print this for debugging
        return None  # Return None if there was a error.

# College info & owner response
college_info = """
Hindustan College of Arts and Science (HCAS), located in Coimbatore, Tamil Nadu, offers a wide range of undergraduate and postgraduate programs.

Departments include:
- B.Sc. Artificial Intelligence and Machine Learning
- B.Com Accounting and Finance
- BCA, BBA, B.Sc. Computer Science, and more

Facilities:
- Library, Smart Classrooms, Computer Labs, Auditorium, Cafeteria, Hostel, Sports Ground

The college is affiliated with Bharathiar University.
Visit: https://www.hicas.ac.in/
"""

college_data = {
    "hindustan": {
        "name": "Hindustan College of Arts and Science",
        "location": "Coimbatore, Tamil Nadu",
        "timing": "9:00 AM to 3:45 PM",
        "departments": [
            "B.Sc. AI & ML", "B.Com Accounting and Finance", "BCA", "BBA", "B.Sc. Computer Science", "B.A. English"
        ],
        "facilities": [
            "Smart Classrooms", "Computer Labs", "Auditorium", "Library", "Cafeteria", "Hostel", "Sports Ground"
        ],
        "website": "https://www.hicas.ac.in/"
    },
    "psg": {
        "name": "PSG College of Arts and Science",
        "location": "Coimbatore, Tamil Nadu",
        "timing": "8:30 AM to 1:30 PM",
        "departments": [
            "B.Com", "BBA", "B.Sc. Computer Science", "BCA", "B.A. English", "M.Com", "M.Sc. IT"
        ],
        "facilities": [
            "Library", "Computer Labs", "Auditorium", "Canteen", "Hostel", "WiFi Campus"
        ],
        "website": "https://www.psgcas.ac.in/"
    },
    "psg tech": {
        "name": "PSG College of Technology",
        "location": "Coimbatore, Tamil Nadu",
        "timing": "8:00 AM to 4:30 PM",
        "departments": [
            "Mechanical Engg", "CSE", "EEE", "ECE", "Civil Engg", "IT", "AI & DS", "Mechatronics"
        ],
        "facilities": [
            "Labs", "Innovation Centre", "Library", "WiFi", "Hostel", "Playgrounds", "Cafeteria"
        ],
        "website": "https://www.psgtech.edu/"
    }
}


owner_response = """
I was created by Saravana Kumar, a student of B.Sc. AI & ML at Hindustan College of Arts and Science, Coimbatore.
He is from Kalaiyarkovil, Sivagangai district, Tamil Nadu, and currently studying in his 2nd year.
"""

print("Chat with your college chatbot (Mistral-7B). Type 'exit' to stop.\n")

def manual_response(corrected_input):
    input_lower = normalize_input(corrected_input.lower().strip())
    print(f"[DEBUG] Normalized input: '{input_lower}'")

    if input_lower in ["hindustan", "hicas", "hindustan college", "hicas college"]:
        return "Hindustan College of Arts and Science is located in Coimbatore, Tamil Nadu. Visit: https://www.hicas.ac.in/"

    if input_lower.strip() == "saravana kumar":
        return "Saravana Kumar is a student of B.Sc. AI & ML at HICAS, known for building this chatbot assistant."

    # Normalize input for college name
    if "hicas" in input_lower:
        input_lower = input_lower.replace("hicas", "hindustan")
    elif "hindustan college" in input_lower:
        input_lower = input_lower.replace("hindustan college", "hindustan")

    if "who is saravana kumar" in input_lower:
        return """Saravana Kumar is a B.Sc. Artificial Intelligence and Machine Learning student at Hindustan College of Arts and Science, Coimbatore. He is originally from Kalaiyarkovil, Sivagangai district, Tamil Nadu, and currently in his second year. Saravana is passionate about AI development and dreams of becoming a successful AI engineer."""

    if "who is saravana" in input_lower:
        return """Saravana is a short name for Saravana Kumar, a 2nd-year student of B.Sc. AI & ML at Hindustan College of Arts and Science, Coimbatore. He is from Kalaiyarkovil and is known for his interest in Artificial Intelligence and Machine Learning."""

    if "college timing" in input_lower or "college time" in input_lower or "when does college start" in input_lower:
        return """The college timing at Hindustan College of Arts and Science (HCAS), Coimbatore, usually starts at 9:00 AM and ends around 3:30 PM. Timings may vary slightly depending on department and schedule."""

    if "admission" in input_lower or "how to join" in input_lower:
        return "For admissions, please visit the official site or contact the college directly at https://www.hicas.ac.in/contact-us/"

    if "principal" in input_lower or "head of the college" in input_lower:
        return "The principal of HICAS is Dr. (Name). For more info, refer to the college website."

    department_keywords = ["departments", "courses", "branches"]
    if any(word in input_lower for word in department_keywords):
        return """HCAS offers a variety of departments including:
- B.Sc. AI & ML
- B.Sc. Computer Science
- B.Com Accounting and Finance
- BCA, BBA, B.A English, and more."""

    if "facilities" in input_lower or "what are the facilities" in input_lower:
        return """HCAS provides a range of facilities such as:
- Smart Classrooms
- Computer Labs
- Auditorium
- Library
- Cafeteria
- Hostel
- Sports Ground"""

    if "owner" in input_lower or "creator" in input_lower:
        return """I was created by Saravana Kumar, a student of B.Sc. AI & ML at Hindustan College of Arts and Science. He built me to assist students and provide information about the college and other topics."""

    if "who are you" in input_lower:
        return "I am your AI chatbot assistant created by Saravana Kumar to help students with college and general information."

    if input_lower in ["hi", "hello", "help"]:
        return "Hi! I can help with college info like timing, website, departments, and facilities. Just ask me!"

    if "where is hindustan" in input_lower or "location of hindustan" in input_lower or "where is hicas" in input_lower or "location of hicas" in input_lower:
        return "Hindustan College of Arts and Science is located in Coimbatore, Tamil Nadu."

    # Main college_data handling loop
    for college_key in college_data:
        if college_key in input_lower:
            if "timing" in input_lower or "time" in input_lower:
                return get_college_info(college_key, "timing")
            elif "department" in input_lower or "course" in input_lower:
                return get_college_info(college_key, "departments")
            elif "facilities" in input_lower or "facility" in input_lower:
                return get_college_info(college_key, "facilities")
            elif "website" in input_lower:
                return get_college_info(college_key, "website")
            else:
                return "I don't have info on that. Try asking about timing, website, or departments."

    return None


def get_college_info(college_key, info_type):
    college = college_data.get(college_key)
    if not college:
        return None

    if info_type == "timing":
        return f"{college['name']} usually operates from {college['timing']}."

    if info_type == "departments":
        return f"{college['name']} offers departments like:\n- " + "\n- ".join(college["departments"])

    if info_type == "facilities":
        return f"{college['name']} provides facilities such as:\n- " + "\n- ".join(college["facilities"])

    if info_type == "website":
        return f"You can visit {college['name']}'s official website here: {college['website']}"

    return None

def chatbot_reply(user_input):
    # Step 1: Normalize and correct user input
    corrected_input = correct_spelling(user_input)

    # Step 2: Try to find a manual response
    manual = manual_response(corrected_input)
    if manual:  # ✅ If manual response is found, return it
        return manual

    # Step 3: If nothing matched, fallback to Mistral API
    return query_mistral(corrected_input)


    # 🔁 If nothing matches, return fallback
    #return "I don't have info on that. Try asking about timing, website, or departments."

    # Fallback to LLM response
    # Corrected
import time

def get_bot_reply(corrected_input):
    prompt = f"You: {corrected_input}\nAI:"
    result = query_mistral(prompt)

    if isinstance(result, dict) and "generated_text" in result:
        bot_reply = result["generated_text"]
    elif isinstance(result, list) and "generated_text" in result[0]:
        bot_reply = result[0]["generated_text"]
    else:
        bot_reply = "🤖 Sorry, I couldn’t understand that. Try rephrasing your question."

    print(f"(Corrected input: {corrected_input})")  # Helpful debug log

    if bot_reply:
        for char in bot_reply:
            print(char, end='', flush=True)
            time.sleep(0.01)
    else:
        print("⚠️ Could not get a reply from the model.")

    print()  # Newline after response
    return bot_reply


chat_history = " chat_history.txt"

