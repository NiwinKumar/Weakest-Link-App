import streamlit as st
import random
import time
from datetime import datetime, timedelta
from streamlit.components.v1 import html

# First: Define all functions
def show_game_results():
    st.markdown("""
        <div style='
            padding: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        '>
            <h2 style='color: #FF4B4B;'>🎮 Game Over! 🎮</h2>
            <div style='margin: 20px 0;'>
                <h3 style='color: #00CC00;'>Game Statistics</h3>
                <table style='width: 100%; margin: 10px 0;'>
                    <tr>
                        <td style='text-align: left; padding: 5px;'>Total Questions:</td>
                        <td style='text-align: right; padding: 5px;'>{}</td>
                    </tr>
                    <tr>
                        <td style='text-align: left; padding: 5px;'>Correct Answers:</td>
                        <td style='text-align: right; padding: 5px;'>{}</td>
                    </tr>
                    <tr>
                        <td style='text-align: left; padding: 5px;'>Wrong Answers:</td>
                        <td style='text-align: right; padding: 5px;'>{}</td>
                    </tr>
                    <tr>
                        <td style='text-align: left; padding: 5px;'>Total Banks:</td>
                        <td style='text-align: right; padding: 5px;'>{}</td>
                    </tr>
                </table>
            </div>
            <h3 style='color: #1f77b4;'>Final Prize Money</h3>
            <h1 style='color: #00CC00; font-size: 48px;'>₹{}</h1>
        </div>
    """.format(
        st.session_state.total_questions,
        st.session_state.correct_answers,
        st.session_state.wrong_answers,
        st.session_state.total_banks,
        st.session_state.banked_amount
    ), unsafe_allow_html=True)
    
    # Add Go Home button
    if st.button("🏠 Go Home", use_container_width=True):
        for key in st.session_state.keys():
            if key != 'questions':  # Preserve questions
                del st.session_state[key]
        st.rerun()

def display_timer():
    if st.session_state.is_game_active:
        elapsed_time = datetime.now() - st.session_state.timer_start
        remaining_time = st.session_state.game_duration - elapsed_time
        
        if remaining_time.total_seconds() <= 0:
            end_game()
            return "00:00"
        
        minutes = int(remaining_time.total_seconds() // 60)
        seconds = int(remaining_time.total_seconds() % 60)
        return f"{minutes:02d}:{seconds:02d}"
    return "00:00"

def reset_game():
    st.session_state.current_amount = 0
    st.session_state.chain_position = 0
    st.session_state.current_question = random.choice(questions)
    st.session_state.timer_start = datetime.now()
    st.session_state.is_game_active = True
    st.session_state.game_started = True
    st.session_state.show_results = False
    st.session_state.banked_amount = 0
    st.session_state.total_questions = 0
    st.session_state.correct_answers = 0
    st.session_state.wrong_answers = 0
    st.session_state.total_banks = 0

def end_game():
    st.session_state.is_game_active = False
    st.session_state.game_started = False
    st.session_state.show_results = True

# Initialize all session state variables at the start
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'is_game_active' not in st.session_state:
    st.session_state.is_game_active = False
if 'current_amount' not in st.session_state:
    st.session_state.current_amount = 0
if 'chain_position' not in st.session_state:
    st.session_state.chain_position = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'banked_amount' not in st.session_state:
    st.session_state.banked_amount = 0
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = datetime.now()
if 'game_duration' not in st.session_state:
    st.session_state.game_duration = timedelta(minutes=3)
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = 0
if 'total_banks' not in st.session_state:
    st.session_state.total_banks = 0
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Questions and money chain
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Which planet is known as the Red Planet?", "answer": "Mars"},
    {"question": "What is the largest mammal in the world?", "answer": "Blue Whale"},
    {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
    {"question": "What is the chemical symbol for gold?", "answer": "Au"},
    {"question": "Which country invented tea?", "answer": "China"},
    {"question": "What is the fastest land animal?", "answer": "Cheetah"},
    {"question": "Who wrote 'Romeo and Juliet'?", "answer": "William Shakespeare"},
    {"question": "What is the capital of Japan?", "answer": "Tokyo"},
    {"question": "What is the largest organ in the human body?", "answer": "Skin"},
]

money_chain = [0, 5, 10, 15, 20, 25, 50, 100, 200]

# Title
st.markdown("<h1 style='text-align: center;'>🔗 The Weakest Link 🎮</h1>", unsafe_allow_html=True)

# Game states handling
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if st.session_state.show_results:
    # Results Screen
    st.markdown("""
        <div style='
            padding: 20px;
            background-color: #2b2b2b;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            color: white;
        '>
            <h2 style='color: #FF4B4B;'>🎮 Game Over! 🎮</h2>
            <div style='margin: 20px 0;'>
                <h3 style='color: #00CC00;'>Game Statistics</h3>
                <table style='
                    width: 100%; 
                    margin: 10px 0;
                    color: white;
                    border-collapse: separate;
                    border-spacing: 0 8px;
                '>
                    <tr style='background-color: #363636;'>
                        <td style='text-align: left; padding: 10px; border-radius: 5px 0 0 5px;'>Total Questions:</td>
                        <td style='text-align: right; padding: 10px; border-radius: 0 5px 5px 0;'>{}</td>
                    </tr>
                    <tr style='background-color: #363636;'>
                        <td style='text-align: left; padding: 10px; border-radius: 5px 0 0 5px;'>Correct Answers:</td>
                        <td style='text-align: right; padding: 10px; border-radius: 0 5px 5px 0;'>{}</td>
                    </tr>
                    <tr style='background-color: #363636;'>
                        <td style='text-align: left; padding: 10px; border-radius: 5px 0 0 5px;'>Wrong Answers:</td>
                        <td style='text-align: right; padding: 10px; border-radius: 0 5px 5px 0;'>{}</td>
                    </tr>
                    <tr style='background-color: #363636;'>
                        <td style='text-align: left; padding: 10px; border-radius: 5px 0 0 5px;'>Total Banks:</td>
                        <td style='text-align: right; padding: 10px; border-radius: 0 5px 5px 0;'>{}</td>
                    </tr>
                </table>
            </div>
            <h3 style='color: #1f77b4;'>Final Prize Money</h3>
            <h1 style='color: #00CC00; font-size: 48px;'>₹{}</h1>
        </div>
    """.format(
        st.session_state.total_questions,
        st.session_state.correct_answers,
        st.session_state.wrong_answers,
        st.session_state.total_banks,
        st.session_state.banked_amount
    ), unsafe_allow_html=True)
    
    # Go Home button with updated styling
    if st.button("🏠 Go Home", use_container_width=True, type="primary"):
        for key in st.session_state.keys():
            if key != 'questions':  # Preserve questions
                del st.session_state[key]
        st.rerun()

elif not st.session_state.game_started:
    # Game Setup Screen
    if 'custom_duration' not in st.session_state:
        st.session_state.custom_duration = 180

    st.markdown("<h2 style='text-align: center;'>Set Game Duration</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("-30 sec", use_container_width=True):
            if st.session_state.custom_duration > 30:
                st.session_state.custom_duration -= 30
                st.rerun()
    
    with col2:
        minutes = st.session_state.custom_duration // 60
        seconds = st.session_state.custom_duration % 60
        st.markdown(f"<h3 style='text-align: center;'>⏱️ {minutes:02d}:{seconds:02d}</h3>", unsafe_allow_html=True)
    
    with col3:
        if st.button("+30 sec", use_container_width=True):
            st.session_state.custom_duration += 30
            st.rerun()

    if st.button("🔄 Start New Game", use_container_width=True, key="new_game_btn"):
        st.session_state.game_duration = timedelta(seconds=st.session_state.custom_duration)
        reset_game()
        st.rerun()

else:
    # Active Game Screen
    # Calculate timer display first
    current_timer = display_timer()
    
    # Display timer
    st.markdown(f"<div class='timer-display'>⏱️ {current_timer}</div>", unsafe_allow_html=True)

    # Display current amount and banked amount
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<p class='money-display'>Current: ₹{st.session_state.current_amount}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p class='money-display'>Banked: ₹{st.session_state.banked_amount}</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p class='money-display'>Chain: {st.session_state.chain_position}</p>", unsafe_allow_html=True)

    # Display question and answer
    if st.session_state.current_question:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("<p class='big-font'>Current Question:</p>", unsafe_allow_html=True)
            st.write(st.session_state.current_question["question"])
        with col2:
            st.markdown("<p class='big-font'>Answer:</p>", unsafe_allow_html=True)
            st.write(st.session_state.current_question["answer"])

    # Game controls
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✅ Correct", use_container_width=True, key="correct_btn"):
            if st.session_state.is_game_active:
                if st.session_state.chain_position < len(money_chain) - 1:
                    st.session_state.chain_position += 1
                    st.session_state.current_amount = money_chain[st.session_state.chain_position]
                    st.session_state.current_question = random.choice(questions)
                    st.session_state.total_questions += 1
                    st.session_state.correct_answers += 1
                    st.rerun()

    with col2:
        if st.button("❌ Wrong", use_container_width=True, key="wrong_btn"):
            if st.session_state.is_game_active:
                st.session_state.current_amount = 0
                st.session_state.chain_position = 0
                st.session_state.current_question = random.choice(questions)
                st.session_state.total_questions += 1
                st.session_state.wrong_answers += 1
                st.rerun()

    with col3:
        if st.button("🏦 Bank", use_container_width=True, key="bank_btn"):
            if st.session_state.is_game_active:
                st.session_state.banked_amount += st.session_state.current_amount
                st.session_state.current_amount = 0
                st.session_state.chain_position = 0
                st.session_state.total_banks += 1
                st.balloons()
                st.session_state.current_question = random.choice(questions)
                st.rerun()

    with col4:
        if st.button("🛑 End Game", use_container_width=True, key="end_btn"):
            st.session_state.is_game_active = False
            st.session_state.game_started = False
            st.session_state.show_results = True
            st.rerun()

    # Display money chain
    st.markdown("---")
    st.markdown("<p class='big-font'>Money Chain:</p>", unsafe_allow_html=True)
    money_chain_display = " → ".join([f"₹{amount}" for amount in money_chain])
    st.markdown(f"<p style='text-align: center;'>{money_chain_display}</p>", unsafe_allow_html=True)

    # Add keyboard controls
    if st.session_state.game_started:
        # Add JavaScript for keyboard controls
        js_code = """
        <script>
        document.addEventListener('keydown', function(e) {
            if (e.key === 'q' || e.key === 'Q') {
                document.querySelector('button[data-testid="correct_btn"]').click();
            }
            if (e.key === 'e' || e.key === 'E') {
                document.querySelector('button[data-testid="wrong_btn"]').click();
            }
            if (e.key === ' ') {
                e.preventDefault();
                document.querySelector('button[data-testid="bank_btn"]').click();
            }
        });
        </script>
        """
        html(js_code)

    # Auto-rerun for timer update
    if st.session_state.is_game_active:
        time.sleep(0.1)
        st.rerun() 