import streamlit as st
import random
import os

# Set up Page Config
st.set_page_config(page_title="Word Scramble & Hangman Arena", page_icon="🎮", layout="centered")

# ==========================================
# 1. FILE PARSING & DATA LOADING
# ==========================================

def load_words_from_file(file_path="words.txt"):
    """Reads categories and words from words.txt."""
    if not os.path.exists(file_path):
        default_data = [
            "Tech: python\n", "Tech: algorithm\n", "Tech: developer\n", "Tech: database\n",
            "Cities: tokyo\n", "Cities: paris\n", "Cities: melbourne\n", "Cities: cairo\n",
            "Sports: basketball\n", "Sports: swimming\n", "Sports: archery\n", "Sports: football\n"
        ]
        with open(file_path, "w") as f:
            f.writelines(default_data)

    word_bank = {}
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line and ":" in line:
                category, word = line.split(":", 1)
                category = category.strip().title()
                word = word.strip().lower()
                if category not in word_bank:
                    word_bank[category] = []
                word_bank[category].append(word)

    return word_bank

def scramble_word(word):
    """Scrambles a word using list rotation and slicing."""
    chars = list(word)
    n = len(chars)
    shift = random.randint(1, max(1, n - 1))
    rotated = chars[shift:] + chars[:shift]
    random.shuffle(rotated)
    scrambled = "".join(rotated)
    if scrambled == word and n > 1:
        scrambled = word[::-1]
    return scrambled

# Load words
word_bank = load_words_from_file()

# ==========================================
# 2. SESSION STATE MANAGEMENT
# ==========================================

def start_new_game():
    category = random.choice(list(word_bank.keys()))
    word = random.choice(word_bank[category])
    
    st.session_state.category = category
    st.session_state.word = word
    st.session_state.scrambled = scramble_word(word)
    st.session_state.guessed_letters = set()
    st.session_state.incorrect_guesses = 0
    st.session_state.scramble_attempts = 3
    st.session_state.game_over = False
    st.session_state.win = False

if 'word' not in st.session_state:
    start_new_game()

# ==========================================
# 3. UI LAYOUT & GAME LOGIC
# ==========================================

st.title("🎮 Word Scramble & Hangman Arena")
st.caption("Powered by Python, String Manipulation & Set Operations")

# Main Page Controls (Dropdown / Selectbox & Restart Button)
col_ctrl1, col_ctrl2 = st.columns([2, 1])
with col_ctrl1:
    mode = st.selectbox("Select Game Mode", ["Word Scramble", "Hangman"])
with col_ctrl2:
    st.write("") # Spacing alignment
    st.write("")
    if st.button("🔄 New Word / Restart"):
        start_new_game()
        st.rerun()

st.markdown("---")
st.write(f"**Current Category:** `{st.session_state.category}`")

# ------------------------------------------
# MODE 1: WORD SCRAMBLE
# ------------------------------------------
if mode == "Word Scramble":
    st.subheader(f"Category: {st.session_state.category}")
    st.info(f"**Scrambled Word:** `{st.session_state.scrambled.upper()}`")
    st.write(f"Attempts remaining: **{st.session_state.scramble_attempts}**")

    if not st.session_state.game_over:
        guess = st.text_input("Enter your full word guess:", key="scramble_input").strip().lower()
        
        if st.button("Submit Guess"):
            if guess == st.session_state.word:
                st.session_state.win = True
                st.session_state.game_over = True
            else:
                st.session_state.scramble_attempts -= 1
                if st.session_state.scramble_attempts <= 0:
                    st.session_state.game_over = True
                else:
                    st.error("Incorrect guess! Try again.")
            st.rerun()

    if st.session_state.game_over:
        if st.session_state.win:
            st.balloons()
            st.success(f"🎉 Correct! The word was **{st.session_state.word.upper()}**.")
        else:
            st.error(f"💀 Game Over! The word was **{st.session_state.word.upper()}**.")

# ------------------------------------------
# MODE 2: HANGMAN
# ------------------------------------------
elif mode == "Hangman":
    st.subheader(f"Category: {st.session_state.category}")
    
    # Reveal word state
    display_word = [letter.upper() if letter in st.session_state.guessed_letters else "_" for letter in st.session_state.word]
    st.markdown(f"### Word:  {' '.join(display_word)}")

    # Set operations for available letters
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    remaining_alphabet = alphabet - st.session_state.guessed_letters
    max_incorrect = 6

    st.write(f"**Incorrect Guesses Left:** {max_incorrect - st.session_state.incorrect_guesses} / {max_incorrect}")
    st.write(f"**Guessed Letters:** `{' '.join(sorted(list(st.session_state.guessed_letters))).upper()}`")

    if not st.session_state.game_over:
        col1, col2 = st.columns([3, 1])
        with col1:
            letter_guess = st.text_input("Guess a letter:", max_chars=1, key="hangman_input").strip().lower()
        
        if st.button("Guess Letter") and letter_guess:
            if letter_guess in st.session_state.guessed_letters:
                st.warning(f"You already guessed '{letter_guess.upper()}'.")
            elif letter_guess not in alphabet:
                st.warning("Please enter a valid single letter (a-z).")
            else:
                st.session_state.guessed_letters.add(letter_guess)
                if letter_guess not in set(st.session_state.word):
                    st.session_state.incorrect_guesses += 1
                
                # Check Win condition
                if set(st.session_state.word).issubset(st.session_state.guessed_letters):
                    st.session_state.win = True
                    st.session_state.game_over = True
                
                # Check Lose condition
                if st.session_state.incorrect_guesses >= max_incorrect:
                    st.session_state.game_over = True
            st.rerun()

    if st.session_state.game_over:
        if st.session_state.win:
            st.balloons()
            st.success(f"🎉 You guessed it! The word was **{st.session_state.word.upper()}**.")
        else:
            st.error(f"💀 Game Over! The word was **{st.session_state.word.upper()}**.")
