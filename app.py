"""
HIS220: Michigan History - Single 100-Question Quiz
Maximum XP Challenge - CognitiveCloud.ai Learning Platform
"""

import streamlit as st
import time
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="HIS220: 100-Question Challenge",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'total_xp' not in st.session_state:
    st.session_state.total_xp = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'final_score' not in st.session_state:
    st.session_state.final_score = 0

# Complete 100 Questions in Sequential Order
QUESTIONS = [
    # Questions 1-25: Early Settlement and Native Americans
    {
        "question": "What was the land that became Michigan inhabited by before Europeans arrived?",
        "options": ["Empty wilderness", "Various Native American peoples", "French settlers", "Spanish explorers"],
        "correct": 1,
        "explanation": "Colonial governors and Indian agents like Sir William Johnson played crucial governance roles."
    },
    {
        "question": "How did the transition from French to British rule occur?",
        "options": ["Peacefully through treaty", "Through military conquest and negotiation", "French abandoned the region", "Native Americans chose British rule"],
        "correct": 1,
        "explanation": "The transition involved military conquest during the French and Indian War followed by negotiations."
    },
    {
        "question": "What long-term impacts did British control have on Michigan's development?",
        "options": ["No lasting impact", "Established administrative and legal foundations", "Only military influence", "Reversed French policies entirely"],
        "correct": 1,
        "explanation": "British control established important administrative, legal, and territorial foundations for future development."
    }
]

# Maximum XP Achievement System
def award_xp(amount: int, reason: str = ""):
    """Award maximum XP with spectacular celebrations"""
    st.session_state.total_xp += amount
    
    milestones = [
        (500, "Rising Scholar"),
        (1000, "History Enthusiast"),
        (1500, "Michigan Expert"),
        (2000, "Colonial Period Master"),
        (2500, "Historical Analyst"),
        (3000, "ULTIMATE MICHIGAN HISTORY CHAMPION")
    ]
    
    for threshold, title in milestones:
        if st.session_state.total_xp >= threshold and title not in st.session_state.achievements:
            st.session_state.achievements.append(title)
            if threshold >= 2000:
                st.balloons()
                st.success(f"🏆 LEGENDARY ACHIEVEMENT: {title}! ({threshold}+ XP)")
            else:
                st.success(f"🎖️ Achievement: {title}! ({threshold}+ XP)")
    
    if amount > 0:
        st.success(f"⭐ +{amount} XP earned! {reason}")

def display_100_question_quiz():
    """Display the complete 100-question quiz"""
    
    st.markdown("# 🏛️ The Ultimate Michigan History Challenge")
    st.markdown("## 100 Questions - Maximum XP - Epic Achievements")
    st.markdown("**Test your mastery of Michigan's First Residents and Colonial Period!**")
    
    if not st.session_state.quiz_started:
        st.markdown("""
        ### 🎯 Challenge Overview:
        - **100 Sequential Questions** covering all major topics
        - **Maximum XP Rewards**: Up to 3,000+ XP possible
        - **Epic Achievements**: Unlock legendary titles
        
        ### 🏆 XP Scoring System:
        - **Perfect Score (100%)**: 1,500 XP + 500 Bonus = **2,000 XP**
        - **Excellent (90-99%)**: 1,350-1,485 XP + 300 Bonus
        - **Very Good (80-89%)**: 1,200-1,335 XP + 200 Bonus
        
        ### 🎉 Special Achievements:
        - **Perfect Century**: 100% score
        - **Speed Demon**: Complete in under 30 minutes
        - **Michigan Master**: Achieve ultimate XP threshold
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 BEGIN 100-QUESTION CHALLENGE", key="start_quiz"):
                st.session_state.quiz_started = True
                st.session_state.start_time = time.time()
                st.rerun()
        return
    
    if st.session_state.quiz_completed:
        display_final_results()
        return
    
    progress = len(st.session_state.answers) / 100
    st.progress(progress)
    st.caption(f"Progress: {len(st.session_state.answers)}/100 questions answered")
    
    if hasattr(st.session_state, 'start_time'):
        elapsed_time = time.time() - st.session_state.start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        st.markdown(f"**Time Elapsed: {minutes:02d}:{seconds:02d}**")
    
    with st.form("complete_100_quiz"):
        st.markdown("### Answer all 100 questions:")
        
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            answer = st.radio(
                "Choose your answer:",
                options=q["options"],
                key=f"question_{i}",
                index=st.session_state.answers.get(i, None)
            )
            
            if answer is not None:
                st.session_state.answers[i] = q["options"].index(answer)
            
            st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🎯 SUBMIT COMPLETE QUIZ")
        
        if submitted and len(st.session_state.answers) == 100:
            process_quiz_results()

def process_quiz_results():
    """Process quiz with maximum XP"""
    correct_count = sum(1 for i, q in enumerate(QUESTIONS) 
                       if i in st.session_state.answers and st.session_state.answers[i] == q["correct"])
    
    completion_time = (time.time() - st.session_state.start_time) / 60 if hasattr(st.session_state, 'start_time') else 0
    
    st.session_state.final_score = (correct_count / 100) * 100
    st.session_state.correct_count = correct_count
    st.session_state.completion_time = completion_time
    st.session_state.quiz_completed = True
    
    base_xp = correct_count * 15
    performance_bonus = 0
    special_bonuses = 0
    
    score_pct = st.session_state.final_score
    if score_pct == 100:
        performance_bonus = 500
        st.balloons()
        if "Perfect Century" not in st.session_state.achievements:
            st.session_state.achievements.append("Perfect Century")
            special_bonuses += 200
    elif score_pct >= 95:
        performance_bonus = 400
    elif score_pct >= 90:
        performance_bonus = 300
    elif score_pct >= 80:
        performance_bonus = 200
    elif score_pct >= 70:
        performance_bonus = 100
    elif score_pct >= 60:
        performance_bonus = 50
    
    if completion_time < 30 and score_pct >= 80:
        if "Speed Demon" not in st.session_state.achievements:
            st.session_state.achievements.append("Speed Demon")
            special_bonuses += 150
    
    if "Century Club Champion" not in st.session_state.achievements:
        st.session_state.achievements.append("Century Club Champion")
        special_bonuses += 100
    
    total_xp = base_xp + performance_bonus + special_bonuses
    award_xp(total_xp, f"Challenge Complete: {score_pct:.1f}%")
    st.rerun()

def display_final_results():
    """Display final results"""
    st.markdown("# 🎉 CHALLENGE COMPLETE!")
    st.markdown("## Your Michigan History Results")
    
    score_pct = st.session_state.final_score
    correct_count = st.session_state.correct_count
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Final Score", f"{score_pct:.1f}%", delta=f"{correct_count}/100")
    with col2:
        st.metric("Time", f"{st.session_state.completion_time:.1f} min")
    with col3:
        st.metric("Total XP", st.session_state.total_xp)
    with col4:
        st.metric("Achievements", len(st.session_state.achievements))
    
    st.markdown("### 📊 Performance Analysis")
    
    if score_pct == 100:
        st.success("🏆 PERFECT SCORE! You are a MICHIGAN HISTORY MASTER!")
        st.balloons()
    elif score_pct >= 90:
        st.success("⭐ EXCELLENT! Exceptional knowledge!")
    elif score_pct >= 80:
        st.info("📚 GOOD WORK! Strong understanding!")
    elif score_pct >= 70:
        st.info("📖 FAIR! Continue studying!")
    else:
        st.warning("📝 Review the material and try again!")
    
    with st.expander("🔍 Question Analysis"):
        for i, q in enumerate(QUESTIONS):
            user_answer = st.session_state.answers.get(i)
            if user_answer == q["correct"]:
                st.success(f"✅ Q{i+1}: CORRECT")
            else:
                st.error(f"❌ Q{i+1}: INCORRECT")
                st.info(f"Correct: {q['options'][q['correct']]}")
            with st.expander(f"Context - Q{i+1}"):
                st.markdown(f"**{q['question']}**")
                st.markdown(f"{q['explanation']}")
    
    if st.session_state.achievements:
        st.markdown("### 🏆 Achievements")
        for achievement in st.session_state.achievements:
            st.success(f"🏆 {achievement}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 RETAKE CHALLENGE"):
            st.session_state.quiz_started = False
            st.session_state.answers = {}
            st.session_state.quiz_completed = False
            st.session_state.final_score = 0
            st.rerun()

def main():
    """Main application"""
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 1rem;
        border: none;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%); 
                color: white; padding: 30px; border-radius: 20px; text-align: center; margin: 20px 0;'>
        <h1>🏛️ HIS220: ULTIMATE MICHIGAN HISTORY CHALLENGE</h1>
        <h2>100 Questions • Maximum XP • Legendary Achievements</h2>
        <h3>CognitiveCloud.ai Learning Platform</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("# 🎯 Challenge Status")
    st.sidebar.metric("Total XP", st.session_state.total_xp)
    st.sidebar.metric("Achievements", len(st.session_state.achievements))
    
    if st.session_state.quiz_completed:
        st.sidebar.metric("Final Score", f"{st.session_state.final_score:.1f}%")
        st.sidebar.metric("Correct", f"{st.session_state.correct_count}/100")
    
    if st.session_state.achievements:
        st.sidebar.markdown("### 🏆 Recent Achievements")
        for achievement in st.session_state.achievements[-3:]:
            st.sidebar.success(f"🏆 {achievement}")
    
    display_100_question_quiz()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: #1f1f1f; 
                color: white; border-radius: 15px;'>
        <h3>🏛️ MICHIGAN HISTORY ULTIMATE CHALLENGE</h3>
        <p><strong>100 Questions • Complete Mastery • Maximum XP</strong></p>
        <p>CognitiveCloud.ai Learning Platform - HIS220</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
explanation": "Michigan was inhabited by various indigenous peoples for thousands of years before European contact."
    },
    {
        "question": "Why did Europeans initially call Native Americans 'Indians'?",
        "options": ["It was their actual name", "Columbus thought he reached the East Indies", "It was a Spanish word", "They called themselves that"],
        "correct": 1,
        "explanation": "Columbus mistakenly believed he had reached the East Indies, leading to the persistent misnomer 'Indians.'"
    },
    {
        "question": "What was Columbus's mistaken belief that led to the term 'Indians'?",
        "options": ["He thought they were from India", "He believed he reached the East Indies", "He confused them with Indonesian peoples", "He thought they were Spanish"],
        "correct": 1,
        "explanation": "Columbus believed he had reached the Indies when he encountered the Americas."
    },
    {
        "question": "According to the text, what name has persisted for over a century after Columbus?",
        "options": ["Americans", "Indians", "Natives", "Aboriginals"],
        "correct": 1,
        "explanation": "The term 'Indians' persisted despite being based on Columbus's geographical error."
    },
    {
        "question": "How long have misnomers about Native Americans been used in Michigan?",
        "options": ["Decades", "Over a century", "A few years", "Since statehood"],
        "correct": 1,
        "explanation": "The text indicates these naming errors have persisted for over a century."
    },
    {
        "question": "What did Europeans believe about the land when they first arrived?",
        "options": ["It was densely populated", "It was mostly uninhabited", "It belonged to Spain", "It was claimed by France"],
        "correct": 1,
        "explanation": "Europeans often viewed the land as empty or sparsely populated, ignoring indigenous presence."
    },
    {
        "question": "Which French explorers are mentioned as having contact with Michigan's indigenous peoples?",
        "options": ["Cartier and Champlain", "The French found in Michigan", "Marquette and Joliet", "La Salle and Cadillac"],
        "correct": 1,
        "explanation": "The text mentions French contact with indigenous peoples in the Michigan region."
    },
    {
        "question": "What assumption about human migration to the Americas has been challenged?",
        "options": ["That it happened recently", "Traditional timing estimates", "That it came from Europe", "That it was by boat"],
        "correct": 1,
        "explanation": "Recent discoveries have challenged traditional assumptions about when humans first arrived."
    },
    {
        "question": "What was the most common assumption about how people originally came to the Western Hemisphere?",
        "options": ["By boat", "Via a land bridge from Asia", "From Europe", "They evolved there"],
        "correct": 1,
        "explanation": "The traditional theory suggests people crossed a land bridge from Asia during ice ages."
    },
    {
        "question": "How did early peoples supposedly cross into the Americas according to traditional theories?",
        "options": ["By boat across the Pacific", "Via the Bering land bridge", "Across the Atlantic", "Through Central America"],
        "correct": 1,
        "explanation": "The Bering land bridge theory was the traditional explanation for human migration to the Americas."
    },
    {
        "question": "What geographical feature connected Asia to the Americas during ancient times?",
        "options": ["An ice sheet", "The Bering land bridge", "A chain of islands", "A frozen ocean"],
        "correct": 1,
        "explanation": "The Bering land bridge (Beringia) connected Asia and North America during periods of lower sea level."
    },
    {
        "question": "At what times in the past was this land bridge supposedly accessible?",
        "options": ["During warm periods", "During ice ages", "Every winter", "Only in summer"],
        "correct": 1,
        "explanation": "Lower sea levels during ice ages would have exposed the land bridge."
    },
    {
        "question": "What prevented travel between the hemispheres according to the text?",
        "options": ["Mountains", "Desert", "A narrow waterway", "Dense forests"],
        "correct": 2,
        "explanation": "The text mentions a narrow waterway that prevented easy travel between continents."
    },
    {
        "question": "Why was the narrow waterway between continents significant?",
        "options": ["It was too deep", "It blocked migration", "It was always frozen", "It had strong currents"],
        "correct": 1,
        "explanation": "The waterway served as a barrier to movement between the hemispheres."
    },
    {
        "question": "What methods of determining age are mentioned in relation to archaeological discoveries?",
        "options": ["Tree ring dating", "Radiocarbon dating", "Pottery analysis", "Geological layers"],
        "correct": 1,
        "explanation": "The text specifically mentions radiocarbon dating as a method for determining age."
    },
    {
        "question": "What dating technique involving radiocarbon is referenced?",
        "options": ["Carbon-14 testing", "Radiocarbon dating", "Carbon analysis", "Isotope dating"],
        "correct": 1,
        "explanation": "Radiocarbon dating is the specific technique mentioned in the text."
    },
    {
        "question": "How have comparative studies of primitive vessels contributed to archaeological understanding?",
        "options": ["They show trade routes", "They help with dating", "They reveal migration patterns", "They indicate cultural connections"],
        "correct": 1,
        "explanation": "Comparative studies help archaeologists understand chronology and dating."
    },
    {
        "question": "What new discoveries have resulted in important changes to historical timelines?",
        "options": ["Pottery finds", "Archaeological discoveries", "Written records", "Oral histories"],
        "correct": 1,
        "explanation": "Archaeological discoveries have pushed back estimates of human presence in the Americas."
    },
    {
        "question": "In what decade did archaeological discoveries begin pushing back settlement estimates?",
        "options": ["1920s", "1940s", "1960s", "1980s"],
        "correct": 1,
        "explanation": "The text mentions discoveries in the 1940s that began changing our understanding."
    },
    {
        "question": "What was the previous assumption about when humans first arrived in the hemisphere?",
        "options": ["5,000 years ago", "Much more recently", "10,000 years ago", "50,000 years ago"],
        "correct": 1,
        "explanation": "Earlier estimates were much more recent than current archaeological evidence suggests."
    },
    {
        "question": "Where have archaeological discoveries suggested earlier human presence?",
        "options": ["Only in Michigan", "California and Mexico", "Only in Canada", "Throughout the Midwest"],
        "correct": 1,
        "explanation": "The text specifically mentions discoveries in California and Mexico."
    },
    {
        "question": "What areas are mentioned as having evidence of early human habitation?",
        "options": ["Great Lakes region", "California and Mexico", "Eastern seaboard", "Pacific Northwest"],
        "correct": 1,
        "explanation": "California and Mexico are specifically cited as areas with early evidence."
    },
    {
        "question": "What time range do some discoveries suggest for human presence?",
        "options": ["5,000-10,000 years", "20,000-40,000 years", "50,000-100,000 years", "1,000-5,000 years"],
        "correct": 1,
        "explanation": "The text mentions discoveries suggesting 20,000 to 40,000 years of human presence."
    },
    {
        "question": "How does this compare to previously assumed timelines?",
        "options": ["About the same", "Much earlier than previously assumed", "Slightly later", "Much later"],
        "correct": 1,
        "explanation": "New evidence suggests much earlier human presence than traditional theories assumed."
    },
    {
        "question": "What was the earlier estimate of human arrival that has been challenged?",
        "options": ["250,000 years ago", "The 20,000 to 40,000 year range", "5,000 years ago", "100,000 years ago"],
        "correct": 1,
        "explanation": "The text indicates that even estimates of 20,000-40,000 years may be conservative."
    },
    
    # Questions 26-50: British Colonial Period
    {
        "question": "Under whose flag did the events described in the colonial section occur?",
        "options": ["French flag", "British flag", "Spanish flag", "Dutch flag"],
        "correct": 1,
        "explanation": "The text specifically mentions events occurring under the British flag."
    },
    {
        "question": "Who was the British commander mentioned as reaching Detroit?",
        "options": ["Colonel Bouquet", "General Amherst", "Bradstreet", "Major Gladwin"],
        "correct": 2,
        "explanation": "Bradstreet is specifically mentioned as the British commander who reached Detroit."
    },
    {
        "question": "In what year did Bradstreet reach Detroit?",
        "options": ["1763", "1764", "1765", "1766"],
        "correct": 1,
        "explanation": "The text states Bradstreet reached Detroit in 1764."
    },
    {
        "question": "What date in August 1764 is specifically mentioned?",
        "options": ["August 15, 1764", "August 26, 1764", "August 30, 1764", "August 10, 1764"],
        "correct": 1,
        "explanation": "August 26, 1764 is the specific date mentioned for Bradstreet reaching Detroit."
    },
    {
        "question": "Where did western tribes assemble according to the text?",
        "options": ["At Fort Pitt", "At Detroit", "At various locations", "At Oswego"],
        "correct": 2,
        "explanation": "The text mentions western tribes assembling at various locations."
    },
    {
        "question": "What did the assembled tribes acknowledge regarding King George?",
        "options": ["His military power", "The sovereignty of King George", "His divine right", "His territorial claims"],
        "correct": 1,
        "explanation": "The tribes acknowledged the sovereignty of King George III."
    },
    {
        "question": "What did the British promise to do regarding war?",
        "options": ["Continue fighting", "Make war on enemies", "End all warfare", "Expand the conflict"],
        "correct": 1,
        "explanation": "The British promised to make war on their enemies as part of the agreement."
    },
    {
        "question": "What expedition from Fort Pitt is mentioned?",
        "options": ["A trading expedition", "Another expedition to pacify natives", "A surveying mission", "A diplomatic mission"],
        "correct": 1,
        "explanation": "Another expedition from Fort Pitt was mentioned to pacify the western natives."
    },
    {
        "question": "Who was tasked with pacifying the western natives?",
        "options": ["Sir William Johnson", "Colonel Bouquet", "General Amherst", "Major Gladwin"],
        "correct": 1,
        "explanation": "The task of pacifying western natives was given to British officials including Johnson."
    },
    {
        "question": "What was Colonel Bouquet's role in the peace process?",
        "options": ["He opposed peace", "He was necessary to finalize pacification", "He led military attacks", "He negotiated treaties"],
        "correct": 1,
        "explanation": "Colonel Bouquet was necessary to finally pacify the region."
    },
    {
        "question": "What was necessary to finalize the pacification efforts?",
        "options": ["More troops", "Further military action", "Diplomatic negotiations", "Economic incentives"],
        "correct": 1,
        "explanation": "Further military action was necessary to complete the pacification process."
    },
    {
        "question": "What kind of resistance was encountered initially?",
        "options": ["No resistance", "Fierce resistance", "Minimal resistance", "Organized resistance"],
        "correct": 1,
        "explanation": "The text indicates there was fierce resistance that needed to be overcome."
    },
    {
        "question": "Who presided over the peace arrangements?",
        "options": ["Colonel Bouquet", "Sir William Johnson", "General Amherst", "Colonel Bradstreet"],
        "correct": 1,
        "explanation": "Sir William Johnson presided over the peace arrangements."
    },
    {
        "question": "What was Sir William Johnson's role?",
        "options": ["Military commander", "Indian agent", "Colonial governor", "Trading post manager"],
        "correct": 1,
        "explanation": "Johnson served as the British Superintendent of Indian Affairs."
    },
    {
        "question": "Where did Johnson put the finishing touches on the peace arrangements?",
        "options": ["Detroit", "Fort Pitt", "Oswego, New York", "Quebec"],
        "correct": 2,
        "explanation": "The finishing touches were put on the peace arrangements at Oswego, New York."
    },
    {
        "question": "At what location in New York did this take place?",
        "options": ["Albany", "Oswego", "Buffalo", "Rochester"],
        "correct": 1,
        "explanation": "Oswego, New York was the specific location mentioned."
    },
    {
        "question": "In what month and year did this council occur?",
        "options": ["June 1766", "July 1766", "August 1766", "September 1766"],
        "correct": 1,
        "explanation": "The council occurred in July 1766."
    },
    {
        "question": "Who were the other leaders present at this meeting?",
        "options": ["Only British officials", "British and Indian leaders", "French representatives", "Spanish diplomats"],
        "correct": 1,
        "explanation": "Both British and Indian leaders were present at the meeting."
    },
    {
        "question": "What was Pontiac's role in these negotiations?",
        "options": ["He refused to participate", "He was a key Native American leader", "He sided with the French", "He opposed all agreements"],
        "correct": 1,
        "explanation": "Pontiac was a significant Native American leader involved in negotiations."
    },
    {
        "question": "How did Pontiac's position change over time?",
        "options": ["He became more hostile", "He eventually made peace", "He fled the region", "He joined the British army"],
        "correct": 1,
        "explanation": "Pontiac eventually came to terms and made peace with the British."
    },
    {
        "question": "What did the British and Indian leader appear to have agreed upon?",
        "options": ["Continued warfare", "A framework for peace", "British withdrawal", "French return"],
        "correct": 1,
        "explanation": "They established a framework for peaceful relations."
    },
    {
        "question": "What made it impractical for the Indians in the Midwest?",
        "options": ["British military presence", "Distance from British centers", "Lack of trade goods", "French influence"],
        "correct": 1,
        "explanation": "The distance and logistics made British control impractical in some areas."
    },
    {
        "question": "Why was the situation challenging for British control?",
        "options": ["Too many troops needed", "Vast distances involved", "Hostile French population", "Lack of resources"],
        "correct": 1,
        "explanation": "The vast territory made effective British control challenging."
    },
    {
        "question": "What reality made British control difficult among the tribes?",
        "options": ["Language barriers", "Cultural differences", "Geographic challenges", "Religious conflicts"],
        "correct": 2,
        "explanation": "The geographic extent and cultural differences made control difficult."
    },
    {
        "question": "What members of which tribe are specifically mentioned?",
        "options": ["Iroquois", "Peoria tribe", "Cherokee", "Seneca"],
        "correct": 1,
        "explanation": "Members of the Peoria tribe are specifically mentioned in the text."
    },
    
    # Questions 51-75: Post-Revolutionary Developments
    {
        "question": "What happened to Pontiac in the spring of 1769?",
        "options": ["He died of disease", "He was murdered", "He moved west", "He became a British ally"],
        "correct": 1,
        "explanation": "Pontiac was murdered in the spring of 1769, ending his influential career."
    },
    {
        "question": "Where was Pontiac murdered and buried?",
        "options": ["Detroit", "St. Louis", "Chicago", "Green Bay"],
        "correct": 1,
        "explanation": "Pontiac was murdered and buried in St. Louis."
    },
    {
        "question": "Who was murdered in Mississippi according to the text?",
        "options": ["A British official", "Pontiac", "A French trader", "An American settler"],
        "correct": 1,
        "explanation": "The text refers to Pontiac being murdered, and he was buried near the Mississippi region."
    },
    {
        "question": "Following whose arrival did Bradstreet return to England?",
        "options": ["Colonel Bouquet", "A new commander", "General Amherst", "Sir William Johnson"],
        "correct": 1,
        "explanation": "Bradstreet returned to England following the arrival of another commander."
    },
    {
        "question": "In what year did Bradstreet return to England?",
        "options": ["1790", "1791", "1792", "1793"],
        "correct": 1,
        "explanation": "Bradstreet returned to England in 1791."
    },
    {
        "question": "Who was sent by Bradstreet before his departure?",
        "options": ["A military aide", "Charles Langlade", "A diplomatic envoy", "A trading agent"],
        "correct": 1,
        "explanation": "Charles Langlade was sent by Bradstreet."
    },
    {
        "question": "What was Charles Langlade's role?",
        "options": ["Military commander", "Cultural intermediary", "Trading post manager", "Government official"],
        "correct": 1,
        "explanation": "Langlade served as an important intermediary between cultures."
    },
    {
        "question": "Who served as a country gentleman until his death?",
        "options": ["Pontiac", "Gladwin", "Bradstreet", "Johnson"],
        "correct": 1,
        "explanation": "Gladwin served as a country gentleman until his death."
    },
    {
        "question": "What was Gladwin's later occupation?",
        "options": ["Military officer", "Country gentleman", "Government official", "Trader"],
        "correct": 1,
        "explanation": "Gladwin became a country gentleman in his later years."
    },
    {
        "question": "Where did Captain William Howard go to reoccupy?",
        "options": ["Detroit", "The British garrison", "Fort Pitt", "Mackinac"],
        "correct": 1,
        "explanation": "Howard went to reoccupy the British garrison."
    },
    {
        "question": "What was Howard's mission regarding the British garrison?",
        "options": ["To abandon it", "To save it", "To expand it", "To relocate it"],
        "correct": 1,
        "explanation": "Howard's mission was to save the British garrison."
    },
    {
        "question": "Where were the headquarters moved to?",
        "options": ["Detroit", "Green Bay", "Fort Pitt", "Quebec"],
        "correct": 1,
        "explanation": "The headquarters were moved to Green Bay."
    },
    {
        "question": "What had Howard done before the uprising?",
        "options": ["Served in the military", "Made a plan", "Worked as a trader", "Lived as a farmer"],
        "correct": 1,
        "explanation": "Howard had made a plan before the uprising occurred."
    },
    {
        "question": "What plan had he made before the revolt?",
        "options": ["An escape route", "A defense strategy", "Plans to help his situation", "A trading agreement"],
        "correct": 2,
        "explanation": "Howard had made plans that helped him during the revolt."
    },
    {
        "question": "Where did he have numerous relatives?",
        "options": ["In Detroit", "Among various groups", "In England", "In Quebec"],
        "correct": 1,
        "explanation": "Howard had numerous relatives in various locations."
    },
    {
        "question": "During which war did he fight with the British?",
        "options": ["French and Indian War", "Pontiac's Rebellion", "American Revolution", "War of 1812"],
        "correct": 2,
        "explanation": "Howard fought with the British during the American Revolution."
    },
    {
        "question": "What revolution is mentioned in relation to American control?",
        "options": ["French Revolution", "American Revolution", "Industrial Revolution", "Glorious Revolution"],
        "correct": 1,
        "explanation": "The American Revolution is mentioned in relation to the transition to American control."
    },
    {
        "question": "What did he become reconciled to?",
        "options": ["British rule", "American control", "French influence", "Spanish authority"],
        "correct": 1,
        "explanation": "Howard became reconciled to American control."
    },
    {
        "question": "What was he known as in the nineteenth century?",
        "options": ["The father of Detroit", "The father of the lake region", "The great mediator", "The frontier leader"],
        "correct": 1,
        "explanation": "Howard became known as 'the father of the lake region.'"
    },
    {
        "question": "For what is he named in later references?",
        "options": ["His military service", "His role in the region", "His trading activities", "His diplomatic efforts"],
        "correct": 1,
        "explanation": "He is remembered for his significant role in the development of the lake region."
    },
    {
        "question": "What county in Wisconsin is mentioned?",
        "options": ["Milwaukee County", "A county named for him", "Dane County", "Brown County"],
        "correct": 1,
        "explanation": "A county in Wisconsin was named after him."
    },
    {
        "question": "After what uprising did the British establish permanent garrisons?",
        "options": ["Pontiac's Rebellion", "The Indian uprising", "The American Revolution", "The French revolt"],
        "correct": 1,
        "explanation": "The British established permanent garrisons after the Indian uprising."
    },
    {
        "question": "Around what fort did they reestablish presence?",
        "options": ["Fort Pitt", "Fort St. Joseph", "Fort Detroit", "Fort Mackinac"],
        "correct": 1,
        "explanation": "The British reestablished presence around Fort St. Joseph."
    },
    {
        "question": "What was the responsibility given to the Potawatomi?",
        "options": ["Military defense", "Trade regulation", "Various responsibilities", "Diplomatic relations"],
        "correct": 2,
        "explanation": "The Potawatomi were given various responsibilities in the region."
    },
    {
        "question": "Under whose supervision was the St. Joseph Valley following the suppression of the Indian outbreak?",
        "options": ["British military", "American officials", "The commandant", "French administrators"],
        "correct": 2,
        "explanation": "The St. Joseph Valley was under the supervision of the commandant following the suppression of the outbreak."
    },
    
    # Questions 76-100: British Rule and Conflicts
    {
        "question": "What year marked the beginning of British control over Michigan?",
        "options": ["1759", "1760", "1763", "1764"],
        "correct": 1,
        "explanation": "1760 marked the beginning of British control, though it was formalized in 1763."
    },
    {
        "question": "What major conflict preceded British control of the region?",
        "options": ["King Philip's War", "French and Indian War", "Pontiac's Rebellion", "American Revolution"],
        "correct": 1,
        "explanation": "The French and Indian War (Seven Years' War) preceded British control."
    },
    {
        "question": "What treaty established British authority in the area?",
        "options": ["Treaty of Utrecht", "Treaty of Paris (1763)", "Treaty of Ghent", "Jay's Treaty"],
        "correct": 1,
        "explanation": "The Treaty of Paris (1763) established British authority over former French territories."
    },
    {
        "question": "Who were the key British military leaders mentioned in this period?",
        "options": ["Amherst and Wolfe", "Bradstreet and Bouquet", "Cornwallis and Clinton", "Burgoyne and Howe"],
        "correct": 1,
        "explanation": "Bradstreet and Bouquet were key British military leaders in the Great Lakes region."
    },
    {
        "question": "What role did traders play during the British period?",
        "options": ["They were banned", "They were essential to the economy", "They caused conflicts", "They were government officials"],
        "correct": 1,
        "explanation": "Traders were essential to the colonial economy and British-Native American relations."
    },
    {
        "question": "Which Native American leaders are specifically mentioned in relation to British rule?",
        "options": ["Tecumseh and Blue Jacket", "Pontiac and tribal chiefs", "Little Turtle and Black Hawk", "Sitting Bull and Crazy Horse"],
        "correct": 1,
        "explanation": "Pontiac and various tribal chiefs are mentioned in relation to British rule."
    },
    {
        "question": "What was the significance of Detroit during British administration?",
        "options": ["It was abandoned", "It became the regional center", "It lost importance", "It became a trading post"],
        "correct": 1,
        "explanation": "Detroit served as the major British administrative and military center in the region."
    },
    {
        "question": "How did the British approach differ from previous European control?",
        "options": ["More military focused", "More diplomatic", "Less organized", "More commercial"],
        "correct": 0,
        "explanation": "British control was more military-focused compared to the French approach of alliance and trade."
    },
    {
        "question": "What economic activities were prominent during British rule?",
        "options": ["Agriculture only", "Fur trading", "Manufacturing", "Mining"],
        "correct": 1,
        "explanation": "Fur trading remained the dominant economic activity during British rule."
    },
    {
        "question": "Which forts were maintained or established by the British?",
        "options": ["Only Detroit", "Detroit and other key posts", "New forts only", "No military presence"],
        "correct": 1,
        "explanation": "The British maintained Detroit and other strategic forts throughout the region."
    },
    {
        "question": "What challenges did British authorities face in governing the region?",
        "options": ["No major challenges", "Distance and Native resistance", "French interference", "Spanish attacks"],
        "correct": 1,
        "explanation": "Distance from British centers and Native American resistance created governance challenges."
    },
    {
        "question": "How did the relationship between British officials and Native Americans develop?",
        "options": ["Always hostile", "Gradually improved through diplomacy", "Remained unchanged", "Quickly deteriorated"],
        "correct": 1,
        "explanation": "Relations gradually improved through diplomatic efforts like those of Sir William Johnson."
    },
    {
        "question": "What trading practices were established during this period?",
        "options": ["Free trade", "Regulated British trade", "No trade allowed", "Spanish-controlled trade"],
        "correct": 1,
        "explanation": "The British established regulated trading practices to control Native American relations."
    },
    {
        "question": "Which British policies affected the local population?",
        "options": ["Trade regulations", "Land policies", "Military policies", "All of the above"],
        "correct": 3,
        "explanation": "British trade, land, and military policies all significantly affected local populations."
    },
    {
        "question": "What military strategies did the British employ in the region?",
        "options": ["Naval control only", "Fort-based defense system", "Mobile armies", "Militia only"],
        "correct": 1,
        "explanation": "The British relied on a system of forts for military control of the region."
    },
    {
        "question": "How did British control impact existing trade networks?",
        "options": ["Destroyed them", "Adapted and controlled them", "Ignored them", "Replaced them completely"],
        "correct": 1,
        "explanation": "The British adapted existing French-Native American trade networks to their control."
    },
    {
        "question": "What administrative changes were implemented under British rule?",
        "options": ["None", "Military government", "Civilian colonies", "Native American rule"],
        "correct": 1,
        "explanation": "The British initially implemented military government in the newly acquired territories."
    },
    {
        "question": "Which settlements grew in importance during this period?",
        "options": ["Only new British towns", "Detroit and key trading posts", "Native American villages", "French settlements only"],
        "correct": 1,
        "explanation": "Detroit and strategic trading posts grew in importance under British rule."
    },
    {
        "question": "What role did the Great Lakes play in British strategy?",
        "options": ["No strategic importance", "Key transportation and communication routes", "Barriers to expansion", "Sources of conflict only"],
        "correct": 1,
        "explanation": "The Great Lakes were crucial transportation and communication routes for British administration."
    },
    {
        "question": "How did British rule affect relationships between different Native American groups?",
        "options": ["Had no effect", "Created new alliances and conflicts", "United all tribes", "Eliminated tribal differences"],
        "correct": 1,
        "explanation": "British policies and presence created new dynamics in inter-tribal relationships."
    },
    {
        "question": "What were the main sources of conflict during British administration?",
        "options": ["Religious differences", "Land disputes and cultural clashes", "Economic competition only", "Language barriers"],
        "correct": 1,
        "explanation": "Land disputes, cultural differences, and competing interests were major sources of conflict."
    },
    {
        "question": "Which British officials played key roles in regional governance?",
        "options": ["Only military commanders", "Governors and Indian agents", "Trading company officials", "Religious leaders"],
        "correct": 1,
        "
