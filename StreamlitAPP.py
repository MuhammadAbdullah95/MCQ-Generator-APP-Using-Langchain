import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from src.mcqgenerator.utils import read_file, get_table_data
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


# loading json file

# with open("D:\AppliedGenAI\Python\mcqgen\Response.json", "r") as file:
#     RESPONSE_JSON = json.load(file)

RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

st.title("MCQ Generator App using Langchain 🦜🔗")
st.caption("Developed By Muhammad ABbdullah")
# Create a form using st.form
with st.form("user input"):
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    # input field
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # subject
    subject = st.text_input("Insert Subject", max_chars=20)

    # Quiz tone
    tone = st.text_input(
        "Complexity level of questions", max_chars=20, placeholder="Simple"
    )

    # Add Button
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                # Count token and the cost of API Call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON),
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Total tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    # Extract the Quiz data From the response
                    quiz = response.get("quiz", None)
                    print(quiz)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)
