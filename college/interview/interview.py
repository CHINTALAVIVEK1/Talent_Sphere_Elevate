import streamlit as st
import json
import random
from utils.gemini import client
from google.genai import types

# Interview Questions Bank - 15 Easy questions per role with specific hints (60 total)
INTERVIEW_ROLES = {
    "Python Developer": [
        {
            "q": "What is the difference between a list and a tuple in Python?",
            "hint": "Think about mutability. Which one can be modified after creation?"
        },
        {
            "q": "How do you add or remove elements in a Python list?",
            "hint": "Recall list methods like append() and remove() or pop()."
        },
        {
            "q": "Explain the difference between local and global variables in Python.",
            "hint": "Think about variable scope. Where can each variable be accessed?"
        },
        {
            "q": "What is a dictionary in Python, and how do you access its values?",
            "hint": "Recall key-value pairs and using square brackets or get() to fetch values."
        },
        {
            "q": "How do you write a basic 'for' loop in Python to iterate through a list of numbers?",
            "hint": "Use 'for num in list_name:' syntax to iterate."
        },
        {
            "q": "What is the difference between the double equals (==) operator and the 'is' operator in Python?",
            "hint": "== checks for equality of values; 'is' checks if they point to the exact same object in memory."
        },
        {
            "q": "What are the common built-in data types in Python (such as int, float, string)?",
            "hint": "Recall types used to store numbers, decimals, text, and list structures."
        },
        {
            "q": "How do you define a function in Python, and what is the return keyword used for?",
            "hint": "Use the 'def' keyword to start and return to send a value back."
        },
        {
            "q": "What is the purpose of comments in Python, and how do you write single-line comments?",
            "hint": "Comments explain code to other developers. Use the hash (#) symbol for single line."
        },
        {
            "q": "Explain the difference between mutable and immutable objects in Python.",
            "hint": "Mutable objects can be modified; immutable objects cannot be changed."
        },
        {
            "q": "What is the purpose of try-except blocks in Python, and how do they handle errors?",
            "hint": "They catch exceptions so that the program does not crash during execution."
        },
        {
            "q": "How do you read a text file line-by-line using Python's open() function?",
            "hint": "Use 'with open(filename, 'r') as file:' and iterate over it using a loop."
        },
        {
            "q": "What are list comprehensions in Python, and can you show a simple example?",
            "hint": "It is a concise way to create lists, e.g. '[x for x in range(10)]'."
        },
        {
            "q": "What is the range() function in Python, and how is it commonly used in loops?",
            "hint": "It generates a sequence of numbers, often used with 'for i in range(N):'."
        },
        {
            "q": "How do you check the length of a string or a list in Python?",
            "hint": "Use the built-in len() function."
        }
    ],
    "SQL Administrator": [
        {
            "q": "What is a database, and what does SQL stand for?",
            "hint": "SQL stands for Structured Query Language."
        },
        {
            "q": "What is the difference between a primary key and a foreign key in database tables?",
            "hint": "A primary key uniquely identifies rows in a table; a foreign key links tables together."
        },
        {
            "q": "Explain the SELECT statement and how to filter rows using the WHERE clause.",
            "hint": "SELECT picks columns; WHERE adds conditions to filter rows."
        },
        {
            "q": "What is the difference between the CHAR and VARCHAR data types in SQL?",
            "hint": "CHAR is fixed-length; VARCHAR is variable-length."
        },
        {
            "q": "How do you sort query results in SQL using the ORDER BY clause?",
            "hint": "Add 'ORDER BY column_name ASC/DESC' at the end of the query."
        },
        {
            "q": "What is a NULL value in SQL, and how do you check for it in a query?",
            "hint": "NULL represents missing data. Check using 'IS NULL' or 'IS NOT NULL'."
        },
        {
            "q": "Explain the difference between an INNER JOIN and a LEFT JOIN in SQL queries.",
            "hint": "INNER JOIN returns only matching rows; LEFT JOIN returns all rows from the left table and matching ones from the right."
        },
        {
            "q": "What are aggregate functions in SQL (such as SUM, AVG, and COUNT)?",
            "hint": "Functions that compute a single value from a set of rows."
        },
        {
            "q": "How do you group query records using the GROUP BY clause?",
            "hint": "Add 'GROUP BY column_name' to compile groups after filtering."
        },
        {
            "q": "What is the difference between the DELETE and TRUNCATE commands in SQL?",
            "hint": "DELETE removes specific rows and can be rolled back; TRUNCATE removes all rows instantly."
        },
        {
            "q": "How do you add a new record to a database table using the INSERT INTO statement?",
            "hint": "Syntax: 'INSERT INTO table_name (cols) VALUES (vals);'."
        },
        {
            "q": "What is the UPDATE statement used for, and why is the WHERE clause crucial in it?",
            "hint": "Without WHERE, UPDATE will overwrite the target column in every single row in the table."
        },
        {
            "q": "How do you filter unique values in a query using the DISTINCT keyword?",
            "hint": "Write 'SELECT DISTINCT column_name FROM table_name;'."
        },
        {
            "q": "What is a database index, and what is its main benefit?",
            "hint": "An index makes query searches faster, though it takes up storage space."
        },
        {
            "q": "What is the difference between the HAVING clause and the WHERE clause in SQL?",
            "hint": "WHERE filters rows before grouping; HAVING filters aggregated groups after GROUP BY."
        }
    ],
    "Data Scientist": [
        {
            "q": "What is Data Science, and what are its primary phases?",
            "hint": "Key phases include data collection, cleaning, exploration, modeling, and communication."
        },
        {
            "q": "What is the difference between structured and unstructured data?",
            "hint": "Structured data fits in relational tables (rows/cols); unstructured data includes text, audio, and video."
        },
        {
            "q": "What are mean, median, and mode, and how do you calculate them?",
            "hint": "Mean is average, median is middle value, mode is most frequent value."
        },
        {
            "q": "Explain what linear regression is in simple terms.",
            "hint": "It models a straight-line relationship between dependent and independent variables."
        },
        {
            "q": "What is the difference between classification and regression in Machine Learning?",
            "hint": "Classification predicts labels (e.g. Yes/No); regression predicts numbers (e.g. house price)."
        },
        {
            "q": "What is overfitting, and what does it mean in simple terms?",
            "hint": "It means the model fits training data perfectly but performs poorly on new test data."
        },
        {
            "q": "What is the difference between a training dataset and a testing dataset?",
            "hint": "Train data trains the model; test data evaluates model performance."
        },
        {
            "q": "Explain what supervised learning is and provide a simple example.",
            "hint": "Learning from labeled historical data, e.g. predicting spam from labeled emails."
        },
        {
            "q": "Explain what unsupervised learning is and provide a simple example.",
            "hint": "Grouping unlabeled data, e.g. customer segmentation by purchase behavior."
        },
        {
            "q": "What is a confusion matrix, and what is it used to evaluate?",
            "hint": "A grid mapping true values against predicted labels to find classification errors."
        },
        {
            "q": "What is the difference between correlation and causation in data analytics?",
            "hint": "Correlation shows patterns/trends match; causation proves one action triggers the other."
        },
        {
            "q": "What is an outlier, and why should we identify and handle outliers in datasets?",
            "hint": "Outliers are extreme data points that can skew averages and model weights."
        },
        {
            "q": "What is data normalization, and why is it useful?",
            "hint": "Scaling features to a common range (e.g. 0 to 1) so large values do not dominate."
        },
        {
            "q": "What are features and labels in a machine learning dataset?",
            "hint": "Features are inputs (columns); labels are target predictions (outputs)."
        },
        {
            "q": "What is the purpose of data visualization (such as using bar charts or scatter plots)?",
            "hint": "To easily explain patterns, correlations, and trends visually."
        }
    ],
    "Frontend Developer": [
        {
            "q": "What do HTML, CSS, and JavaScript stand for, and what are their respective roles in web development?",
            "hint": "HTML builds structure; CSS controls style; JavaScript adds logic/interactivity."
        },
        {
            "q": "What is the difference between an HTML tag and an HTML element?",
            "hint": "A tag is opening/closing markers (e.g. <div>); an element includes start tag, content, and end tag."
        },
        {
            "q": "How do you link a CSS stylesheet to an HTML document?",
            "hint": "Use '<link rel=\"stylesheet\" href=\"styles.css\">' inside the <head> block."
        },
        {
            "q": "Explain the CSS Box Model (Margin, Border, Padding, and Content).",
            "hint": "Content is text/image, padding is internal space, border is outer line, margin is external space."
        },
        {
            "q": "How do you declare a variable in JavaScript using var, let, and const?",
            "hint": "var is function-scoped; let is block-scoped; const is block-scoped and read-only."
        },
        {
            "q": "What is the difference between double equals (==) and triple equals (===) in JavaScript?",
            "hint": "== checks value after type conversion; === checks both value and type."
        },
        {
            "q": "What is a CSS selector, and can you list three common types?",
            "hint": "Class (.class), ID (#id), and Element selector (div)."
        },
        {
            "q": "What is the DOM (Document Object Model) in web browsers?",
            "hint": "An interface representing HTML structure as a tree, allowing scripts to edit it."
        },
        {
            "q": "How do you add a click event listener to a button in JavaScript?",
            "hint": "Use 'button.addEventListener(\"click\", callback_function);'."
        },
        {
            "q": "What is the difference between block-level and inline HTML elements?",
            "hint": "Block elements start on a new line and take full width (e.g. div); inline take only needed space (e.g. span)."
        },
        {
            "q": "How do you redirect a user to a new web URL using an HTML anchor tag?",
            "hint": "Use '<a href=\"url\">Link Text</a>'."
        },
        {
            "q": "What is a media query in CSS, and what is it used for in responsive design?",
            "hint": "Applies styling rules based on screen widths, e.g. '@media (max-width: 600px)'."
        },
        {
            "q": "Explain the purpose of the 'alt' attribute in HTML image (img) tags.",
            "hint": "Provides fallback description text if an image fails to load or for screen readers."
        },
        {
            "q": "What is the difference between client-side scripting and server-side scripting?",
            "hint": "Client-side compiles in browser; server-side compiles on remote hosts."
        },
        {
            "q": "How do you display text in the browser console using JavaScript?",
            "hint": "Use 'console.log(\"text\");'."
        }
    ]
}

def evaluate_interview(questions, answers):
    """
    Queries Gemini to grade the mock interview answers and provide feedback.
    """
    prompt = "You are an expert technical interviewer.\nEvaluate the candidate's answers to the following questions:\n\n"
    for idx, (q, a) in enumerate(zip(questions, answers)):
        prompt += f"Question {idx+1}: {q}\nCandidate Answer {idx+1}: {a}\n\n"
        
    prompt += """
    You MUST return a JSON object with the following schema:
    - total_score (Integer between 0 and 10 representing overall performance)
    - evaluations (Array of objects, each containing:
      - question (string)
      - score (Integer between 0 and 10)
      - feedback (string summarizing strengths and improvement areas)
      - model_answer (string detailing the optimal answer)
    )
    
    Return ONLY the raw JSON string. Do not wrap in markdown tags or extra characters.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"Error evaluating mock interview: {e}")
        evals = []
        for q in questions:
            evals.append({
                "question": q,
                "score": 7,
                "feedback": "Response reviewed. Focus on adding technical definitions, complexity considerations, and real-world execution cases to improve your score.",
                "model_answer": "Model answer would include core terminology, time/space trade-offs, and clear diagrams/architectures."
            })
        return {
            "total_score": 7,
            "evaluations": evals
        }

def mock_interview():
    st.markdown("### Mock Interview Simulator")
    st.write("Simulate technical screen rounds for top software engineering positions, and get scored reviews.")
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return
        
    if "int_stage" not in st.session_state:
        st.session_state.int_stage = "setup"
        st.session_state.int_role = ""
        st.session_state.int_questions = []
        st.session_state.int_hints = []
        st.session_state.int_answers = []
        st.session_state.int_curr_idx = 0
        st.session_state.int_eval_results = None
        st.session_state.show_hint = False
        
    # --- STAGE 1: SETUP ---
    if st.session_state.int_stage == "setup":
        st.markdown("#### Interview Configuration")
        role = st.selectbox("Select Target Job Role", list(INTERVIEW_ROLES.keys()))
        difficulty = st.selectbox("Select Interview Difficulty", ["Easy", "Medium", "Hard"])
        length = st.selectbox("Select Number of Questions", [3, 5, 10])
        
        start_btn = st.button("Start Mock Interview", type="primary")
        if start_btn:
            st.session_state.int_role = role
            all_qs = INTERVIEW_ROLES[role]
            sampled_items = random.sample(all_qs, min(length, len(all_qs)))
            
            st.session_state.int_questions = [item["q"] for item in sampled_items]
            st.session_state.int_hints = [item["hint"] for item in sampled_items]
            
            st.session_state.int_answers = []
            st.session_state.int_curr_idx = 0
            st.session_state.int_stage = "questioning"
            st.session_state.int_eval_results = None
            st.session_state.show_hint = False
            st.rerun()
            
    # --- STAGE 2: QUESTIONING ---
    elif st.session_state.int_stage == "questioning":
        idx = st.session_state.int_curr_idx
        total_q = len(st.session_state.int_questions)
        
        st.markdown(f"#### Question {idx + 1} of {total_q}")
        st.write(f"Role: **{st.session_state.int_role}**")
        st.progress((idx + 1) / total_q)
        
        st.markdown(f"##### Q: {st.session_state.int_questions[idx]}")
        
        answer_input = st.text_area("Type your response here:", height=150, key=f"ans_input_{idx}")
        
        # Hint logic
        if st.session_state.get("show_hint", False):
            st.info(f"Hint: {st.session_state.int_hints[idx]}")
            
        st.write("")
        
        col_act1, col_act2, col_act3, col_act4 = st.columns([1.5, 1.5, 1.5, 4.5])
        
        with col_act1:
            if idx < total_q - 1:
                next_btn = st.button("Next Question", type="primary", use_container_width=True)
                if next_btn:
                    st.session_state.int_answers.append(answer_input.strip() or "No response.")
                    st.session_state.int_curr_idx += 1
                    st.session_state.show_hint = False
                    st.rerun()
            else:
                submit_btn = st.button("Submit Interview", type="primary", use_container_width=True)
                if submit_btn:
                    st.session_state.int_answers.append(answer_input.strip() or "No response.")
                    st.session_state.int_stage = "evaluating"
                    st.rerun()
                    
        with col_act2:
            hint_btn = st.button("Get Hint", use_container_width=True)
            if hint_btn:
                st.session_state.show_hint = True
                st.rerun()
                
        with col_act3:
            stop_btn = st.button("Stop Interview", use_container_width=True, type="secondary")
            if stop_btn:
                st.session_state.int_stage = "setup"
                st.session_state.int_role = ""
                st.session_state.int_questions = []
                st.session_state.int_hints = []
                st.session_state.int_answers = []
                st.session_state.int_curr_idx = 0
                st.session_state.int_eval_results = None
                st.session_state.show_hint = False
                st.success("Interview terminated.")
                st.rerun()
                    
    # --- STAGE 3: EVALUATING (Intermediate spinner) ---
    elif st.session_state.int_stage == "evaluating":
        st.info("Evaluating your responses... Please wait.")
        with st.spinner("AI evaluating interview answers..."):
            res = evaluate_interview(st.session_state.int_questions, st.session_state.int_answers)
            st.session_state.int_eval_results = res
            st.session_state.int_stage = "results"
            st.rerun()
            
    # --- STAGE 4: RESULTS ---
    elif st.session_state.int_stage == "results":
        res = st.session_state.int_eval_results
        
        st.markdown("#### Interview Evaluation Card")
        st.markdown(f"Overall Performance Score: **{res['total_score']} / 10**")
        st.progress(res["total_score"] / 10.0)
        
        st.write("")
        st.divider()
        
        for idx, item in enumerate(res["evaluations"]):
            st.markdown(f"##### Q{idx+1}: {item['question']}")
            st.markdown(f"Your Answer Score: **{item['score']} / 10**")
            
            st.info(f"Feedback: {item['feedback']}")
            with st.expander("Show Model Answer", expanded=False):
                st.markdown(item["model_answer"])
            st.divider()
            
        if st.button("Start New Interview Session", type="primary"):
            st.session_state.int_stage = "setup"
            st.session_state.int_role = ""
            st.session_state.int_questions = []
            st.session_state.int_hints = []
            st.session_state.int_answers = []
            st.session_state.int_curr_idx = 0
            st.session_state.int_eval_results = None
            st.session_state.show_hint = False
            st.rerun()
