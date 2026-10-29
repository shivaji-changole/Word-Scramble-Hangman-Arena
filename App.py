import streamlit as st
import random
import os

st.set_page_config(page_title="Word Scramble & Hangman", page_icon="🎮")

# ==========================================
# 1. DATA LOADING & FILE HANDLING
# ==========================================
def load_words(file_path="words.txt"):
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
        for line in f:
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
    chars = list(word)
    n = len(chars)
    shift = random.randint(1, max(1, n - 1))
    rotated = chars[shift:] + chars[:shift]
    random.shuffle(rotated)
    scrambled = "".join(rotated)
    if scrambled == word and n > 1:
        scrambled = word[::-1]
    return scrambled

word_bank = load_words()

# ==========================================
# 2. SESSION STATE
# ==========================================
def reset_game():
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
    reset_game()

# ==========================================
# 3. UI & GAME PLAY
# ==========================================
st.title("Word Scramble & Hangman")

# Simple dropdown and button stacked vertically
mode = st.selectbox("Select Mode", ["Word Scramble", "Hangman"])

if st.button("New Game / Reset"):
    reset_game()
    st.rerun()

st.write(f"**Category:** {st.session_state.category}")
st.divider()

# --- WORD SCRAMBLE ---
if mode == "Word Scramble":
    st.write(f"**Scrambled Word:** `{st.session_state.scrambled.upper()}`")
    st.write(f"Attempts left: {st.session_state.scramble_attempts}")

    if not st.session_state.game_over:
        guess = st.text_input("Your guess:", key="scramble_guess").strip().lower()
        if st.button("Submit Guess"):
            if guess == st.session_state.word:
                st.session_state.win = True
                st.session_state.game_over = True
            else:
                st.session_state.scramble_attempts -= 1
                if st.session_state.scramble_attempts <= 0:
                    st.session_state.game_over = True
                else:
                    st.warning("Incorrect! Try again.")
            st.rerun()

    if st.session_state.game_over:
        if st.session_state.win:
            st.success(f"Correct! The word was {st.session_state.word.upper()}.")
        else:
            st.error(f"Game Over! The word was {st.session_state.word.upper()}.")

# --- HANGMAN ---
elif mode == "Hangman":
    display_word = [l.upper() if l in st.session_state.guessed_letters else "_" for l in st.session_state.word]
    st.write(f"**Word:** {' '.join(display_word)}")
    st.write(f"Incorrect guesses left: {6 - st.session_state.incorrect_guesses} / 6")
    
    guessed_list = sorted(list(st.session_state.guessed_letters))
    st.write(f"Guessed letters: {', '.join(guessed_list).upper() if guessed_list else 'None'}")

    alphabet = set("abcdefghijklmnopqrstuvwxyz")

    if not st.session_state.game_over:
        letter_guess = st.text_input("Guess a letter:", max_chars=1, key="hangman_guess").strip().lower()
        if st.button("Submit Letter") and letter_guess:
            if letter_guess in st.session_state.guessed_letters:
                st.warning("You already guessed that letter.")
            elif letter_guess not in alphabet:
                st.warning("Enter a valid letter (a-z).")
            else:
                st.session_state.guessed_letters.add(letter_guess)
                if letter_guess not in set(st.session_state.word):
                    st.session_state.incorrect_guesses += 1
                
                if set(st.session_state.word).issubset(st.session_state.guessed_letters):
                    st.session_state.win = True
                    st.session_state.game_over = True
                elif st.session_state.incorrect_guesses >= 6:
                    st.session_state.game_over = True
            st.rerun()

    if st.session_state.game_over:
        if st.session_state.win:
            st.success(f"You won! The word was {st.session_state.word.upper()}.")
        else:
            st.error(f"Game Over! The word was {st.session_state.word.upper()}.")
