import streamlit as st  # type: ignore[import]

from utils.pdf_reader import extract_text_from_pdf

from utils.ai_helper import (
    generate_summary,
    generate_questions,
    generate_mcqs,
    create_vector_store,
    ask_pdf_question
)

from database import (
    register_user,
    login_user,
    save_chat,
    get_chat_history
)


# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# LOAD CSS
def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# PAGE CONFIG
st.set_page_config(
    page_title="EduGenie AI",
    page_icon="📘",
    layout="wide"
)

load_css()


# SIDEBAR
with st.sidebar:

    st.title("📘 EduGenie AI")

    st.markdown("""
    ### Smart AI Study Assistant

    Features:
    - 📄 PDF Reader
    - 🤖 AI Summary
    - ❓ Important Questions
    - 🧠 MCQ Generator
    - 💬 Chat with PDF
    """)

    st.markdown("---")

    st.info("Built with Generative AI + Gemini")

    menu = ["Login", "Register"]

    choice = st.selectbox(
        "Menu",
        menu
    )

    # LOGOUT BUTTON
    if st.session_state.logged_in:

        if st.button("Logout"):

            st.session_state.logged_in = False

            st.rerun()


# REGISTER
if choice == "Register":

    st.subheader("📝 Create Account")

    new_user = st.text_input("Username")

    new_password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        register_user(new_user, new_password)

        st.success("✅ Account Created Successfully")


# LOGIN
elif choice == "Login":

    st.subheader("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        result = login_user(username, password)

        if result:

            st.session_state.logged_in = True

            st.session_state.username = username

            st.success(f"Welcome {username} 🎉")

            st.rerun()

        else:

            st.error("Invalid Username or Password")


# MAIN DASHBOARD
if st.session_state.logged_in:

    # TITLE
    st.title("📘 EduGenie AI")

    st.subheader("Smart AI Study Assistant")

    # METRICS
    col1, col2, col3 = st.columns(3)

    col1.metric("AI Features", "5+")

    col2.metric("Powered By", "Gemini AI")

    col3.metric("Project Type", "Generative AI")

    # PDF UPLOAD
    uploaded_file = st.file_uploader(
        "Upload your PDF Notes",
        type=["pdf"]
    )

    # PROCESS PDF
    if uploaded_file:

        st.success("✅ PDF Uploaded Successfully!")

        with st.spinner("Reading PDF..."):

            pdf_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("Preparing AI Chat..."):

            vector_store = create_vector_store(pdf_text)


        # TABS
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Summary",
            "❓ Questions",
            "🧠 MCQs",
            "💬 Chat"
        ])

        # SUMMARY
        with tab1:

            if st.button("Generate AI Summary"):

                with st.spinner("Generating Summary..."):

                    summary = generate_summary(pdf_text)

                st.write(summary)

        # QUESTIONS
        with tab2:

            if st.button("Generate Important Questions"):

                with st.spinner("Generating Questions..."):

                    questions = generate_questions(pdf_text)

                st.write(questions)

        # MCQS
        with tab3:

            if st.button("Generate MCQs"):

                with st.spinner("Generating MCQs..."):

                    mcqs = generate_mcqs(pdf_text)

                st.write(mcqs)

        # CHAT
        with tab4:

            st.subheader("💬 Chat With PDF")

            user_question = st.text_input(
                "Ask a question from the PDF"
            )

            if user_question:

                with st.spinner("Thinking..."):

                    answer = ask_pdf_question(
                        vector_store,
                        user_question
                    )

                st.write(answer)

                save_chat(
                    st.session_state.username,
                    user_question,
                    answer
                )
        # CHAT HISTORY
        st.subheader("🕘 Chat History")

        history = get_chat_history(
            st.session_state.username
        )

        if history:

            for question, answer in history:

                st.markdown(f"### ❓ {question}")

                st.write(answer)

                st.markdown("---")

        else:

            st.info("No chat history available yet.")
            
# NOT LOGGED IN
else:

    st.warning("⚠️ Please Login to Access EduGenie AI")