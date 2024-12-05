#test2.py
import streamlit as st
import contextlib
import io
from streamlit_ace import st_ace

def user_answer_review_test(module_number):
    from llm3 import llama3
    from content2 import get_content

    st.subheader("Let's see what you understood from this module:")

    role = """
    Scenario:

    You are a teacher who has recently taught a module to me. Now, you have asked Me to explain the concept as you taught Me.

    Task:

    Your task is to review My explanation by comparing it with the correct answer you covered in your lesson which will be provided by me . Assess the clarity of My response based on the following criteria:

    Did I accurately define what the module  is and explain its purpose in Python?
    
    Review My answer based on these criteria and provide constructive feedback to help Me improve My understanding of the module.

    If my answer is not up to the mark, Motivate me and guide me by providing the content by which i can improve myself and my knowledge.
    Don't Degrade me or demotivate me if my answer is wrong or not up to the mark but if both the answers are same tell the student not to copy paste.
    """
    
    correct_answer = get_content(module_number)
    user_answer = st.text_area(placeholder="Write what you understood in your own words here",label="")

    answer_review = llama3(role, f"""The correct explanation is  '''{correct_answer}''' \n  and the user's answer is '''{user_answer}'''. Check whether the user's concept is clear or not, by comparing with the correct explanation and provide a review.
                           If the user's response and the correct explanation are both the same, suggest the user write their own understanding and not copy-paste the content.""")

    if st.button("Evaluate answer") and answer_review is not None:
        st.write(answer_review)

def python_ide():
    st.title("Python IDE")
    code = st_ace(language='python', theme='monokai', height=200)
    result = "Run the code to get the output"

    run_clicked = st.button("Run")
    if run_clicked:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code)
                result = output.getvalue()
            except Exception as e:
                result = str(e)

        st.subheader("Output")
        st.text(result)
    return "Please run your code to get the output and review."

def take_test(question):
    from llm3 import llama3
    st.title("Test")
    st.subheader(question)
    code = st.text_area("Code:")

    run_clicked = st.button("Submit test and get review")
    if run_clicked:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code)
                result = output.getvalue()
            except Exception as e:
                result = str(e)

        st.subheader("Output")
        st.write(result)

        role = """
         You are an expert in Python programming. The user will provide you with a question, code written by them, and its output. You have to give hints to solve 
         the answer if the user is wrong, and if they are correct, motivate them and give hints to solve the problem but dont give them the actual code, if any, to solve the problem.Also give a score out of 10 like 
         1,2,3,4,5,6,7,8,9,10 based on the users answer ,if the code is good and the logic seems to be working give score more than 5 ,if the code is consisting errors and the logic is not correct give score less than 5 
        """
        
        prompt = f"The question is '{question}'. My answer is {code} and the output is '{result}'. Please provide a review and a score out of 10."
        remarks = llama3(role, prompt)

        st.subheader("Review")
        st.write(remarks)
        return remarks

def test_content(module_number, test_question):
    practice_answer = user_answer_review_test(module_number)
    test_review = take_test(test_question)
    return test_review

def get_score(review):
    import re
    from llm3 import llama3
    role = "You are an information extractor based on the given review you will have to extract the score which will be ranging in numbers from(1-10)"
    score = llama3(role, f"You are an information extractor based on the given review you will have to extract the score which will be ranging in numbers from(1-10),Based on the review ''' {review}''' give me score out of 10 , your answer should only consist of the number and nothing else. Ex1: 9, Ex2: 4")
    if score is not None:
        clean_score = int(re.sub('[^0-9]', '', score))
    if clean_score > 5:
        new_score = 1
    else:
        new_score = 0
    
    return new_score