import streamlit as st
import json
import os
from deep_translator import GoogleTranslator  # New translator

# Constants
USER_DATA = "progress_data.json"

# Load or create user progress data
def load_user_data():
    if os.path.exists(USER_DATA):
        with open(USER_DATA, "r") as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(USER_DATA, "w") as f:
        json.dump(data, f, indent=4)

# Translate text using deep-translator
def translate_text(text, lang):
    if lang == "English":
        return text
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text) if lang == "Tamil" else text
    except:
        return text  # fallback if translation fails

# Simulated AI suggestion logic
def suggest_content(level, interest):
    suggestions = {
        "Math": f"Try solving adaptive math problems at {level} level.",
        "Science": f"Explore AI-generated science simulations for {level} learners.",
        "History": f"Watch interactive history videos tailored to {level} learners."
    }
    return suggestions.get(interest, "Start with general knowledge quizzes!")

# Quiz questions
QUIZ = {
    "Math": {"Q": "What is 12 + 8?", "A": "20"},
    "Science": {"Q": "What planet is known as the Red Planet?", "A": "Mars"},
    "History": {"Q": "Who was the first president of India?", "A": "Dr. Rajendra Prasad"}
}

# Main App
def main():
    st.set_page_config(page_title="AI Learning App")
    st.title("🎓 AI-Powered Personalized Learning")

    user_data = load_user_data()

    name = st.text_input("Enter your name:")
    if not name:
        st.warning("Please enter your name.")
        return

    lang = st.selectbox("Choose your preferred language", ["English", "Tamil"])
    level = st.selectbox("Select your learning level", ["Beginner", "Intermediate", "Advanced"])
    interest = st.selectbox("What subject do you like?", ["Math", "Science", "History"])

    # Initialize user if new
    if name not in user_data:
        user_data[name] = {
            "language": lang,
            "level": level,
            "interest": interest,
            "score": 0,
            "badges": []
        }

    # Welcome Message
    st.success(translate_text(f"Welcome, {name}!", lang))

    # Content Suggestion
    st.subheader(translate_text("📘 Personalized Suggestion", lang))
    suggestion = suggest_content(level, interest)
    st.info(translate_text(suggestion, lang))

    # Quiz Section
    st.subheader(translate_text("🧠 Quick Quiz", lang))
    quiz = QUIZ[interest]
    q = translate_text(quiz["Q"], lang)
    answer = st.text_input(q)

    if st.button(translate_text("Submit", lang)):
        correct = quiz["A"].lower() == answer.strip().lower()
        if correct:
            user_data[name]["score"] += 10
            badge = f"{interest} Star"
            if badge not in user_data[name]["badges"]:
                user_data[name]["badges"].append(badge)
            st.success(translate_text("Correct! You've earned a badge!", lang))
        else:
            st.error(translate_text(f"Wrong. The correct answer is: {quiz['A']}", lang))
        save_user_data(user_data)

    # Progress Display
    st.subheader(translate_text("📈 Your Progress", lang))
    st.write(translate_text(f"Score: {user_data[name]['score']}", lang))
    st.write(translate_text(f"Badges: {', '.join(user_data[name]['badges']) or 'None'}", lang))

if __name__ == "__main__":
    main()
