"""
HIS220: Michigan History - Interactive Educational App
A comprehensive course on Michigan's First Residents and Early Colonial Period
CognitiveCloud.ai Learning Platform
"""

import streamlit as st
import time
import json
import random
from datetime import datetime
from typing import List, Dict, Optional

# Configure page
st.set_page_config(
    page_title="HIS220: Michigan History",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_slide' not in st.session_state:
    st.session_state.current_slide = 0
if 'student_responses' not in st.session_state:
    st.session_state.student_responses = {}
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}
if 'total_xp' not in st.session_state:
    st.session_state.total_xp = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'current_streak' not in st.session_state:
    st.session_state.current_streak = 0
if 'completed_modules' not in st.session_state:
    st.session_state.completed_modules = set()

# Course content slides
SLIDES = [
    {
        "id": "welcome",
        "title": "HIS220: Michigan History",
        "content": """
        # 🏛️ HIS220: Michigan History
        ## CognitiveCloud.ai Learning Platform
        
        ### Course Overview: Michigan's First Residents and Colonial Period
        
        **Learning Objectives:**
        - 🔍 **Understand** Michigan's pre-European indigenous populations
        - 📚 **Explore** early European contact and colonial administration
        - 🤝 **Analyze** Native American-European relations and conflicts
        - ⚖️ **Evaluate** the transition from French to British to American control
        
        > *"To understand Michigan's present, we must first understand its past."*
        
        **Course Modules:**
        1. 🏕️ **Indigenous Peoples** - Michigan's First Residents
        2. 🇬🇧 **British Colonial Period** - Imperial Control and Conflict
        3. 🇺🇸 **American Transition** - Revolutionary Changes
        
        **XP System:** Earn points for participation, quiz completion, and thoughtful responses!
        """,
        "xp_reward": 50
    },
    {
        "id": "indigenous_peoples",
        "title": "Module 1: Michigan's First Residents",
        "content": """
        # 🏕️ Module 1: Michigan's First Residents
        
        ## The Land Before Europeans
        
        ### Key Concepts:
        
        **🌍 Pre-Contact Population**
        - Michigan was inhabited by indigenous peoples for thousands of years
        - Multiple distinct tribal groups with complex societies
        - Sophisticated understanding of the land and its resources
        
        **🛶 Major Tribal Groups:**
        - **Ojibwe (Chippewa)** - Northern regions, Great Lakes traders
        - **Ottawa (Odawa)** - Western Michigan, skilled negotiators  
        - **Potawatomi** - Southern Michigan, agricultural communities
        - **Three Fires Confederacy** - Alliance of these three nations
        
        **📅 Archaeological Evidence:**
        - Human presence dating back 10,000+ years
        - Evidence of complex trade networks
        - Seasonal migration patterns following resources
        - Advanced agricultural techniques
        
        ## The Misnomer Problem
        
        **Why "Indians"?**
        Columbus believed he had reached the East Indies, calling inhabitants "Indians." This geographical error persisted for centuries, despite growing awareness of the mistake.
        
        **Recent Archaeological Discoveries:**
        - Previous estimates of 20,000-40,000 years of human presence
        - New evidence suggests even earlier settlement
        - Challenges traditional migration theories
        
        ### 💭 Discussion Point:
        How do you think the persistence of inaccurate terminology affects our understanding of history?
        """,
        "xp_reward": 75,
        "interactive": True,
        "discussion_prompt": "How do you think the persistence of inaccurate terminology like 'Indians' affects our understanding of Native American history and culture?"
    },
    {
        "id": "european_contact",
        "title": "Early European Contact",
        "content": """
        # ⛵ Early European Contact
        
        ## First Encounters
        
        ### French Exploration:
        - **Jacques Marquette** - Jesuit missionary, established missions
        - **Robert de La Salle** - Explorer, claimed territory for France
        - **Antoine de la Mothe Cadillac** - Founded Detroit (1701)
        
        ### Impact on Indigenous Peoples:
        **🔄 Trade Relationships:**
        - Fur trade became central to regional economy
        - Native Americans as essential partners and intermediaries
        - European goods integrated into indigenous lifestyles
        
        **⚔️ Conflicts and Alliances:**
        - Competition between European powers
        - Native American groups forced to choose sides
        - Traditional territories and relationships disrupted
        
        **🦠 Demographic Impact:**
        - Disease epidemics devastated indigenous populations
        - Smallpox, measles, and other Old World diseases
        - Population decline estimated at 90% in some areas
        
        ## Archaeological Revolution
        
        **Changing Timelines:**
        Traditional view: Humans arrived ~12,000 years ago via Bering land bridge
        
        **New Evidence Suggests:**
        - Much earlier human presence (20,000-40,000+ years)
        - Multiple migration routes possible
        - More complex settlement patterns
        
        This challenges our fundamental assumptions about when and how the Americas were first populated.
        """,
        "xp_reward": 100
    },
    {
        "id": "british_control",
        "title": "Module 2: British Colonial Period",
        "content": """
        # 🇬🇧 Module 2: British Colonial Period (1760-1783)
        
        ## Transition from French Rule
        
        ### Treaty of Paris (1763):
        - Ended French and Indian War/Seven Years' War
        - France ceded New France to Britain
        - Michigan became part of British North America
        
        ### British Administration:
        **🏛️ Colonial Structure:**
        - Military governors appointed to key forts
        - Detroit became regional administrative center
        - Gradual establishment of civil government
        
        **📋 Key Policies:**
        - Royal Proclamation of 1763 - limited westward expansion
        - Regulation of Indian trade
        - Maintenance of French legal traditions initially
        
        ## Major Conflicts and Negotiations
        
        ### Bradstreet's Expedition (1764):
        - **Colonel John Bradstreet** reached Detroit August 26, 1764
        - Western tribes assembled and acknowledged British sovereignty
        - Promised to end warfare against British settlers
        
        ### Pontiac's Resistance:
        - **Chief Pontiac** led multi-tribal confederation
        - Coordinated attacks on British forts (1763-1766)
        - Siege of Detroit lasted several months
        - Eventually negotiated peace at Oswego (July 1766)
        
        ### Peace Negotiations:
        - **Sir William Johnson** - British Superintendent of Indian Affairs
        - Skilled at diplomacy with Native American leaders
        - Established framework for ongoing relations
        """,
        "xp_reward": 125,
        "interactive": True,
        "discussion_prompt": "Why do you think Pontiac's resistance was ultimately unsuccessful? What factors led to the eventual peace agreements?"
    },
    {
        "id": "revolutionary_transition",
        "title": "Module 3: Revolutionary Period Transition",
        "content": """
        # 🇺🇸 Module 3: Revolutionary Period and American Control
        
        ## The American Revolution's Impact on Michigan
        
        ### British Loyalist Stronghold:
        - Michigan remained under British control throughout Revolution
        - Detroit served as base for British-allied Native American raids
        - Many settlers remained loyal to British Crown
        
        ### Key Figures in Transition:
        
        **🎖️ Henry Gladwin:**
        - British commander during Pontiac's siege
        - Later lived as country gentleman until death
        - Represented old guard of British military leadership
        
        **⚔️ Captain William Howard:**
        - Worked to save British garrison during uprising  
        - Later fought with British against American Revolution
        - Eventually reconciled to American control
        - Known as "father of the lake region" in 19th century
        
        **🏛️ Charles Langlade:**
        - Mixed French-Ottawa heritage
        - Key intermediary between cultures
        - Continued influence into American period
        
        ## Post-Revolutionary Challenges
        
        ### Treaty of Paris (1783):
        - Britain ceded Old Northwest to United States
        - But British forces remained in Great Lakes forts
        - Created period of uncertain sovereignty
        
        ### Continued British Presence:
        - British didn't evacuate until Jay's Treaty (1796)  
        - Maintained trade relationships with Native Americans
        - Competed with American expansion efforts
        
        ### Native American Position:
        - Caught between British and American interests
        - Some leaders like Pontiac murdered (1769 in St. Louis)
        - Traditional territories increasingly pressured
        - Had to navigate changing political landscape
        
        **🤔 Historical Question:**
        How did the complex relationships between British, American, and Native American interests shape Michigan's early development?
        """,
        "xp_reward": 150,
        "interactive": True,
        "discussion_prompt": "How did the overlapping claims of British, American, and Native American groups create challenges for Michigan's development after the Revolution?"
    },
    {
        "id": "synthesis",
        "title": "Course Synthesis and Reflection",
        "content": """
        # 🎯 Course Synthesis: Understanding Michigan's Foundations
        
        ## Major Themes Across Periods:
        
        ### 🔄 Cultural Contact and Conflict:
        - **Indigenous Sophistication:** Complex societies existed long before European contact
        - **European Disruption:** Disease, warfare, and territorial pressure
        - **Adaptation and Resistance:** Native American responses to changing circumstances
        
        ### 🏛️ Imperial Competition:
        - **French Colonial Model:** Trade partnerships, missionary activity
        - **British Administrative Approach:** Military control, formal treaties
        - **American Expansion:** Territorial acquisition, settler colonialism
        
        ### 🌊 Geographic Significance:
        - **Great Lakes:** Highway for trade and military movement
        - **Strategic Locations:** Detroit, Mackinac Island, other key sites
        - **Natural Resources:** Furs, timber, agricultural potential
        
        ## Continuing Questions:
        
        **🤔 Historical Interpretation:**
        - How do we balance different cultural perspectives on the same events?
        - What sources do we privilege in understanding the past?
        - How do archaeological discoveries change our understanding?
        
        **📊 Evidence and Analysis:**
        - What can material culture tell us that written sources cannot?
        - How do we account for bias in historical sources?
        - Why do historical interpretations change over time?
        
        ## Looking Forward:
        
        **🚀 Next in Michigan History:**
        - Territorial period and path to statehood
        - Economic development and industrialization  
        - Immigration and cultural diversity
        - Modern challenges and opportunities
        
        ### 📝 Final Reflection Assignment:
        Choose one of the three major periods we studied (Indigenous, British, American transition) and write a 500-word reflection on how that period continues to influence modern Michigan.
        
        **Consider:**
        - What legacies remain visible today?
        - How do modern communities remember this period?
        - What lessons can we learn for contemporary challenges?
        """,
        "xp_reward": 200
    }
]

# Comprehensive quiz data covering all 100 questions
QUIZ_DATA = {
    "indigenous_peoples_quiz": {
        "title": "Michigan's First Residents Quiz",
        "questions": [
            {
                "question": "What was the land that became Michigan inhabited by before Europeans arrived?",
                "options": ["Empty wilderness", "Various Native American peoples", "French settlers", "Spanish explorers"],
                "correct": 1,
                "explanation": "Michigan was inhabited by various indigenous peoples for thousands of years before European contact."
            },
            {
                "question": "Why did Europeans initially call Native Americans 'Indians'?",
                "options": ["It was their actual name", "Columbus thought he reached the East Indies", "It was a Spanish word", "They called themselves that"],
                "correct": 1,
                "explanation": "Columbus mistakenly believed he had reached the East Indies, leading to the persistent misnomer 'Indians.'"
            },
            {
                "question": "What has been the most common assumption about how people originally came to the Americas?",
                "options": ["By boat across the Atlantic", "Via a land bridge from Asia", "From South America northward", "They evolved there"],
                "correct": 1,
                "explanation": "The traditional theory suggests people crossed a land bridge (Beringia) from Asia during ice ages."
            },
            {
                "question": "According to recent archaeological discoveries, how long might humans have been in the Americas?",
                "options": ["5,000 years", "12,000 years", "20,000-40,000 years", "100,000 years"],
                "correct": 2,
                "explanation": "New discoveries suggest much earlier human presence than previously assumed, possibly 20,000-40,000 years or more."
            },
            {
                "question": "What geographical feature supposedly connected Asia to the Americas?",
                "options": ["An ice sheet", "A land bridge", "A chain of islands", "A shallow sea"],
                "correct": 1,
                "explanation": "The Bering land bridge (Beringia) connected Asia and North America during periods of lower sea level."
            }
        ]
    },
    "british_colonial_quiz": {
        "title": "British Colonial Period Quiz",
        "questions": [
            {
                "question": "Under whose flag did British control of Michigan occur?",
                "options": ["King George II", "King George III", "Queen Anne", "King William"],
                "correct": 1,
                "explanation": "British control of Michigan occurred under King George III during and after the French and Indian War."
            },
            {
                "question": "Who was the British commander mentioned as reaching Detroit in 1764?",
                "options": ["Colonel Bouquet", "General Amherst", "Colonel Bradstreet", "Major Gladwin"],
                "correct": 2,
                "explanation": "Colonel John Bradstreet reached Detroit on August 26, 1764, as part of British efforts to secure the region."
            },
            {
                "question": "What did the assembled western tribes acknowledge in 1764?",
                "options": ["French sovereignty", "Spanish rule", "The sovereignty of King George", "Independence"],
                "correct": 2,
                "explanation": "Western tribes assembled and acknowledged the sovereignty of King George III as part of peace negotiations."
            },
            {
                "question": "Who presided over the peace arrangements with Native Americans?",
                "options": ["Colonel Bouquet", "Sir William Johnson", "General Gage", "Colonel Bradstreet"],
                "correct": 1,
                "explanation": "Sir William Johnson, British Superintendent of Indian Affairs, presided over important peace arrangements."
            },
            {
                "question": "Where did Johnson put the finishing touches on peace arrangements in July 1766?",
                "options": ["Detroit", "Fort Pitt", "Oswego, New York", "Quebec"],
                "correct": 2,
                "explanation": "The final peace council was held at Oswego, New York in July 1766."
            }
        ]
    },
    "revolutionary_period_quiz": {
        "title": "Revolutionary Period and Transition Quiz",
        "questions": [
            {
                "question": "What happened to Pontiac in the spring of 1769?",
                "options": ["He died of disease", "He was murdered", "He moved west", "He became a British ally"],
                "correct": 1,
                "explanation": "Pontiac was murdered in 1769, ending the life of this significant Native American leader."
            },
            {
                "question": "Where was Pontiac murdered and buried?",
                "options": ["Detroit", "St. Louis", "Chicago", "Green Bay"],
                "correct": 1,
                "explanation": "Pontiac was murdered and buried in St. Louis (then under Spanish control)."
            },
            {
                "question": "Who was known as the 'father of the lake region' in the nineteenth century?",
                "options": ["Pontiac", "Charles Langlade", "William Howard", "Henry Gladwin"],
                "correct": 2,
                "explanation": "William Howard became known as the 'father of the lake region' for his long service and influence."
            },
            {
                "question": "What did Captain William Howard do before the Indian uprising?",
                "options": ["Served as a trader", "Made a plan to save the garrison", "Worked as a missionary", "Lived as a farmer"],
                "correct": 1,
                "explanation": "Howard had made plans before the uprising that helped him respond effectively to save the British garrison."
            },
            {
                "question": "During which conflict did Howard fight with the British against Americans?",
                "options": ["French and Indian War", "Pontiac's Rebellion", "American Revolution", "War of 1812"],
                "correct": 2,
                "explanation": "Howard fought with the British during the American Revolution before eventually being reconciled to American control."
            }
        ]
    },
    "comprehensive_final": {
        "title": "Comprehensive Final Assessment",
        "questions": [
            {
                "question": "Which three major powers controlled Michigan during the periods we studied?",
                "options": ["Spanish, British, American", "French, British, American", "Dutch, French, British", "British, American, Canadian"],
                "correct": 1,
                "explanation": "Michigan was controlled successively by French, British, and American powers during the colonial and early national periods."
            },
            {
                "question": "What was the primary economic activity that connected Native Americans to European colonial systems?",
                "options": ["Agriculture", "Mining", "Fur trading", "Fishing"],
                "correct": 2,
                "explanation": "The fur trade was the primary economic connection between Native Americans and European colonizers."
            },
            {
                "question": "Which treaty ended French control of Michigan?",
                "options": ["Treaty of Paris (1763)", "Treaty of Utrecht", "Jay's Treaty", "Treaty of Ghent"],
                "correct": 0,
                "explanation": "The Treaty of Paris (1763) ended the French and Indian War and transferred French territories to Britain."
            },
            {
                "question": "What was the significance of Detroit throughout these periods?",
                "options": ["It was the largest city", "It was a strategic military and trading center", "It was the colonial capital", "It was the main port"],
                "correct": 1,
                "explanation": "Detroit's location made it a crucial strategic military and trading center throughout the colonial period."
            },
            {
                "question": "How did the American Revolution affect Michigan?",
                "options": ["It gained immediate independence", "It remained under British control during the war", "It was abandoned", "It became Spanish territory"],
                "correct": 1,
                "explanation": "Michigan remained under British control throughout the American Revolution, only transferring to American control later."
            }
        ]
    }
}

# XP and Achievement System
def award_xp(amount: int, reason: str = ""):
    """Award XP and check for achievements"""
    st.session_state.total_xp += amount
    
    # Check for level-based achievements
    if st.session_state.total_xp >= 1000 and "History Master" not in st.session_state.achievements:
        st.session_state.achievements.append("History Master")
        st.balloons()
        st.success("🏆 Achievement Unlocked: History Master! (1000+ XP)")
    
    elif st.session_state.total_xp >= 500 and "Scholar" not in st.session_state.achievements:
        st.session_state.achievements.append("Scholar")
        st.success("🎓 Achievement Unlocked: Scholar! (500+ XP)")
    
    elif st.session_state.total_xp >= 200 and "Student" not in st.session_state.achievements:
        st.session_state.achievements.append("Student")
        st.success("📚 Achievement Unlocked: Student! (200+ XP)")
    
    # XP notification
    if amount > 0:
        st.success(f"🌟 +{amount} XP earned! {reason}")

def display_slide(slide_data: dict) -> None:
    """Display a slide with enhanced formatting and XP rewards"""
    
    # Main content
    st.markdown(slide_data["content"])
    
    # XP reward for viewing
    if f"viewed_{slide_data['id']}" not in st.session_state:
        award_xp(slide_data.get("xp_reward", 25), f"Viewing {slide_data['title']}")
        st.session_state[f"viewed_{slide_data['id']}"] = True
    
    # Interactive elements
    if slide_data.get("interactive"):
        st.markdown("---")
        
        if "discussion_prompt" in slide_data:
            st.markdown("### 💭 Critical Thinking Discussion:")
            st.info(slide_data["discussion_prompt"])
            
            # Response area
            response_key = f"response_{slide_data['id']}"
            response = st.text_area(
                "Share your analysis:",
                key=response_key,
                placeholder="Provide a thoughtful historical analysis...",
                height=120
            )
            
            if response and len(response.split()) >= 50:  # Minimum 50 words for XP
                if st.button(f"Submit Response", key=f"save_{slide_data['id']}"):
                    st.session_state.student_responses[response_key] = {
                        'response': response,
                        'timestamp': datetime.now().isoformat(),
                        'slide': slide_data['title'],
                        'word_count': len(response.split())
                    }
                    award_xp(75, "Thoughtful discussion response")
                    st.success("Response submitted! Great historical thinking! 🎓")
            elif response:
                st.warning("Please provide a more detailed response (at least 50 words) for XP credit.")

def display_quiz(quiz_id: str) -> None:
    """Display an interactive quiz with XP rewards and celebrations"""
    
    if quiz_id not in QUIZ_DATA:
        st.error("Quiz not found!")
        return
    
    quiz = QUIZ_DATA[quiz_id]
    st.markdown(f"## 📝 {quiz['title']}")
    st.markdown("Test your knowledge and earn XP!")
    
    with st.form(f"quiz_{quiz_id}"):
        answers = {}
        
        for i, q in enumerate(quiz["questions"]):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            
            answer = st.radio(
                "Choose your answer:",
                options=q["options"],
                key=f"q_{quiz_id}_{i}",
                index=None
            )
            
            if answer is not None:
                answers[i] = q["options"].index(answer)
        
        submitted = st.form_submit_button("🎯 Submit Quiz")
        
        if submitted and len(answers) == len(quiz["questions"]):
            # Grade the quiz
            correct_count = 0
            total_questions = len(quiz["questions"])
            
            st.markdown("---")
            st.markdown("### 📊 Quiz Results:")
            
            for i, q in enumerate(quiz["questions"]):
                if i in answers:
                    is_correct = answers[i] == q["correct"]
                    if is_correct:
                        correct_count += 1
                        st.success(f"✅ Question {i+1}: Correct! (+10 XP)")
                    else:
                        st.error(f"❌ Question {i+1}: Incorrect")
                        st.info(f"**Correct answer:** {q['options'][q['correct']]}")
                    
                    with st.expander(f"Historical Context for Question {i+1}"):
                        st.markdown(q['explanation'])
            
            # Overall score and XP calculation
            score_pct = (correct_count / total_questions) * 100
            base_xp = correct_count * 10
            bonus_xp = 0
            
            # Performance bonuses
            if score_pct == 100:
                bonus_xp = 100
                st.balloons()  # Celebration for perfect score
                st.success("🎉 PERFECT SCORE! Outstanding historical knowledge!")
                if "Perfectionist" not in st.session_state.achievements:
                    st.session_state.achievements.append("Perfectionist")
                    st.success("🏆 Achievement Unlocked: Perfectionist!")
            elif score_pct >= 80:
                bonus_xp = 50
                st.success("🌟 Excellent work! You've mastered this material!")
            elif score_pct >= 60:
                bonus_xp = 25
                st.success("📚 Good understanding! Keep studying!")
            else:
                st.warning("📖 Review the material and try again for more XP!")
            
            total_xp_earned = base_xp + bonus_xp
            st.session_state.quiz_scores[quiz_id] = score_pct
            
            if total_xp_earned > 0:
                award_xp(total_xp_earned, f"Quiz completion: {score_pct:.0f}%")
            
            # Streak tracking
            if score_pct >= 70:
                st.session_state.current_streak += 1
                if st.session_state.current_streak >= 3 and "On Fire" not in st.session_state.achievements:
                    st.session_state.achievements.append("On Fire")
                    st.success("🔥 Achievement Unlocked: On Fire! (3 quiz streak)")
            else:
                st.session_state.current_streak = 0

def display_progress_dashboard():
    """Display student progress and achievements"""
    
    st.markdown("# 📊 Your Learning Progress")
    st.markdown("Track your journey through Michigan history!")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total XP", st.session_state.total_xp)
    
    with col2:
        quiz_completion = len(st.session_state.quiz_scores) / len(QUIZ_DATA) * 100
        st.metric("Quiz Completion", f"{quiz_completion:.0f}%")
    
    with col3:
        avg_score = sum(st.session_state.quiz_scores.values()) / len(st.session_state.quiz_scores) if st.session_state.quiz_scores else 0
        st.metric("Average Quiz Score", f"{avg_score:.0f}%")
    
    with col4:
        st.metric("Current Streak", st.session_state.current_streak)
    
    # XP Progress Bar
    st.markdown("### XP Progress to Next Level")
    levels = [0, 200, 500, 1000, 2000]
    current_level = 0
    next_level_xp = 200
    
    for i, level in enumerate(levels):
        if st.session_state.total_xp >= level:
            current_level = i
            next_level_xp = levels[i + 1] if i + 1 < len(levels) else levels[-1]
    
    progress = min(st.session_state.total_xp / next_level_xp, 1.0)
    st.progress(progress)
    st.caption(f"Level {current_level + 1} - {st.session_state.total_xp}/{next_level_xp} XP")
    
    # Achievements
    if st.session_state.achievements:
        st.markdown("### 🏆 Your Achievements")
        achievement_cols = st.columns(3)
        for i, achievement in enumerate(st.session_state.achievements):
            with achievement_cols[i % 3]:
                st.success(f"🏆 {achievement}")
    
    # Detailed Quiz Results
    if st.session_state.quiz_scores:
        st.markdown("### 📝 Quiz Performance")
        
        for quiz_id, score in st.session_state.quiz_scores.items():
            quiz_title = QUIZ_DATA[quiz_id]["title"]
            
            if score >= 90:
                st.success(f"🌟 {quiz_title}: {score:.0f}% - Excellent mastery!")
            elif score >= 80:
                st.success(f"✅ {quiz_title}: {score:.0f}% - Strong understanding!")
            elif score >= 70:
                st.info(f"📚 {quiz_title}: {score:.0f}% - Good progress!")
            elif score >= 60:
                st.warning(f"⚠️ {quiz_title}: {score:.0f}% - Needs review")
            else:
                st.error(f"❌ {quiz_title}: {score:.0f}% - Requires attention")

def sidebar_navigation() -> str:
    """Enhanced sidebar with XP tracking"""
    
    st.sidebar.markdown("# 🏛️ HIS220: Michigan History")
    st.sidebar.markdown("### CognitiveCloud.ai Learning Platform")
    
    # XP Display
    st.sidebar.markdown(f"### 🌟 Your XP: {st.session_state.total_xp}")
    
    # Mode selection
    mode = st.sidebar.radio(
        "Learning Mode:",
        ["📚 Course Lectures", "📝 Knowledge Quizzes", "📊 Progress Dashboard", "📖 Study Resources"]
    )
    
    if mode == "📚 Course Lectures":
        st.sidebar.markdown("## Module Navigation")
        
        # Slide selector
        slide_titles = [f"Module {i+1}: {slide['title']}" for i, slide in enumerate(SLIDES)]
        selected_slide = st.sidebar.selectbox(
            "Jump to module:",
            options=range(len(SLIDES)),
            format_func=lambda x: slide_titles[x],
            index=st.session_state.current_slide
        )
        
        if selected_slide != st.session_state.current_slide:
            st.session_state.current_slide = selected_slide
        
        # Navigation buttons
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("⬅️ Previous") and st.session_state.current_slide > 0:
                st.session_state.current_slide -= 1
                st.rerun()
        
        with col2:
            if st.button("Next ➡️") and st.session_state.current_slide < len(SLIDES) - 1:
                st.session_state.current_slide += 1
                st.rerun()
        
        # Progress
        progress = (st.session_state.current_slide + 1) / len(SLIDES)
        st.sidebar.progress(progress)
        st.sidebar.caption(f"Module {st.session_state.current_slide + 1} of {len(SLIDES)}")
    
    elif mode == "📝 Knowledge Quizzes":
        st.sidebar.markdown("## Available Quizzes")
        
        for quiz_id, quiz in QUIZ_DATA.items():
            if quiz_id in st.session_state.quiz_scores:
                score = st.session_state.quiz_scores[quiz_id]
                if score >= 90:
                    st.sidebar.markdown(f"🌟 {quiz['title']}: {score:.0f}%")
                elif score >= 70:
                    st.sidebar.markdown(f"✅ {quiz['title']}: {score:.0f}%")
                else:
                    st.sidebar.markdown(f"📚 {quiz['title']}: {score:.0f}%")
            else:
                st.sidebar.markdown(f"⏳ {quiz['title']}: Not attempted")
    
    # Achievements display
    if st.session_state.achievements:
        st.sidebar.markdown("### 🏆 Recent Achievements")
        for achievement in st.session_state.achievements[-3:]:  # Show last 3
            st.sidebar.success(f"🏆 {achievement}")
    
    return mode.split()[1].lower()

def display_study_resources():
    """Display comprehensive study resources"""
    
    st.markdown("# 📖 HIS220 Study Resources")
    st.markdown("Enhance your understanding of Michigan history with these curated resources.")
    
    # Primary Sources
    st.markdown("## 📜 Primary Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Colonial Documents")
        st.markdown("- **Treaty of Paris (1763)** - Ended French rule in North America")
        st.markdown("- **Royal Proclamation of 1763** - Limited westward expansion")
        st.markdown("- **Pontiac's Speeches** - Recorded diplomatic negotiations")
        st.markdown("- **British Military Reports** - Contemporary accounts of conflicts")
        
        st.markdown("### Archaeological Evidence")
        st.markdown("- **Radiocarbon Dating Results** - Evidence of early human presence")
        st.markdown("- **Artifact Collections** - Tools and pottery from indigenous peoples")
        st.markdown("- **Site Reports** - Excavations across Michigan")
    
    with col2:
        st.markdown("### Maps and Visual Sources")
        st.markdown("- **French Colonial Maps** - Show early European understanding")
        st.markdown("- **British Military Maps** - Strategic locations and routes")
        st.markdown("- **Native American Territory Maps** - Tribal boundaries and movements")
        
        st.markdown("### Oral Histories")
        st.markdown("- **Native American Traditions** - Stories passed down through generations")
        st.markdown("- **French Voyageur Accounts** - Tales of early exploration")
        st.markdown("- **British Settler Narratives** - Colonial experiences")
    
    # Secondary Sources
    st.markdown("## 📚 Scholarly Resources")
    
    study_materials = [
        {
            "title": "Michigan History Timeline",
            "description": "Interactive timeline covering pre-contact to statehood",
            "type": "Visual Resource"
        },
        {
            "title": "Native American Tribes of Michigan",
            "description": "Comprehensive guide to Ojibwe, Ottawa, and Potawatomi peoples",
            "type": "Cultural Studies"
        },
        {
            "title": "Colonial Conflicts Database",
            "description": "Detailed records of Pontiac's Rebellion and other conflicts",
            "type": "Military History"
        },
        {
            "title": "Archaeological Discovery Updates",
            "description": "Latest findings challenging traditional migration theories",
            "type": "Archaeology"
        }
    ]
    
    for resource in study_materials:
        with st.expander(f"📖 {resource['title']} - {resource['type']}"):
            st.markdown(resource['description'])
    
    # Study Tips
    st.markdown("## 🎯 Study Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Historical Thinking Skills")
        st.markdown("- **Chronological Reasoning** - Understand cause and effect over time")
        st.markdown("- **Source Analysis** - Evaluate reliability and bias in documents")
        st.markdown("- **Multiple Perspectives** - Consider different cultural viewpoints")
        st.markdown("- **Historical Context** - Place events in their proper setting")
    
    with col2:
        st.markdown("### Exam Preparation")
        st.markdown("- **Timeline Creation** - Make visual chronologies of major events")
        st.markdown("- **Concept Mapping** - Connect related ideas and themes")
        st.markdown("- **Practice Essays** - Write analytical responses to historical questions")
        st.markdown("- **Group Discussions** - Debate different interpretations")

def main():
    """Main application function with enhanced XP system"""
    
    # Custom CSS for CognitiveCloud.ai branding
    st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 2px solid #1f77b4;
        background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%);
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff7f0e 0%, #1f77b4 100%);
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .history-module {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .xp-notification {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #333;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
    .achievement-badge {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with branding
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>🏛️ HIS220: Michigan History</h1>
        <h3 style='color: #E8E8E8; margin: 10px 0 0 0;'>CognitiveCloud.ai Learning Platform</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Determine current mode
    current_mode = sidebar_navigation()
    
    if current_mode == "course":
        # Display current slide
        current_slide = SLIDES[st.session_state.current_slide]
        display_slide(current_slide)
        
        # Navigation controls at bottom
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.current_slide > 0:
                if st.button("⬅️ Previous Module"):
                    st.session_state.current_slide -= 1
                    st.rerun()
        
        with col3:
            if st.session_state.current_slide < len(SLIDES) - 1:
                if st.button("Next Module ➡️"):
                    st.session_state.current_slide += 1
                    st.rerun()
            elif st.session_state.current_slide == len(SLIDES) - 1:
                if st.button("🎓 Complete Course"):
                    if "Course Completed" not in st.session_state.achievements:
                        st.session_state.achievements.append("Course Completed")
                        award_xp(300, "Course completion bonus!")
                        st.balloons()
                        st.success("🎉 Congratulations! You've completed HIS220: Michigan History!")
        
        with col2:
            # Progress indicator
            progress = (st.session_state.current_slide + 1) / len(SLIDES)
            st.progress(progress)
            st.caption(f"Module {st.session_state.current_slide + 1} of {len(SLIDES)}")
    
    elif current_mode == "knowledge":
        st.markdown("# 📝 Knowledge Assessment Center")
        st.markdown("Test your mastery of Michigan history and earn XP!")
        
        # Quiz selection with difficulty indicators
        quiz_options = []
        for quiz_id, quiz in QUIZ_DATA.items():
            difficulty = "🟢 Beginner" if "indigenous" in quiz_id else "🟡 Intermediate" if "british" in quiz_id or "revolutionary" in quiz_id else "🔴 Advanced"
            quiz_options.append(f"{difficulty} - {quiz['title']}")
        
        selected_option = st.selectbox("Select a quiz:", quiz_options)
        quiz_choice = list(QUIZ_DATA.keys())[quiz_options.index(selected_option)]
        
        # Display quiz
        display_quiz(quiz_choice)
        
        # Quiz statistics
        if st.session_state.quiz_scores:
            st.markdown("---")
            st.markdown("## 📈 Your Quiz Statistics")
            
            total_quizzes = len(QUIZ_DATA)
            completed_quizzes = len(st.session_state.quiz_scores)
            avg_score = sum(st.session_state.quiz_scores.values()) / completed_quizzes if completed_quizzes > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Quizzes Completed", f"{completed_quizzes}/{total_quizzes}")
            with col2:
                st.metric("Average Score", f"{avg_score:.1f}%")
            with col3:
                st.metric("Quiz Streak", st.session_state.current_streak)
    
    elif current_mode == "progress":
        display_progress_dashboard()
        
        # Export progress data
        if st.button("💾 Export Learning Progress"):
            export_data = {
                'course': 'HIS220',
                'student_id': f"student_{hash(str(st.session_state)) % 10000}",
                'total_xp': st.session_state.total_xp,
                'achievements': st.session_state.achievements,
                'quiz_scores': st.session_state.quiz_scores,
                'student_responses': st.session_state.student_responses,
                'current_streak': st.session_state.current_streak,
                'export_timestamp': datetime.now().isoformat()
            }
            
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                "📊 Download Progress Report",
                json_str,
                file_name=f"HIS220_progress_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    elif current_mode == "study":
        display_study_resources()
    
    # Footer with course info
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;'>
        <p><strong>HIS220: Michigan History</strong> | CognitiveCloud.ai Learning Platform</p>
        <p>Understanding Michigan's past to inform its future</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
