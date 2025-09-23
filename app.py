"""
HIS220: Michigan's First Residents & Colonial Era - Century Challenge
100-Question Mastery Quiz - CognitiveCloud.ai
"""

import streamlit as st
import time
import json
from datetime import datetime

st.set_page_config(
    page_title="HIS220: Michigan Century Challenge",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

QUESTIONS = [
    {"question": "What was the land that became Michigan inhabited by before Europeans arrived?", "options": ["Empty wilderness", "Various Native American peoples", "French settlers", "Spanish explorers"], "correct": 1, "explanation": "Michigan was inhabited by various indigenous peoples for thousands of years before European contact."},
    {"question": "Why did Europeans initially call Native Americans 'Indians'?", "options": ["It was their actual name", "Columbus thought he reached the East Indies", "It was a Spanish word", "They called themselves that"], "correct": 1, "explanation": "Columbus mistakenly believed he had reached the East Indies."},
    {"question": "What was Columbus's mistaken belief?", "options": ["He thought they were from India", "He believed he reached the East Indies", "He confused them with Indonesians", "He thought they were Spanish"], "correct": 1, "explanation": "Columbus believed he had reached the Indies."},
    {"question": "What name has persisted for over a century?", "options": ["Americans", "Indians", "Natives", "Aboriginals"], "correct": 1, "explanation": "The term 'Indians' persisted despite the geographical error."},
    {"question": "How long have misnomers been used in Michigan?", "options": ["Decades", "Over a century", "A few years", "Since statehood"], "correct": 1, "explanation": "These naming errors persisted for over a century."},
    {"question": "What did Europeans believe about the land?", "options": ["Densely populated", "Mostly uninhabited", "Belonged to Spain", "Claimed by France"], "correct": 1, "explanation": "Europeans viewed the land as empty, ignoring indigenous presence."},
    {"question": "Which French explorers had contact with Michigan's indigenous peoples?", "options": ["Cartier and Champlain", "The French found in Michigan", "Marquette and Joliet", "La Salle and Cadillac"], "correct": 1, "explanation": "French contact with indigenous peoples in Michigan."},
    {"question": "What assumption about migration has been challenged?", "options": ["That it happened recently", "Traditional timing estimates", "That it came from Europe", "That it was by boat"], "correct": 1, "explanation": "Recent discoveries challenged traditional assumptions."},
    {"question": "Most common assumption about how people came to the Western Hemisphere?", "options": ["By boat", "Via a land bridge from Asia", "From Europe", "They evolved there"], "correct": 1, "explanation": "Traditional theory suggests land bridge from Asia."},
    {"question": "How did early peoples supposedly cross to the Americas?", "options": ["By boat across Pacific", "Via the Bering land bridge", "Across the Atlantic", "Through Central America"], "correct": 1, "explanation": "The Bering land bridge theory was traditional explanation."},
    {"question": "What geographical feature connected Asia to the Americas?", "options": ["An ice sheet", "The Bering land bridge", "A chain of islands", "A frozen ocean"], "correct": 1, "explanation": "The Bering land bridge (Beringia) connected continents."},
    {"question": "When was this land bridge accessible?", "options": ["During warm periods", "During ice ages", "Every winter", "Only in summer"], "correct": 1, "explanation": "Lower sea levels during ice ages exposed the bridge."},
    {"question": "What prevented travel between hemispheres?", "options": ["Mountains", "Desert", "A narrow waterway", "Dense forests"], "correct": 2, "explanation": "A narrow waterway prevented easy travel."},
    {"question": "Why was the waterway significant?", "options": ["Too deep", "It blocked migration", "Always frozen", "Strong currents"], "correct": 1, "explanation": "The waterway served as a barrier to movement."},
    {"question": "What age-determining methods are mentioned?", "options": ["Tree ring dating", "Radiocarbon dating", "Pottery analysis", "Geological layers"], "correct": 1, "explanation": "Radiocarbon dating is mentioned for determining age."},
    {"question": "What dating technique involving radiocarbon is referenced?", "options": ["Carbon-14 testing", "Radiocarbon dating", "Carbon analysis", "Isotope dating"], "correct": 1, "explanation": "Radiocarbon dating is the specific technique."},
    {"question": "How have comparative studies of vessels contributed?", "options": ["Show trade routes", "Help with dating", "Reveal migration patterns", "Indicate cultural connections"], "correct": 1, "explanation": "Comparative studies help understand chronology."},
    {"question": "What discoveries changed historical timelines?", "options": ["Pottery finds", "Archaeological discoveries", "Written records", "Oral histories"], "correct": 1, "explanation": "Archaeological discoveries pushed back estimates."},
    {"question": "In what decade did discoveries push back estimates?", "options": ["1920s", "1940s", "1960s", "1980s"], "correct": 1, "explanation": "Discoveries in the 1940s changed understanding."},
    {"question": "What was the previous assumption about arrival?", "options": ["5,000 years ago", "Much more recently", "10,000 years ago", "50,000 years ago"], "correct": 1, "explanation": "Earlier estimates were much more recent."},
    {"question": "Where have discoveries suggested earlier presence?", "options": ["Only in Michigan", "California and Mexico", "Only in Canada", "Throughout Midwest"], "correct": 1, "explanation": "California and Mexico specifically mentioned."},
    {"question": "What areas have evidence of early habitation?", "options": ["Great Lakes region", "California and Mexico", "Eastern seaboard", "Pacific Northwest"], "correct": 1, "explanation": "California and Mexico are cited."},
    {"question": "What time range do discoveries suggest?", "options": ["5,000-10,000 years", "20,000-40,000 years", "50,000-100,000 years", "1,000-5,000 years"], "correct": 1, "explanation": "20,000 to 40,000 years suggested."},
    {"question": "How does this compare to previous timelines?", "options": ["About the same", "Much earlier", "Slightly later", "Much later"], "correct": 1, "explanation": "Much earlier than traditional theories assumed."},
    {"question": "What earlier estimate has been challenged?", "options": ["250,000 years ago", "The 20,000-40,000 year range", "5,000 years ago", "100,000 years ago"], "correct": 1, "explanation": "Even 20,000-40,000 year estimates may be conservative."},
    {"question": "Under whose flag did colonial events occur?", "options": ["French flag", "British flag", "Spanish flag", "Dutch flag"], "correct": 1, "explanation": "Events occurred under the British flag."},
    {"question": "Who was the British commander reaching Detroit?", "options": ["Colonel Bouquet", "General Amherst", "Bradstreet", "Major Gladwin"], "correct": 2, "explanation": "Bradstreet reached Detroit."},
    {"question": "In what year did Bradstreet reach Detroit?", "options": ["1763", "1764", "1765", "1766"], "correct": 1, "explanation": "Bradstreet reached Detroit in 1764."},
    {"question": "What date in August 1764 is mentioned?", "options": ["August 15", "August 26", "August 30", "August 10"], "correct": 1, "explanation": "August 26, 1764 is the specific date."},
    {"question": "Where did western tribes assemble?", "options": ["At Fort Pitt", "At Detroit", "At various locations", "At Oswego"], "correct": 2, "explanation": "Western tribes assembled at various locations."},
    {"question": "What did tribes acknowledge about King George?", "options": ["His military power", "The sovereignty of King George", "His divine right", "His territorial claims"], "correct": 1, "explanation": "Tribes acknowledged King George III's sovereignty."},
    {"question": "What did the British promise regarding war?", "options": ["Continue fighting", "Make war on enemies", "End all warfare", "Expand the conflict"], "correct": 1, "explanation": "British promised to make war on enemies."},
    {"question": "What expedition from Fort Pitt is mentioned?", "options": ["A trading expedition", "Another expedition to pacify natives", "A surveying mission", "A diplomatic mission"], "correct": 1, "explanation": "Another expedition to pacify western natives."},
    {"question": "Who was tasked with pacifying western natives?", "options": ["Sir William Johnson", "Colonel Bouquet", "General Amherst", "Major Gladwin"], "correct": 1, "explanation": "British officials including Johnson."},
    {"question": "What was Colonel Bouquet's role?", "options": ["He opposed peace", "He was necessary to finalize pacification", "He led military attacks", "He negotiated treaties"], "correct": 1, "explanation": "Bouquet was necessary to pacify the region."},
    {"question": "What was necessary to finalize pacification?", "options": ["More troops", "Further military action", "Diplomatic negotiations", "Economic incentives"], "correct": 1, "explanation": "Further military action was necessary."},
    {"question": "What resistance was encountered?", "options": ["No resistance", "Fierce resistance", "Minimal resistance", "Organized resistance"], "correct": 1, "explanation": "Fierce resistance needed to be overcome."},
    {"question": "Who presided over peace arrangements?", "options": ["Colonel Bouquet", "Sir William Johnson", "General Amherst", "Colonel Bradstreet"], "correct": 1, "explanation": "Sir William Johnson presided."},
    {"question": "What was Sir William Johnson's role?", "options": ["Military commander", "Indian agent", "Colonial governor", "Trading post manager"], "correct": 1, "explanation": "Johnson was Superintendent of Indian Affairs."},
    {"question": "Where did Johnson finalize peace arrangements?", "options": ["Detroit", "Fort Pitt", "Oswego, New York", "Quebec"], "correct": 2, "explanation": "Oswego, New York was the location."},
    {"question": "At what location in New York?", "options": ["Albany", "Oswego", "Buffalo", "Rochester"], "correct": 1, "explanation": "Oswego, New York."},
    {"question": "When did this council occur?", "options": ["June 1766", "July 1766", "August 1766", "September 1766"], "correct": 1, "explanation": "The council occurred in July 1766."},
    {"question": "Who were the other leaders present?", "options": ["Only British officials", "British and Indian leaders", "French representatives", "Spanish diplomats"], "correct": 1, "explanation": "Both British and Indian leaders present."},
    {"question": "What was Pontiac's role?", "options": ["He refused to participate", "He was a key Native American leader", "He sided with the French", "He opposed all agreements"], "correct": 1, "explanation": "Pontiac was a significant leader."},
    {"question": "How did Pontiac's position change?", "options": ["He became more hostile", "He eventually made peace", "He fled the region", "He joined the British army"], "correct": 1, "explanation": "Pontiac eventually made peace with the British."},
    {"question": "What did British and Indian leaders agree upon?", "options": ["Continued warfare", "A framework for peace", "British withdrawal", "French return"], "correct": 1, "explanation": "They established a framework for peace."},
    {"question": "What made it impractical for Indians in Midwest?", "options": ["British military presence", "Distance from British centers", "Lack of trade goods", "French influence"], "correct": 1, "explanation": "Distance made British control impractical."},
    {"question": "Why was the situation challenging for British?", "options": ["Too many troops needed", "Vast distances involved", "Hostile French population", "Lack of resources"], "correct": 1, "explanation": "Vast territory made control challenging."},
    {"question": "What made British control difficult?", "options": ["Language barriers", "Cultural differences", "Geographic challenges", "Religious conflicts"], "correct": 2, "explanation": "Geographic extent and cultural differences."},
    {"question": "What tribe members are mentioned?", "options": ["Iroquois", "Peoria tribe", "Cherokee", "Seneca"], "correct": 1, "explanation": "Members of the Peoria tribe mentioned."},
    {"question": "What happened to Pontiac in spring 1769?", "options": ["He died of disease", "He was murdered", "He moved west", "He became a British ally"], "correct": 1, "explanation": "Pontiac was murdered in spring 1769."},
    {"question": "Where was Pontiac murdered and buried?", "options": ["Detroit", "St. Louis", "Chicago", "Green Bay"], "correct": 1, "explanation": "Pontiac was murdered and buried in St. Louis."},
    {"question": "Who was murdered in Mississippi?", "options": ["A British official", "Pontiac", "A French trader", "An American settler"], "correct": 1, "explanation": "Pontiac was murdered near Mississippi region."},
    {"question": "Following whose arrival did Bradstreet return?", "options": ["Colonel Bouquet", "A new commander", "General Amherst", "Sir William Johnson"], "correct": 1, "explanation": "Bradstreet returned after new commander arrived."},
    {"question": "When did Bradstreet return to England?", "options": ["1790", "1791", "1792", "1793"], "correct": 1, "explanation": "Bradstreet returned to England in 1791."},
    {"question": "Who was sent by Bradstreet before departure?", "options": ["A military aide", "Charles Langlade", "A diplomatic envoy", "A trading agent"], "correct": 1, "explanation": "Charles Langlade was sent by Bradstreet."},
    {"question": "What was Charles Langlade's role?", "options": ["Military commander", "Cultural intermediary", "Trading post manager", "Government official"], "correct": 1, "explanation": "Langlade was an important intermediary."},
    {"question": "Who served as country gentleman until death?", "options": ["Pontiac", "Gladwin", "Bradstreet", "Johnson"], "correct": 1, "explanation": "Gladwin served as a country gentleman."},
    {"question": "What was Gladwin's later occupation?", "options": ["Military officer", "Country gentleman", "Government official", "Trader"], "correct": 1, "explanation": "Gladwin became a country gentleman."},
    {"question": "Where did Captain Howard go to reoccupy?", "options": ["Detroit", "The British garrison", "Fort Pitt", "Mackinac"], "correct": 1, "explanation": "Howard went to reoccupy the British garrison."},
    {"question": "What was Howard's mission?", "options": ["To abandon it", "To save it", "To expand it", "To relocate it"], "correct": 1, "explanation": "Howard's mission was to save the garrison."},
    {"question": "Where were headquarters moved?", "options": ["Detroit", "Green Bay", "Fort Pitt", "Quebec"], "correct": 1, "explanation": "Headquarters moved to Green Bay."},
    {"question": "What had Howard done before uprising?", "options": ["Served in military", "Made a plan", "Worked as trader", "Lived as farmer"], "correct": 1, "explanation": "Howard had made a plan before uprising."},
    {"question": "What plan had he made?", "options": ["An escape route", "A defense strategy", "Plans to help his situation", "A trading agreement"], "correct": 2, "explanation": "Howard made plans that helped during revolt."},
    {"question": "Where did he have relatives?", "options": ["In Detroit", "Among various groups", "In England", "In Quebec"], "correct": 1, "explanation": "Howard had relatives in various locations."},
    {"question": "During which war did he fight with British?", "options": ["French and Indian War", "Pontiac's Rebellion", "American Revolution", "War of 1812"], "correct": 2, "explanation": "Howard fought with British during Revolution."},
    {"question": "What revolution is mentioned?", "options": ["French Revolution", "American Revolution", "Industrial Revolution", "Glorious Revolution"], "correct": 1, "explanation": "American Revolution mentioned."},
    {"question": "What did he become reconciled to?", "options": ["British rule", "American control", "French influence", "Spanish authority"], "correct": 1, "explanation": "Howard reconciled to American control."},
    {"question": "What was he known as in 19th century?", "options": ["Father of Detroit", "Father of the lake region", "The great mediator", "The frontier leader"], "correct": 1, "explanation": "Known as 'father of the lake region.'"},
    {"question": "For what is he named in references?", "options": ["His military service", "His role in the region", "His trading activities", "His diplomatic efforts"], "correct": 1, "explanation": "Remembered for his role in development."},
    {"question": "What county in Wisconsin is mentioned?", "options": ["Milwaukee County", "A county named for him", "Dane County", "Brown County"], "correct": 1, "explanation": "A Wisconsin county was named after him."},
    {"question": "After what uprising did British establish garrisons?", "options": ["Pontiac's Rebellion", "The Indian uprising", "American Revolution", "French revolt"], "correct": 1, "explanation": "After the Indian uprising."},
    {"question": "Around what fort did they reestablish?", "options": ["Fort Pitt", "Fort St. Joseph", "Fort Detroit", "Fort Mackinac"], "correct": 1, "explanation": "Around Fort St. Joseph."},
    {"question": "What responsibility given to Potawatomi?", "options": ["Military defense", "Trade regulation", "Various responsibilities", "Diplomatic relations"], "correct": 2, "explanation": "Potawatomi given various responsibilities."},
    {"question": "Under whose supervision was St. Joseph Valley?", "options": ["British military", "American officials", "The commandant", "French administrators"], "correct": 2, "explanation": "Under the commandant's supervision."},
    {"question": "What year marked British control over Michigan?", "options": ["1759", "1760", "1763", "1764"], "correct": 1, "explanation": "1760 marked British control beginning."},
    {"question": "What conflict preceded British control?", "options": ["King Philip's War", "French and Indian War", "Pontiac's Rebellion", "American Revolution"], "correct": 1, "explanation": "French and Indian War preceded control."},
    {"question": "What treaty established British authority?", "options": ["Treaty of Utrecht", "Treaty of Paris (1763)", "Treaty of Ghent", "Jay's Treaty"], "correct": 1, "explanation": "Treaty of Paris (1763) established authority."},
    {"question": "Who were key British military leaders?", "options": ["Amherst and Wolfe", "Bradstreet and Bouquet", "Cornwallis and Clinton", "Burgoyne and Howe"], "correct": 1, "explanation": "Bradstreet and Bouquet were key leaders."},
    {"question": "What role did traders play?", "options": ["They were banned", "They were essential to economy", "They caused conflicts", "They were government officials"], "correct": 1, "explanation": "Traders were essential to economy."},
    {"question": "Which Native leaders are mentioned with British rule?", "options": ["Tecumseh and Blue Jacket", "Pontiac and tribal chiefs", "Little Turtle and Black Hawk", "Sitting Bull and Crazy Horse"], "correct": 1, "explanation": "Pontiac and tribal chiefs mentioned."},
    {"question": "What was Detroit's significance?", "options": ["It was abandoned", "It became the regional center", "It lost importance", "It became a trading post"], "correct": 1, "explanation": "Detroit became the regional center."},
    {"question": "How did British approach differ?", "options": ["More military focused", "More diplomatic", "Less organized", "More commercial"], "correct": 0, "explanation": "British control was more military-focused."},
    {"question": "What economic activities were prominent?", "options": ["Agriculture only", "Fur trading", "Manufacturing", "Mining"], "correct": 1, "explanation": "Fur trading remained dominant."},
    {"question": "Which forts were maintained by British?", "options": ["Only Detroit", "Detroit and other key posts", "New forts only", "No military presence"], "correct": 1, "explanation": "Detroit and other strategic forts maintained."},
    {"question": "What challenges did British face?", "options": ["No major challenges", "Distance and Native resistance", "French interference", "Spanish attacks"], "correct": 1, "explanation": "Distance and Native resistance created challenges."},
    {"question": "How did British-Native relations develop?", "options": ["Always hostile", "Gradually improved through diplomacy", "Remained unchanged", "Quickly deteriorated"], "correct": 1, "explanation": "Relations gradually improved through diplomacy."},
    {"question": "What trading practices were established?", "options": ["Free trade", "Regulated British trade", "No trade allowed", "Spanish-controlled trade"], "correct": 1, "explanation": "British established regulated trading."},
    {"question": "Which British policies affected locals?", "options": ["Trade regulations", "Land policies", "Military policies", "All of the above"], "correct": 3, "explanation": "All policies affected local populations."},
    {"question": "What military strategies did British employ?", "options": ["Naval control only", "Fort-based defense system", "Mobile armies", "Militia only"], "correct": 1, "explanation": "British relied on system of forts."},
    {"question": "How did British control impact trade networks?", "options": ["Destroyed them", "Adapted and controlled them", "Ignored them", "Replaced them completely"], "correct": 1, "explanation": "British adapted existing networks."},
    {"question": "What administrative changes were implemented?", "options": ["None", "Military government", "Civilian colonies", "Native American rule"], "correct": 1, "explanation": "British implemented military government."},
    {"question": "Which settlements grew in importance?", "options": ["Only new British towns", "Detroit and key trading posts", "Native American villages", "French settlements only"], "correct": 1, "explanation": "Detroit and trading posts grew."},
    {"question": "What role did Great Lakes play?", "options": ["No strategic importance", "Key transportation routes", "Barriers to expansion", "Sources of conflict only"], "correct": 1, "explanation": "Great Lakes were crucial transportation routes."},
    {"question": "How did British rule affect Native relations?", "options": ["Had no effect", "Created new alliances and conflicts", "United all tribes", "Eliminated tribal differences"], "correct": 1, "explanation": "Created new dynamics in relationships."},
    {"question": "What were main sources of conflict?", "options": ["Religious differences", "Land disputes and cultural clashes", "Economic competition only", "Language barriers"], "correct": 1, "explanation": "Land disputes and cultural differences."},
    {"question": "Which officials played key governance roles?", "options": ["Only military commanders", "Governors and Indian agents", "Trading company officials", "Religious leaders"], "correct": 1, "explanation": "Governors and Indian agents were crucial."},
    {"question": "How did transition from French to British occur?", "options": ["Peacefully through treaty", "Through military conquest and negotiation", "French abandoned region", "Natives chose British"], "correct": 1, "explanation": "Through conquest and negotiations."},
    {"question": "What long-term impacts did British control have?", "options": ["No lasting impact", "Established administrative foundations", "Only military influence", "Reversed French policies"], "correct": 1, "explanation": "Established administrative and legal foundations."}
]

def award_xp(amount, reason=""):
    st.session_state.total_xp += amount
    milestones = [(500, "Rising Scholar"), (1000, "History Enthusiast"), (1500, "Michigan Expert"), (2000, "Colonial Master"), (2500, "Historical Analyst"), (3000, "ULTIMATE CHAMPION")]
    for threshold, title in milestones:
        if st.session_state.total_xp >= threshold and title not in st.session_state.achievements:
            st.session_state.achievements.append(title)
            if threshold >= 2000:
                st.balloons()
            st.success(f"🏆 {title}! ({threshold}+ XP)")
    if amount > 0:
        st.success(f"⭐ +{amount} XP! {reason}")

def display_quiz():
    st.markdown("# 🏛️ Ultimate Michigan History Challenge")
    st.markdown("## 100 Questions - Maximum XP")
    
    if not st.session_state.quiz_started:
        st.markdown("""
        ### Challenge Overview:
        - **100 Sequential Questions**
        - **Up to 3,000+ XP possible**
        - **Epic Achievements**
        
        ### XP System:
        - **Perfect (100%)**: 2,000 XP
        - **Excellent (90-99%)**: 1,650 XP
        - **Very Good (80-89%)**: 1,400 XP
        """)
        if st.button("🚀 BEGIN CHALLENGE", key="start"):
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()
            st.rerun()
        return
    
    if st.session_state.quiz_completed:
        display_results()
        return
    
    st.progress(len(st.session_state.answers) / 100)
    st.caption(f"Progress: {len(st.session_state.answers)}/100")
    
    if hasattr(st.session_state, 'start_time'):
        elapsed = time.time() - st.session_state.start_time
        mins, secs = divmod(int(elapsed), 60)
        st.markdown(f"**Time: {mins:02d}:{secs:02d}**")
    
    with st.form("quiz"):
        st.markdown("### Answer all 100 questions:")
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"**Q{i+1}:** {q['question']}")
            answer = st.radio("", q["options"], key=f"q_{i}", index=st.session_state.answers.get(i))
            if answer:
                st.session_state.answers[i] = q["options"].index(answer)
            st.markdown("---")
        
        if st.form_submit_button("🎯 SUBMIT QUIZ") and len(st.session_state.answers) == 100:
            process_results()

def process_results():
    correct = sum(1 for i, q in enumerate(QUESTIONS) if i in st.session_state.answers and st.session_state.answers[i] == q["correct"])
    st.session_state.final_score = (correct / 100) * 100
    st.session_state.correct_count = correct
    st.session_state.completion_time = (time.time() - st.session_state.start_time) / 60 if hasattr(st.session_state, 'start_time') else 0
    st.session_state.quiz_completed = True
    
    base_xp = correct * 15
    bonus = 500 if st.session_state.final_score == 100 else 300 if st.session_state.final_score >= 90 else 200 if st.session_state.final_score >= 80 else 100 if st.session_state.final_score >= 70 else 50
    
    if st.session_state.final_score == 100:
        st.balloons()
        st.session_state.achievements.append("Perfect Century")
    
    if st.session_state.completion_time < 30 and st.session_state.final_score >= 80:
        st.session_state.achievements.append("Speed Demon")
        bonus += 150
    
    st.session_state.achievements.append("Century Club")
    total_xp = base_xp + bonus + 100
    award_xp(total_xp, f"Challenge: {st.session_state.final_score:.1f}%")
    st.rerun()

def display_results():
    st.markdown("# 🎉 CHALLENGE COMPLETE!")
    score = st.session_state.final_score
    correct = st.session_state.correct_count
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{score:.1f}%", f"{correct}/100")
    col2.metric("Time", f"{st.session_state.completion_time:.1f} min")
    col3.metric("XP", st.session_state.total_xp)
    col4.metric("Achievements", len(st.session_state.achievements))
    
    if score == 100:
        st.success("🏆 PERFECT! MICHIGAN HISTORY MASTER!")
        st.balloons()
    elif score >= 90:
        st.success("⭐ EXCELLENT! Exceptional knowledge!")
    elif score >= 80:
        st.info("📚 GOOD WORK! Strong understanding!")
    else:
        st.info("📖 Keep studying!")
    
    with st.expander("🔍 Question Analysis"):
        for i, q in enumerate(QUESTIONS):
            user_ans = st.session_state.answers.get(i)
            if user_ans == q["correct"]:
                st.success(f"✅ Q{i+1}: CORRECT")
            else:
                st.error(f"❌ Q{i+1}: INCORRECT - Correct: {q['options'][q['correct']]}")
            with st.expander(f"Context Q{i+1}"):
                st.markdown(q['explanation'])
    
    if st.session_state.achievements:
        st.markdown("### 🏆 Achievements")
        for ach in st.session_state.achievements:
            st.success(f"🏆 {ach}")
    
    if st.button("🔄 RETAKE"):
        st.session_state.quiz_started = False
        st.session_state.answers = {}
        st.session_state.quiz_completed = False
        st.rerun()

st.markdown("""
<style>
.stButton > button {
    width: 100%;
    border-radius: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: bold;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%); 
            color: white; padding: 30px; border-radius: 20px; text-align: center; margin: 20px 0;'>
    <h1>🏛️ HIS220: MICHIGAN CENTURY CHALLENGE</h1>
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

display_quiz()

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: #1f1f1f; 
            color: white; border-radius: 15px;'>
    <h3>🏛️ MICHIGAN HISTORY ULTIMATE CHALLENGE</h3>
    <p><strong>100 Questions • Complete Mastery • Maximum XP</strong></p>
    <p>CognitiveCloud.ai Learning Platform - HIS220</p>
</div>
""", unsafe_allow_html=True)
