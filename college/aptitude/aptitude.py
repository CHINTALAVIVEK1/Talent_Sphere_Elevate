import streamlit as st
import datetime
import random
from college.coding.database import get_aptitude_scores, save_aptitude_score

APTITUDE_SYLLABUS = {
    "Quantitative": ["Percentage", "Profit and Loss", "Speed and Distance"],
    "Logical Reasoning": ["Series Completion", "Coding-Decoding", "Blood Relations"],
    "Verbal Ability": ["Synonyms", "Antonyms", "Sentence Correction"]
}

# --- Database of Vocabulary and Templates to fuel the generator ---
VOCABULARY = [
    {"word": "admonish", "synonym": "warn", "antonym": "applaud", "definition": "warn or reprimand someone firmly"},
    {"word": "brief", "synonym": "short", "antonym": "long", "definition": "of short duration or concise"},
    {"word": "embezzle", "synonym": "misappropriate", "antonym": "return", "definition": "steal or misappropriate money in trust"},
    {"word": "candid", "synonym": "honest", "antonym": "secretive", "definition": "truthful and straightforward"},
    {"word": "dearth", "synonym": "scarcity", "antonym": "abundance", "definition": "a scarcity or lack of something"},
    {"word": "frugal", "synonym": "economical", "antonym": "extravagant", "definition": "sparing or economical regarding money"},
    {"word": "ambiguous", "synonym": "vague", "antonym": "clear", "definition": "unclear or double-meaning"},
    {"word": "acquitted", "synonym": "freed", "antonym": "convicted", "definition": "declared not guilty"},
    {"word": "harsh", "synonym": "severe", "antonym": "mild", "definition": "severe or cruel"},
    {"word": "optimistic", "synonym": "hopeful", "antonym": "pessimistic", "definition": "hopeful and confident about the future"},
    {"word": "placate", "synonym": "appease", "antonym": "provoke", "definition": "make someone less angry or hostile"},
    {"word": "tenacious", "synonym": "persistent", "antonym": "weak", "definition": "tending to keep a firm hold of something"},
    {"word": "volatile", "synonym": "unstable", "antonym": "stable", "definition": "liable to change rapidly and unpredictably"},
    {"word": "zealous", "synonym": "passionate", "antonym": "indifferent", "definition": "having or showing zeal"},
    {"word": "lethargic", "synonym": "sluggish", "antonym": "energetic", "definition": "sluggish and apathetic"},
    {"word": "authentic", "synonym": "genuine", "antonym": "fake", "definition": "of undisputed origin; genuine"},
    {"word": "benevolent", "synonym": "kind", "antonym": "malevolent", "definition": "well meaning and kindly"},
    {"word": "capricious", "synonym": "fickle", "antonym": "consistent", "definition": "given to sudden and unaccountable changes of mood"},
    {"word": "diligent", "synonym": "hardworking", "antonym": "lazy", "definition": "having or showing care and conscientiousness in work"},
    {"word": "ephemeral", "synonym": "transient", "antonym": "permanent", "definition": "lasting for a very short time"}
]

def generate_questions(type_name, topic_name, set_name):
    """
    Deterministic question generator. Seeds random with the set parameters 
    to guarantee consistent question sets on every render.
    Returns exactly 20 questions.
    """
    # Create deterministic seed from inputs
    seed_str = f"{type_name}_{topic_name}_{set_name}"
    rng = random.Random(hash(seed_str))
    
    questions = []
    
    for i in range(1, 21):
        q_id = f"gen_{topic_name.lower().replace(' ', '_')}_{set_name.lower()}_{i}"
        
        # ==========================================
        # QUANTITATIVE TOPICS
        # ==========================================
        if topic_name == "Percentage":
            style = i % 3
            if style == 0:
                p = rng.choice([10, 20, 25, 40, 50])
                # Math: if A earns P% less than B, B is A / (1 - P/100)
                ans_pct = int((p / (100 - p)) * 100)
                q_text = f"If A's salary is {p}% less than B's salary, then how much percent is B's salary more than A's?"
                options = [f"{ans_pct - 5}%", f"{ans_pct}%", f"{ans_pct + 5}%", f"{ans_pct + 10}%"]
                correct = 1
                explanation = f"Let B's salary be 100. A's salary is {100-p}. Difference is {p}. Percent B is more than A = ({p} / {100-p}) * 100 = {ans_pct}%."
            elif style == 1:
                val1 = rng.choice([200, 400, 500, 800, 1000])
                val2 = rng.choice([10, 15, 20, 25, 30])
                ans_val = int((val1 * val2) / 100)
                q_text = f"What is {val2}% of {val1}?"
                options = [f"{ans_val - 10}", f"{ans_val - 5}", f"{ans_val}", f"{ans_val + 5}"]
                correct = 2
                explanation = f"Value = ({val2} * {val1}) / 100 = {ans_val}."
            else:
                p1 = rng.choice([10, 20, 30])
                p2 = rng.choice([10, 20, 30])
                # Net change: -p1 + p2 - (p1*p2)/100
                net = -p1 + p2 - (p1 * p2) / 100.0
                q_text = f"If the price of a commodity decreases by {p1}% and then increases by {p2}%, what is the net percentage change in price?"
                options = [f"{net - 2.5}%", f"{net}%", f"{net + 2.5}%", f"{net + 5}%"]
                correct = 1
                explanation = f"Net change = -{p1} + {p2} - ({p1} * {p2})/100 = {net}%."

        elif topic_name == "Profit and Loss":
            style = i % 3
            if style == 0:
                cp = rng.choice([50, 100, 200, 400, 500])
                sp = cp + int(cp * rng.choice([0.1, 0.2, 0.25, 0.5]))
                profit_pct = int(((sp - cp) / cp) * 100)
                q_text = f"A merchant buys an item for ${cp} and sells it for ${sp}. Find the profit percentage."
                options = [f"{profit_pct - 5}%", f"{profit_pct - 2}%", f"{profit_pct}%", f"{profit_pct + 5}%"]
                correct = 2
                explanation = f"Profit = Selling Price - Cost Price = ${sp} - ${cp} = ${sp - cp}. Profit % = ({sp - cp} / {cp}) * 100 = {profit_pct}%."
            elif style == 1:
                sp = rng.choice([90, 180, 270, 360])
                loss_pct = 10
                cp = int(sp / (1 - loss_pct / 100.0))
                q_text = f"By selling an item for ${sp}, a dealer loses {loss_pct}%. What was the cost price of the item?"
                options = [f"${cp - 20}", f"${cp - 10}", f"${cp}", f"${cp + 20}"]
                correct = 2
                explanation = f"Cost Price = Selling Price / (1 - Loss/100) = {sp} / (1 - 0.1) = ${cp}."
            else:
                items = rng.choice([10, 15, 20, 25])
                sp_items = items - 5
                profit_pct = int(((items - sp_items) / sp_items) * 100)
                q_text = f"If the cost price of {items} items is equal to the selling price of {sp_items} items, what is the profit percentage?"
                options = [f"{profit_pct - 10}%", f"{profit_pct - 5}%", f"{profit_pct}%", f"{profit_pct + 5}%"]
                correct = 2
                explanation = f"Profit % = ((Items CP - Items SP) / Items SP) * 100 = ({items - sp_items} / {sp_items}) * 100 = {profit_pct}%."

        elif topic_name == "Speed and Distance":
            style = i % 3
            if style == 0:
                speed_kmh = rng.choice([36, 54, 72, 90])
                time_sec = rng.choice([10, 15, 20])
                length = int(speed_kmh * (5 / 18.0) * time_sec)
                q_text = f"A train running at the speed of {speed_kmh} km/hr crosses a stationary pole in {time_sec} seconds. What is the length of the train?"
                options = [f"{length - 50} meters", f"{length} meters", f"{length + 50} meters", f"{length + 100} meters"]
                correct = 1
                explanation = f"Speed in m/s = {speed_kmh} * 5/18 = {speed_kmh * 5//18} m/s. Length = Speed * Time = {speed_kmh * 5//18} * {time_sec} = {length} meters."
            elif style == 1:
                dist_m = rng.choice([500, 600, 1000, 1200])
                time_min = rng.choice([5, 10, 15])
                speed_kmh = round((dist_m / (time_min * 60.0)) * 3.6, 2)
                q_text = f"A person crosses a {dist_m} meter long street in {time_min} minutes. What is his speed in km per hour?"
                options = [f"{speed_kmh - 2} km/hr", f"{speed_kmh - 1} km/hr", f"{speed_kmh} km/hr", f"{speed_kmh + 1} km/hr"]
                correct = 2
                explanation = f"Speed = Distance / Time = {dist_m}m / {time_min * 60}s = {dist_m / (time_min * 60):.2f} m/s. In km/hr = {dist_m / (time_min * 60):.2f} * 3.6 = {speed_kmh} km/hr."
            else:
                s1 = rng.choice([40, 50, 60])
                s2 = s1 + 10
                diff_d = rng.choice([10, 15, 20])
                actual_d = int((diff_d * s1) / (s2 - s1))
                q_text = f"If a man walks at {s2} km/hr instead of {s1} km/hr, he would have walked {diff_d} km more. The actual distance travelled by him is:"
                options = [f"{actual_d - 10} km", f"{actual_d} km", f"{actual_d + 10} km", f"{actual_d + 20} km"]
                correct = 1
                explanation = f"Let actual distance be d. d/{s1} = (d + {diff_d})/{s2} => {s2}d = {s1}d + {diff_d * s1} => {s2 - s1}d = {diff_d * s1} => d = {actual_d} km."

        # ==========================================
        # LOGICAL TOPICS
        # ==========================================
        elif topic_name == "Series Completion":
            style = i % 3
            if style == 0:
                start = rng.choice([2, 5, 10, 15])
                diff = rng.choice([3, 4, 5])
                seq = [start + diff * k for k in range(5)]
                q_text = f"Look at this series: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... What number should come next?"
                options = [str(seq[3] + diff - 1), str(seq[3] + diff), str(seq[3] + diff + 1), str(seq[3] + diff + 2)]
                correct = 1
                explanation = f"This is an arithmetic progression series with a common difference of +{diff}."
            elif style == 1:
                start = rng.choice([3, 4, 5])
                ratio = 2
                seq = [start * (ratio ** k) for k in range(4)]
                q_text = f"Look at this series: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... What number should come next?"
                options = [str(seq[3] * ratio - 5), str(seq[3] * ratio), str(seq[3] * ratio + 5), str(seq[3] * ratio + 10)]
                correct = 1
                explanation = f"This is a geometric progression series where each number is multiplied by {ratio}."
            else:
                start = rng.choice([100, 80, 60])
                diff1 = 10
                diff2 = 5
                seq = [start, start - diff1, start - diff1 + diff2, start - 2 * diff1 + diff2, start - 2 * diff1 + 2 * diff2]
                q_text = f"Look at this series: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... What number should come next?"
                ans = seq[4] - diff1
                options = [str(ans - 5), str(ans), str(ans + 5), str(ans + 10)]
                correct = 1
                explanation = f"Alternating series subtraction: subtract {diff1}, then add {diff2}. Next operation is -{diff1}."

        elif topic_name == "Coding-Decoding":
            words = ["COULD", "MARGIN", "CALM", "ROPE", "BASE"]
            word = rng.choice(words)
            shift = rng.choice([-1, 1, 2])
            
            # Helper to shift word
            coded = "".join([chr(ord(c) + shift) for c in word])
            target_word = "ALLY" if word != "ALLY" else "BASE"
            target_coded = "".join([chr(ord(c) + shift) for c in target_word])
            
            q_text = f"If in a code language, {word} is written as {coded}, how will {target_word} be written?"
            options = [target_coded[:2] + "XX", target_coded, target_coded[:3] + "Z", "None of these"]
            correct = 1
            explanation = f"Each character is shifted by {shift} positions in the alphabet sequence."

        elif topic_name == "Blood Relations":
            relations = [
                {"q": "Pointing to a photograph, Vipul said, 'She is the daughter of my grandfather's only son.' How is Vipul related to the girl?", "ans": "Brother", "exp": "Grandfather's only son is Vipul's father. The girl is the daughter of Vipul's father, which makes her Vipul's sister. Vipul is her brother."},
                {"q": "A man said to a lady, 'Your mother's husband's sister is my aunt.' How is the lady related to the man?", "ans": "Sister", "exp": "Lady's mother's husband is the lady's father. Father's sister is the lady's aunt. Since she is also the man's aunt, the lady and the man are siblings."},
                {"q": "Introducing Sonia, Aamir says, 'She is the wife of the only grandson of my father.' How is Aamir related to Sonia?", "ans": "Father-in-law", "exp": "Father's grandson is Aamir's son. Sonia is the wife of Aamir's son, making Aamir her father-in-law."},
                {"q": "If A is B's brother, B is C's sister, and C is D's father, how is A related to D?", "ans": "Uncle", "exp": "A is the brother of C (since A is B's brother and B is C's sister). C is D's father. Therefore, A is D's father's brother, which is D's uncle."},
                {"q": "Pointing to a man, a woman said, 'His mother is the only daughter of my mother.' How is the woman related to the man?", "ans": "Mother", "exp": "Only daughter of the woman's mother is the woman herself. So the man's mother is the woman herself."}
            ]
            rel = relations[i % len(relations)]
            q_text = f"{rel['q']} (Set variant {i})"
            options = ["Brother", "Uncle", "Father-in-law", "Sister", "Mother"]
            if rel["ans"] not in options:
                options[0] = rel["ans"]
            options = sorted(list(set(options)))
            correct = options.index(rel["ans"])
            explanation = rel["exp"]

        # ==========================================
        # VERBAL TOPICS
        # ==========================================
        elif topic_name == "Synonyms":
            vocab_item = VOCABULARY[i % len(VOCABULARY)]
            word = vocab_item["word"]
            syn = vocab_item["synonym"]
            
            q_text = f"Choose the synonym of '{word.upper()}':"
            options = ["ignore", "support", syn, "criticize"]
            options = sorted(list(set(options)))
            correct = options.index(syn)
            explanation = f"'{word}' means {vocab_item['definition']}."

        elif topic_name == "Antonyms":
            vocab_item = VOCABULARY[(i + 5) % len(VOCABULARY)]
            word = vocab_item["word"]
            ant = vocab_item["antonym"]
            
            q_text = f"Choose the antonym of '{word.upper()}':"
            options = ["basic", "support", ant, "similar"]
            options = sorted(list(set(options)))
            correct = options.index(ant)
            explanation = f"The opposite of '{word}' ({vocab_item['definition']}) is '{ant}'."

        elif topic_name == "Sentence Correction":
            grammar_sets = [
                {"q": "Choose the grammatically correct sentence:", "opts": ["Neither of the boys are going.", "Neither of the boys is going.", "Neither of the boys were going.", "None of the above."], "cor": 1, "exp": "'Neither' is singular and requires the singular verb 'is'."},
                {"q": "Identify the correct past tense sentence:", "opts": ["He gone to the store yesterday.", "He went to the store yesterday.", "He has gone to the store yesterday.", "He was went to the store yesterday."], "cor": 1, "exp": "Simple past tense 'went' is required when referring to a specific past time ('yesterday')."},
                {"q": "Choose the correct pronoun syntax:", "opts": ["Between you and I, this is a secret.", "Between you and me, this is a secret.", "Between you and we, this is a secret.", "Between you and us, this is a secret."], "cor": 1, "exp": "'Between' is a preposition and requires objective case pronouns ('me')."},
                {"q": "Select the correct plural sentence:", "opts": ["One of my friends are coming today.", "One of my friends is coming today.", "One of my friend is coming today.", "One of my friends were coming today."], "cor": 1, "exp": "The subject is the singular 'One', requiring the singular verb 'is'."}
            ]
            gs = grammar_sets[i % len(grammar_sets)]
            q_text = f"{gs['q']} (Variant {i})"
            options = gs["opts"]
            correct = gs["cor"]
            explanation = gs["exp"]
            
        questions.append({
            "id": q_id,
            "question": q_text,
            "options": options,
            "correct": correct,
            "explanation": explanation
        })
        
    return questions

def aptitude_practice():
    st.markdown("### Aptitude Practice")
    st.write("Train Quantitative, Logical, and Verbal skills. Select your type, topic, and set to practice.")
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return
        
    tab_practice, tab_history = st.tabs(["Take Quiz", "Attempt History"])
    
    with tab_practice:
        # Step 1: Select Type
        selected_type = st.selectbox("Select Aptitude Type", list(APTITUDE_SYLLABUS.keys()))
        
        # Step 2: Select Topic based on Type
        topics = APTITUDE_SYLLABUS[selected_type]
        selected_topic = st.selectbox("Select Topic Set", topics)
        
        # Step 3: Select Set (Set 1, Set 2, Set 3)
        selected_set = st.selectbox("Select Quiz Set", ["Set 1", "Set 2", "Set 3"])
        
        # Dynamically generate 20 questions for this set parameters
        questions = generate_questions(selected_type, selected_topic, selected_set)
        
        st.write(f"Category: **{selected_type}** | Topic: **{selected_topic}** | **{selected_set}** ({len(questions)} Questions)")
        st.write("Select options for all 20 questions and click Submit below.")
        
        user_selections = {}
        for idx, q in enumerate(questions):
            st.markdown(f"**Q{idx+1}: {q['question']}**")
            user_selections[q["id"]] = st.radio(
                "Select Answer",
                options=q["options"],
                key=f"opt_{selected_type}_{selected_topic}_{selected_set}_{q['id']}",
                label_visibility="collapsed"
            )
            st.write("")
            
        submit_quiz = st.button("Submit Quiz Answers", type="primary")
        
        if submit_quiz:
            score = 0
            results = []
            
            for idx, q in enumerate(questions):
                selected_val = user_selections[q["id"]]
                selected_idx = q["options"].index(selected_val)
                correct_idx = q["correct"]
                
                passed = (selected_idx == correct_idx)
                if passed:
                    score += 1
                    
                results.append({
                    "idx": idx + 1,
                    "question": q["question"],
                    "selected": selected_val,
                    "correct": q["options"][correct_idx],
                    "passed": passed,
                    "explanation": q["explanation"]
                })
                
            # Log score to db
            category_label = f"{selected_type} - {selected_topic} ({selected_set})"
            save_aptitude_score(user_id, category_label, score, len(questions))
            
            st.subheader(f"Quiz Score: {score} / {len(questions)}")
            st.progress(score / len(questions))
            
            st.write("")
            st.markdown("##### Detailed Review:")
            for res in results:
                status_text = "Passed" if res["passed"] else "Failed"
                if res["passed"]:
                    st.success(f"Q{res['idx']}: {status_text} | Your answer: {res['selected']}")
                else:
                    st.error(f"Q{res['idx']}: {status_text} | Your answer: {res['selected']} | Correct answer: {res['correct']}")
                st.info(f"Explanation: {res['explanation']}")
                st.write("")
                
    with tab_history:
        st.markdown("#### Quiz Performance History")
        scores = get_aptitude_scores(user_id)
        
        if scores:
            for s in scores:
                st.markdown(f"""
                <div style="background-color: #1e293b; padding: 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #334155; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 700; color: #f8fafc;">{s['category']}</span>
                        <span style="color: #94a3b8; font-size: 13px; margin-left: 12px;">Attempted on {s['date']}</span>
                    </div>
                    <b style="color: #10b981; font-size: 16px;">{s['score']} / {s['total']}</b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No attempts found. Take a quiz to begin tracking your history.")
