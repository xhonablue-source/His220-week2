"""
Quiz 1: HIS 220 History of Michigan
Based on "Michigan A History of the Wolverine State" 
by Willis F. Dunbar and Georges May (Third Revised Edition)
"""

import streamlit as st
import time
import json
from datetime import datetime

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Quiz 1: HIS220 History of Michigan",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
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
if 'completion_time' not in st.session_state:
    st.session_state.completion_time = 0

# --- 100 Sensible Questions Based on the PDF Text ---
# (The 100-question list remains the same)
QUESTIONS = [
    {"question": "English observers *incorrectly* depicted French habitants as primarily interested in what activity?", "options": ["Working the fields", "Trading furs", "Playing", "Fishing"], "correct": 2, "explanation": "English and American observers inaccurately characterized the habitants as 'more interested in playing than in working.'"},
    {"question": "What kind of people were the French habitants described as in *actuality*?", "options": ["Irresponsible dreamers", "Hard-working, conservative folk", "Wealthy merchants", "Vagrant adventurers"], "correct": 1, "explanation": "The text states the habitants were, as a group, hard-working, conservative folk of good, solid peasant stock."},
    {"question": "The failure of Detroit to develop according to plan was primarily attributed to the failure of the:", "options": ["French habitants", "Indian tribes", "French authorities", "British military"], "correct": 2, "explanation": "It was 'less the fault of its inhabitants than it was the failure or inability of the French authorities' to shift focus from the fur trade."},
    {"question": "What economic activity offered the most significant prospects for profit in New France?", "options": ["Agriculture", "Iron mining", "The fur trade", "Shipbuilding"], "correct": 2, "explanation": "The fur trade 'undoubtedly attracted the more enterprising individuals since no other activities held out... similar prospects for profit.'"},
    {"question": "Detroit's primary importance continued to be that of a center for:", "options": ["Agricultural production", "Military strategy", "Fur-trading", "Lumber processing"], "correct": 2, "explanation": "Detroit's importance continued to be not that of an agricultural center but that of a fur-trading center."},
    {"question": "The fur trade from Detroit particularly focused on the valleys of which two rivers?", "options": ["Maumee and Wabash", "Ohio and Mississippi", "Detroit and St. Lawrence", "Potomac and Hudson"], "correct": 0, "explanation": "The trade went south 'into the Maumee and Wabash river valleys.'"},
    {"question": "Indian troubles were not immediately menacing after which specific tribe had departed?", "options": ["Iroquois", "Fox", "Huron", "Potawatomi"], "correct": 1, "explanation": "The troubles 'did not take on an immediately menacing aspect... once the Fox had departed.'"},
    {"question": "What French authority figures made an effort to stop fur traders from selling liquor to Native Americans?", "options": ["Local merchants", "Military commanders", "French authorities", "Jesuit missionaries"], "correct": 2, "explanation": "French authorities were known for 'trying to stop French fur traders from selling liquor to the Indians.'"},
    {"question": "Which Jesuit missionary ministered to the Hurons at Detroit?", "options": ["Father Jacques Marquette", "Father Louis Hennepin", "Father Armand de la Richardie", "Father Isaac Jogues"], "correct": 2, "explanation": "Father Armand de la Richardie ministered to the Hurons."},
    {"question": "In what year did the Jesuit missionary move his mission to Bois Blanc Island?", "options": ["1713", "1742", "1760", "1796"], "correct": 1, "explanation": "He transferred his mission to Bois Blanc Island in 1742."},
    {"question": "Why were most of the French habitants noted to be illiterate?", "options": ["They were forbidden to read", "They were too lazy to learn", "Schools were not regularly kept", "Books were unavailable"], "correct": 2, "explanation": "Most of the habitants were illiterate because 'Schools were not regularly kept.'"},
    {"question": "What type of institutions were absent from French colonial community life?", "options": ["Religious institutions", "Military institutions", "Trading institutions", "Democratic institutions"], "correct": 3, "explanation": "The text notes: 'There were no democratic institutions.'"},
    {"question": "The isolated life of Detroiters in the French period was described by the author as:", "options": ["Impoverished and difficult", "In a sense, idyllic", "Constantly besieged", "Overly regulated"], "correct": 1, "explanation": "Detroiters lived an 'isolated and 'in a sense, idyllic life'.'"},
    {"question": "British control over Michigan is noted to have begun in what year?", "options": ["1759", "1760", "1763", "1776"], "correct": 1, "explanation": "British control began in 1760."},
    {"question": "The initial British control in the years following 1760 was described as:", "options": ["Firmly established", "Not firmly established", "Peaceful and prosperous", "Non-existent"], "correct": 1, "explanation": "British control was 'not firmly established' in the early years."},
    {"question": "Which tactic did the British use *before* taking over to gain favor with western tribes?", "options": ["Refusing to trade with them", "Selling liquor", "Cutting off all gifts", "Offering military alliances"], "correct": 1, "explanation": "The British attempted to gain favor by 'Selling the Indians liquor,' a contrast to French authorities."},
    {"question": "What did the British lavishly distribute to Native American tribes *before* taking control?", "options": ["Weapons", "Presents", "Land titles", "Livestock"], "correct": 1, "explanation": "They gained favor by 'Lavishly distributing presents.'"},
    {"question": "The prices the British offered for furs *before* taking control were described as:", "options": ["The same as the French", "Lower than the French", "More than the French had", "Fair market value"], "correct": 2, "explanation": "The British gained favor by 'Paying the Indians more for their furs than the French had.'"},
    {"question": "Who was the British leader responsible for the major policy shift after control was assumed?", "options": ["Colonel Henry Bouquet", "Sir William Johnson", "Major Henry Gladwin", "General Jeffrey Amherst"], "correct": 3, "explanation": "General Jeffrey Amherst instituted the drastic post-1760 policy changes."},
    {"question": "What was the major source of European goods that General Amherst's new policy cut off?", "options": ["Furs", "Gifts", "Iron tools", "Salt"], "correct": 1, "explanation": "Amherst 'cut off the major source of European goods (gifts) to the Indians.'"},
    {"question": "Amherst ordered rigid restrictions on the sale of which item to Native Americans?", "options": ["Tobacco", "Liquor", "Blankets", "Gunpowder"], "correct": 1, "explanation": "Amherst 'ordered rigid restrictions on the sale of liquor.'"},
    {"question": "What was Amherst's policy toward misbehaving Indians?", "options": ["Leniency and understanding", "Negotiation and compromise", "No leniency", "Immediate execution"], "correct": 2, "explanation": "He declared 'no leniency for misbehaving Indians.'"},
    {"question": "Amherst's policy changes were largely responsible for what major historical event?", "options": ["The American Revolution", "The most formidable Indian uprising in American history", "The French and Indian War", "The Treaty of Paris (1763)"], "correct": 1, "explanation": "These changes were largely responsible for 'the most formidable Indian uprising in American history.'"},
    {"question": "Who led the most formidable Indian uprising described in the text?", "options": ["Tecumseh", "Chief Logan", "Pontiac", "Shabbona"], "correct": 2, "explanation": "The uprising was led by Pontiac."},
    {"question": "What crucial post was Pontiac unable to take, contributing to the uprising's failure?", "options": ["Fort Pitt", "Fort Michilimackinac", "Detroit", "Fort Niagara"], "correct": 2, "explanation": "Pontiac's failure was due to his inability to take the crucial post of Detroit."},
    {"question": "What news was the final blow that removed any hope of French aid for the uprising?", "options": ["France's defeat in Europe", "French ceded all land east of the Mississippi", "French troops arriving at the coast", "Spain declaring war on Britain"], "correct": 1, "explanation": "The news that the French had ceded all their lands 'east of the Mississippi to Great Britain' removed hope of French aid."},
    {"question": "What adjective did English/American observers use to describe the French habitants' work ethic?", "options": ["Diligient", "Lazy", "Efficient", "Unskilled"], "correct": 1, "explanation": "They depicted the habitants as an 'essentially lazy lot.'"},
    {"question": "Which term describes the French habitants' literacy level?", "options": ["Highly literate", "Mostly educated", "Illiterate", "Partially schooled"], "correct": 2, "explanation": "'Most of the habitants were illiterate.'"},
    {"question": "The lack of consistent schools led directly to what social condition in French Detroit?", "options": ["Unemployment", "Illiteracy", "Crime", "Emigration"], "correct": 1, "explanation": "Illiteracy was a direct result of schools not being regularly kept."},
    {"question": "The enterprising individuals left other activities because the fur trade offered superior:", "options": ["Safety", "Prospects for profit", "Social standing", "Military protection"], "correct": 1, "explanation": "The text emphasizes the 'prospects for profit' in the fur trade."},
    {"question": "What year did Father de la Richardie move his mission?", "options": ["1713", "1742", "1760", "1796"], "correct": 1, "explanation": "The move to Bois Blanc Island occurred in 1742."},
    {"question": "The French authorities' failure was their inability to shift the economic emphasis away from the:", "options": ["Agriculture", "Fur trade", "Timber industry", "Fishing"], "correct": 1, "explanation": "They failed to shift the emphasis away from the fur trade."},
    {"question": "What was the French colonial government's stance on democratic institutions?", "options": ["Actively promoted them", "Provided limited institutions", "They were absent", "They were encouraged only for merchants"], "correct": 2, "explanation": "They were absent, so politics was absent from the community life."},
    {"question": "The initial British attempt to gain favor involved paying the Indians *what* for their furs?", "options": ["The same rate", "More", "Less", "In liquor only"], "correct": 1, "explanation": "The British paid the Indians 'more for their furs than the French had.'"},
    {"question": "What was the purpose of the British lavishly distributing presents *before* taking control?", "options": ["To celebrate victory", "To recruit soldiers", "To gain favor with western tribes", "To clear the land"], "correct": 2, "explanation": "It was part of their strategy to 'gain favor with western tribes.'"},
    {"question": "General Amherst's policy was defined by a shift from using presents to Native Americans to:", "options": ["Offering more land", "Imposing rigid restrictions", "Negotiating treaties", "Building new forts"], "correct": 1, "explanation": "He shifted from gifts to imposing rigid restrictions."},
    {"question": "The uprising led by Pontiac failed partly because the French cession of land removed the possibility of:", "options": ["Trade with the Spanish", "A French return/aid", "British defeat in Europe", "A Native American government"], "correct": 1, "explanation": "The cession removed the 'hope of French aid.'"},
    {"question": "What kind of people were the habitants, as a group, based on their stock?", "options": ["Aristocratic", "Solid peasant stock", "Wealthy stock", "Land-owning gentry"], "correct": 1, "explanation": "They were of 'good, solid peasant stock.'"},
    {"question": "What was the location of Father de la Richardie's mission after 1742?", "options": ["Bois Blanc Island", "Maumee Valley", "Detroit mainland", "Fort Pitt"], "correct": 0, "explanation": "Bois Blanc Island."},
    {"question": "The French period peace discussed in the text ran until what year?", "options": ["1760", "1744", "1713", "1783"], "correct": 1, "explanation": "The peace period was 1713–1744."},
    {"question": "What best describes the focus of Detroit's fur trade?", "options": ["Eastern markets", "Trade to the south", "Trade to the north", "Overseas exports"], "correct": 1, "explanation": "It focused on the 'trade to the south' into the river valleys."},
    {"question": "The policy change by Amherst was the cause of which type of historical event?", "options": ["A military mutiny", "An Indian uprising", "A trade embargo", "A diplomatic treaty"], "correct": 1, "explanation": "It caused the most formidable Indian uprising."},
    {"question": "The term 'politics (as that term is usually understood)' was described as what in French settlements?", "options": ["Vibrant", "Active", "Absent", "Corrupt"], "correct": 2, "explanation": "The term was 'absent' due to the lack of democracy."},
    {"question": "The British attempted to gain favor with which group of tribes *before* taking control?", "options": ["Eastern tribes", "Southern tribes", "Western tribes", "Coastal tribes"], "correct": 2, "explanation": "The British tried to gain favor with 'western tribes.'"},
    {"question": "Which tribe was ministered to by Father Armand de la Richardie?", "options": ["Fox", "Hurons", "Iroquois", "Ojibwe"], "correct": 1, "explanation": "He ministered to the Hurons."},
    {"question": "What British policy was a direct reversal of the previous French authorities' attempt to restrict liquor sales?", "options": ["Lavishly distributing presents", "Selling the Indians liquor", "Paying more for furs", "Cutting off gifts"], "correct": 1, "explanation": "Selling liquor was the British pre-1760 contrast to the French attempt to stop it."},
    {"question": "What action was taken by General Amherst in response to misbehaving Indians?", "options": ["He negotiated a truce", "He declared no leniency", "He offered new presents", "He ignored them"], "correct": 1, "explanation": "Amherst declared no leniency."},
    {"question": "The habitants were described as hard-working and conservative, contrasting with their depiction as being:", "options": ["Wealthy", "Lazy and irresponsible", "Military leaders", "Overly ambitious"], "correct": 1, "explanation": "Their real character contradicted the 'lazy' and 'irresponsible' depiction."},
    {"question": "Which characteristic of Detroit was *not* its primary importance during the French period?", "options": ["Fur-trading center", "Agricultural center", "Trade center", "Post on the Detroit River"], "correct": 1, "explanation": "Detroit's importance was not that of an 'agricultural center.'"},
    {"question": "What was the final blow to Pontiac's uprising, according to the text?", "options": ["His death", "The arrival of American troops", "French land cession", "Loss of all fort battles"], "correct": 2, "explanation": "The news of the French cession was the point at which 'any hope of French aid' was removed."},
    {"question": "What year did British control of Michigan begin?", "options": ["1713", "1744", "1760", "1796"], "correct": 2, "explanation": "British control began in 1760."},
    {"question": "Amherst's restriction on gifts cut off the Native Americans' major source of:", "options": ["Liquor", "European goods", "Fur trade profits", "Ammunition"], "correct": 1, "explanation": "It cut off the 'major source of European goods.'"},
    {"question": "What was the main reason the more enterprising individuals were attracted to the fur trade?", "options": ["Easy work", "Guaranteed safety", "Profit prospects", "Government subsidies"], "correct": 2, "explanation": "They were attracted by the 'prospects for profit.'"},
    {"question": "The Hurons' mission moved to Bois Blanc Island from where?", "options": ["Mackinac", "Fort Pitt", "Detroit", "Wabash Valley"], "correct": 2, "explanation": "He transferred his mission from Detroit."},
    {"question": "The failure of Detroit's development was blamed on the habitants, which the author corrects by blaming:", "options": ["The British", "The Fox tribe", "French authorities", "The fur traders"], "correct": 2, "explanation": "The text states the failure was 'less the fault of its inhabitants than it was the failure or inability of the French authorities.'"},
    {"question": "What did French authorities attempt to stop the sale of to the Native Americans?", "options": ["Guns", "Whiskey/Liquor", "Tobacco", "Blankets"], "correct": 1, "explanation": "They tried to stop the sale of liquor."},
    {"question": "Which region was *not* mentioned as a destination for Detroit's fur trade?", "options": ["Maumee River Valley", "Wabash River Valley", "Mississippi River Valley", "South"], "correct": 2, "explanation": "It focused on the Maumee and Wabash, trading to the south."},
    {"question": "The habitants were of good, solid stock, suggesting they were:", "options": ["Well-bred and lazy", "Common and industrious", "Conservative and wealthy", "Uneducated and migratory"], "correct": 1, "explanation": "The 'hard-working, conservative folk' were of 'good, solid peasant stock.'"},
    {"question": "What was the consequence of the Fox tribe's departure?", "options": ["Increased Indian troubles", "Indian troubles were less menacing", "British gained control", "The fur trade collapsed"], "correct": 1, "explanation": "The troubles were 'not an immediately menacing aspect... once the Fox had departed.'"},
    {"question": "Which characteristic of the French habitants contradicted English/American observers' views?", "options": ["Their political activity", "Their conservationism", "Their wealth", "Their illiteracy"], "correct": 1, "explanation": "The observers called them 'irresponsible' and 'lazy'; the author calls them 'conservative folk.'"},
    {"question": "What was the British policy regarding paying for furs *before* 1760?", "options": ["Paid less than the French", "Paid the same as the French", "Paid more than the French", "Refused to pay"], "correct": 2, "explanation": "The British paid the Indians 'more for their furs than the French had.'"},
    {"question": "What did General Amherst's policy on liquor sales consist of?", "options": ["Encouragement", "Free distribution", "Rigid restrictions", "Total ban"], "correct": 2, "explanation": "Amherst ordered 'rigid restrictions on the sale of liquor.'"},
    {"question": "The uprising was ultimately classified as the most formidable of its kind in what historical context?", "options": ["World history", "European history", "American history", "Canadian history"], "correct": 2, "explanation": "The most formidable Indian uprising in American history."},
    {"question": "The period of peace mentioned for the French rule was from 1713 to what year?", "options": ["1760", "1744", "1713", "1783"], "correct": 1, "explanation": "The peace period was 1713–1744."},
    {"question": "What was the primary military reason for Pontiac's uprising failing?", "options": ["Loss of all men", "Inability to take Detroit", "Amherst's surprise attack", "A naval blockade"], "correct": 1, "explanation": "He failed because he could not take the crucial post of Detroit."},
    {"question": "The land ceded by the French was specifically located on which side of the Mississippi River?", "options": ["West", "East", "Both sides", "North"], "correct": 1, "explanation": "The French ceded all their lands 'east of the Mississippi to Great Britain.'"},
    {"question": "What best describes the state of British control in Michigan in the years immediately following 1760?", "options": ["Stable", "Contested", "Irrelevant", "Firmly established"], "correct": 1, "explanation": "It was 'not firmly established' and led to the uprising."},
    {"question": "Who was the Jesuit missionary at Detroit?", "options": ["Father Louis Hennepin", "Father Jacques Marquette", "Father Armand de la Richardie", "Father Isaac Jogues"], "correct": 2, "explanation": "Father Armand de la Richardie ministered to the Hurons."},
    {"question": "Amherst's strict policies were largely responsible for what major event?", "options": ["The French and Indian War", "Pontiac's Uprising", "The American Revolution", "The War of 1812"], "correct": 1, "explanation": "The most formidable Indian uprising."},
    {"question": "The French habitants were accurately described as which of the following?", "options": ["Lazy", "Irresponsible", "Hard-working", "Playful"], "correct": 2, "explanation": "They were 'hard-working, conservative folk.'"},
    {"question": "What did the British lavishly distribute to Native American tribes *before* taking control?", "options": ["Guns", "Presents", "Land titles", "Livestock"], "correct": 1, "explanation": "Lavishly distributing presents."},
    {"question": "The lack of schools resulted in most French habitants being:", "options": ["Wealthy", "Illiterate", "Politically active", "Conservative"], "correct": 1, "explanation": "Most of the habitants were illiterate."},
    {"question": "What was absent from French colonial community life due to a lack of democratic institutions?", "options": ["Religion", "Trade", "Politics", "Community"], "correct": 2, "explanation": "Politics (as that term is usually understood) was absent."},
    {"question": "The isolated life of Detroiters was described by the author as, in a sense, what?", "options": ["Harsh", "Idyllic", "Dangerous", "Temporary"], "correct": 1, "explanation": "Idyllic."},
    {"question": "The enterprising individuals were attracted to the fur trade because of superior:", "options": ["Safety", "Prospects for profit", "Social standing", "Military protection"], "correct": 1, "explanation": "Prospects for profit."},
    {"question": "The Fox tribe's departure meant the Indian troubles ceased to have what quality?", "options": ["Frequent", "Menacing", "Religious", "Economic"], "correct": 1, "explanation": "Not an immediately menacing aspect."},
    {"question": "The French authorities' attempts to stop the sale of liquor were aimed at which group?", "options": ["British soldiers", "Native Americans", "French settlers", "American explorers"], "correct": 1, "explanation": "The Indians."},
    {"question": "What year did Father Armand de la Richardie move his mission to Bois Blanc Island?", "options": ["1713", "1742", "1760", "1796"], "correct": 1, "explanation": "1742."},
    {"question": "The British attempted to gain favor with which group of tribes *before* taking control?", "options": ["Eastern tribes", "Southern tribes", "Western tribes", "Coastal tribes"], "correct": 2, "explanation": "Western tribes."},
    {"question": "What did the French cession of land east of the Mississippi to Great Britain remove?", "options": ["Trade restrictions", "Hope of French aid", "British presence", "Pontiac's life"], "correct": 1, "explanation": "Hope of French aid."},
    {"question": "The inhabitants of Detroit lived an isolated and 'in a sense, idyllic life' during which rule?", "options": ["British", "American", "Spanish", "French"], "correct": 3, "explanation": "French period."},
    {"question": "The French authorities were unable to shift the emphasis in New France away from the:", "options": ["Agriculture", "Fur trade", "Timber industry", "Fishing"], "correct": 1, "explanation": "Fur trade."},
    {"question": "Detroit's importance continued to be that of a center for what specific economic activity?", "options": ["Agricultural production", "Military strategy", "Fur-trading", "Lumber processing"], "correct": 2, "explanation": "Fur-trading center."},
    {"question": "What kind of folk were the habitants described as being of 'good, solid' stock?", "options": ["Aristocratic", "Peasant", "Merchant", "Military"], "correct": 1, "explanation": "Peasant stock."},
    {"question": "General Amherst's policy on liquor sales was characterized by:", "options": ["Complete ban", "Open sales to all", "Rigid restrictions", "French control"], "correct": 2, "explanation": "Rigid restrictions."},
    {"question": "Pontiac's uprising was deemed formidable due to its scale in what history?", "options": ["European", "World", "American", "Canadian"], "correct": 2, "explanation": "American history."},
    {"question": "The British tried to gain favor by paying Native Americans what for their furs?", "options": ["The same rate", "More than the French", "Less than the French", "In European goods only"], "correct": 1, "explanation": "More than the French."},
    {"question": "What was the primary reason the French habitants were illiterate?", "options": ["Lack of books", "Lack of desire", "Schools not regularly kept", "Prohibition by clergy"], "correct": 2, "explanation": "Schools were not regularly kept."},
    {"question": "What did the British cut off from Native Americans that served as a 'major source of European goods'?", "options": ["Furs", "Gifts", "Liquor", "Weapons"], "correct": 1, "explanation": "Gifts."},
    {"question": "The Maumee and Wabash river valleys were key to Detroit's fur trade in which direction?", "options": ["North", "South", "East", "West"], "correct": 1, "explanation": "To the south."},
    {"question": "What year marks the start of the French period peace discussed?", "options": ["1760", "1744", "1713", "1796"], "correct": 2, "explanation": "1713."},
    {"question": "The initial lack of British stability after 1760 contributed to what event?", "options": ["French return", "American Revolution", "Pontiac's Uprising", "Economic boom"], "correct": 2, "explanation": "Pontiac's Uprising."},
    {"question": "What were the habitants, as a group, accurately described as being?", "options": ["Lazy", "Irresponsible", "Hard-working", "Playful"], "correct": 2, "explanation": "Hard-working."},
    {"question": "The Jesuit missionary transferred his mission to what specific location?", "options": ["Fort Pitt", "Bois Blanc Island", "Fort Detroit", "Maumee Valley"], "correct": 1, "explanation": "Bois Blanc Island."},
    {"question": "What did the British distribute lavishly *before* the takeover?", "options": ["Taxes", "Presents", "Land deeds", "Furs"], "correct": 1, "explanation": "Presents."},
    {"question": "General Amherst's policy on misbehaving Indians was characterized by what?", "options": ["Leniency", "No leniency", "Compensation", "Warning"], "correct": 1, "explanation": "No leniency."},
    {"question": "The French ceded land located on which side of the Mississippi River?", "options": ["West", "East", "Both sides", "North"], "correct": 1, "explanation": "East."},
    {"question": "The most enterprising individuals were attracted to the fur trade due to what factor?", "options": ["Safety", "Profit", "Adventure", "Subsidies"], "correct": 1, "explanation": "Profit."},
    {"question": "What kind of stock were the French habitants of?", "options": ["Noble", "Peasant", "Military", "Merchant"], "correct": 1, "explanation": "Peasant stock."},
    {"question": "What was the final blow to Native American hopes of French aid?", "options": ["Pontiac's capture", "French land cession", "British naval victory", "Detroit's fall"], "correct": 1, "explanation": "French land cession."},
    {"question": "The British *pre-1760* policy on liquor sales was to:", "options": ["Stop it", "Restrict it rigidly", "Sell it to Indians", "Ban it"], "correct": 2, "explanation": "Selling the Indians liquor."},
    {"question": "The Indian troubles became less immediately menacing after the departure of which tribe?", "options": ["Huron", "Fox", "Ojibwe", "Miami"], "correct": 1, "explanation": "Fox."},
    {"question": "The British rule period ended in what year according to the text?", "options": ["1760", "1796", "1783", "1812"], "correct": 1, "explanation": "1796."},
    {"question": "What was the failure of the French authorities regarding Detroit's development?", "options": ["Lack of military", "Inability to shift to agriculture", "Too much taxation", "Poor trade routes"], "correct": 1, "explanation": "Inability to shift focus to agriculture."},
    {"question": "What crucial post did Pontiac fail to take?", "options": ["Fort Pitt", "Fort Michilimackinac", "Detroit", "Fort Niagara"], "correct": 2, "explanation": "Detroit."},
    {"question": "The French habitants were illiterate primarily due to a lack of what?", "options": ["Books", "Teachers", "Regularly kept schools", "Funding"], "correct": 2, "explanation": "Schools were not regularly kept."},
    {"question": "What was the French authorities' stance on liquor sales to Native Americans?", "options": ["Encouraged", "Tried to stop", "Ignored", "Regulated"], "correct": 1, "explanation": "Tried to stop it."},
    {"question": "What did the British cut off as a major source of European goods?", "options": ["Furs", "Gifts", "Liquor", "Weapons"], "correct": 1, "explanation": "Gifts."},
    {"question": "The absence of democratic institutions meant what was absent in the settlements?", "options": ["Community", "Politics", "Trade", "Religion"], "correct": 1, "explanation": "Politics."},
    {"question": "The French period peace discussed was between 1713 and 1744, a duration of how many years?", "options": ["30", "31", "32", "33"], "correct": 0, "explanation": "1744 - 1713 = 31 years."},
    {"question": "What was the main reason the fur trade attracted more enterprising individuals?", "options": ["Easy work", "Guaranteed safety", "Profit prospects", "Government subsidies"], "correct": 2, "explanation": "Profit prospects."},
    {"question": "Who was the British leader responsible for the strict post-1760 policies?", "options": ["Pontiac", "Amherst", "Cadillac", "De la Richardie"], "correct": 1, "explanation": "General Jeffrey Amherst."},
    {"question": "The French ceded land located east of what river to Great Britain?", "options": ["Ohio", "Mississippi", "Maumee", "Wabash"], "correct": 1, "explanation": "Mississippi."},
    {"question": "What policy did General Amherst order rigid restrictions on the sale of?", "options": ["Furs", "Gifts", "Liquor", "Land"], "correct": 2, "explanation": "Liquor."},
    {"question": "The most formidable Indian uprising was caused by the British policy of:", "options": ["Generosity", "Retaliation", "Restriction", "Diplomacy"], "correct": 2, "explanation": "Restriction (cutting off gifts, restricting liquor)."},
    {"question": "What was a consequence of the British distributing presents *before* 1760?", "options": ["French were pleased", "Western tribes gained favor", "Prices for furs dropped", "War broke out"], "correct": 1, "explanation": "Gained favor with western tribes."},
    {"question": "What kind of folk were the French habitants, according to the author?", "options": ["Lazy", "Irresponsible", "Hard-working", "Playful"], "correct": 2, "explanation": "Hard-working."},
    {"question": "The Huron mission moved to Bois Blanc Island in what year?", "options": ["1713", "1742", "1760", "1796"], "correct": 1, "explanation": "1742."},
    {"question": "Detroit's trade to the south focused on the valleys of which rivers?", "options": ["Ohio and Mississippi", "Maumee and Wabash", "Detroit and St. Lawrence", "Potomac and Hudson"], "correct": 1, "explanation": "Maumee and Wabash river valleys."},
    {"question": "The French habitants were accurately described as being what type of stock?", "options": ["Noble", "Peasant", "Military", "Merchant"], "correct": 1, "explanation": "Peasant stock."},
    {"question": "What was the British policy on paying for furs *before* 1760?", "options": ["More than the French", "Less than the French", "The same rate", "Refused to pay"], "correct": 0, "explanation": "More than the French."},
    {"question": "Who led the most formidable Indian uprising?", "options": ["Tecumseh", "Chief Logan", "Pontiac", "Shabbona"], "correct": 2, "explanation": "Pontiac."},
    {"question": "What was the final blow that removed any hope of French aid?", "options": ["Pontiac's death", "French land cession", "British victory at Detroit", "American intervention"], "correct": 1, "explanation": "French land cession."},
    {"question": "What did the French authorities try to stop the sale of to the Native Americans?", "options": ["Guns", "Whiskey/Liquor", "Tobacco", "Blankets"], "correct": 1, "explanation": "Liquor."},
    {"question": "The isolated life of Detroiters during the French period was described as 'in a sense' what?", "options": ["Harsh", "Idyllic", "Dangerous", "Temporary"], "correct": 1, "explanation": "Idyllic."},
    {"question": "What year did British control of Michigan begin?", "options": ["1759", "1760", "1763", "1776"], "correct": 1, "explanation": "1760."},
    {"question": "What policy did General Amherst impose 'no leniency' for?", "options": ["French authorities", "British soldiers", "Misbehaving Indians", "Fur traders"], "correct": 2, "explanation": "Misbehaving Indians."},
    {"question": "The Huron mission was ministered to by which Jesuit missionary?", "options": ["Father Louis Hennepin", "Father Jacques Marquette", "Father Armand de la Richardie", "Father Isaac Jogues"], "correct": 2, "explanation": "Father Armand de la Richardie."},
]


def award_xp(amount, reason=""):
    st.session_state.total_xp += amount
    milestones = [(500, "Rising Scholar"), (1000, "History Enthusiast"), (1500, "Michigan Expert"), (2000, "Colonial Master"), (2500, "Historical Analyst"), (3000, "ULTIMATE CHAMPION")]
    for threshold, title in milestones:
        if st.session_state.total_xp >= threshold and title not in st.session_state.achievements:
            st.session_state.achievements.append(title)
            if threshold >= 2000:
                st.balloons()
            st.sidebar.success(f"🏆 {title}! ({threshold}+ XP)")
    
    if amount > 0:
        st.sidebar.success(f"⭐ +{amount} XP! {reason}")


def display_quiz():
    st.markdown("## 100 Questions - Immediate Feedback")
    
    if not st.session_state.quiz_started:
        # Hyperlink to Main Page
        st.markdown(f"**<a href='https://his220-launcher.streamlit.app/' target='_self'>⬅️ Go back to Main Page/Quiz Launcher</a>**", unsafe_allow_html=True)

        st.markdown("""
        ### Challenge Overview:
        - **100 Sequential Questions** based on the provided text.
        - **Immediate color-coded feedback**
        - **Up to 3,000+ XP possible**
        """)

        # Resources Section (Added)
        with st.expander("📚 Study Resources"):
            st.markdown(f"""
            This quiz is based on **HIS 220 Week 1-2** content from *Michigan A History of the Wolverine State* by Dunbar & May.

            **To find the answers:** Review the relevant sections of the textbook or the PDF text you uploaded concerning the **French colonial period, the fur trade, and Pontiac's Uprising.**
            
            *If available online, you may search for excerpts or digital copies of the **Third Revised Edition** of the book.*
            """)
        
        if st.button("🚀 BEGIN QUIZ 1", key="start"):
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()
            st.rerun()
        return
    
    if st.session_state.quiz_completed:
        display_results()
        return
    
    # Progress Bar
    st.progress(len(st.session_state.answers) / 100)
    st.caption(f"Progress: {len(st.session_state.answers)}/100")
    
    if hasattr(st.session_state, 'start_time'):
        elapsed = time.time() - st.session_state.start_time
        mins, secs = divmod(int(elapsed), 60)
        st.markdown(f"**Time: {mins:02d}:{secs:02d}**")
    
    st.markdown("### Answer all 100 questions:")
    
    # Display Questions
    for i, q in enumerate(QUESTIONS):
        user_answer = st.session_state.answers.get(i)
        is_correct = user_answer == q["correct"] if user_answer is not None else None
        
        # Color-coded question display
        if is_correct == True:
            st.markdown(f"""
            <div style='background-color: #d4edda; border-left: 5px solid #28a745; padding: 10px; margin: 10px 0; border-radius: 5px;'>
                <strong style='color: #155724;'>✅ Q{i+1}: {q['question']}</strong>
            </div>
            """, unsafe_allow_html=True)
        elif is_correct == False:
            st.markdown(f"""
            <div style='background-color: #f8d7da; border-left: 5px solid #dc3545; padding: 10px; margin: 10px 0; border-radius: 5px;'>
                <strong style='color: #721c24;'>❌ Q{i+1}: {q['question']}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"**Q{i+1}:** {q['question']}")
        
        # Radio buttons
        answer = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"q_{i}",
            index=user_answer if user_answer is not None else None
        )
        
        # Update answer and rerun to show color
        if answer:
            try:
                new_answer = q["options"].index(answer)
            except ValueError:
                return
            
            if st.session_state.answers.get(i) != new_answer:
                st.session_state.answers[i] = new_answer
                time.sleep(0.01)
                st.rerun()
        
        # Show explanation
        if is_correct == False:
            st.error(f"Correct answer: {q['options'][q['correct']]}", icon="💡")
            st.info(f"📖 **Explanation:** {q['explanation']}")
        elif is_correct == True:
            st.success("Correct!")
            with st.expander("📖 Learn more"):
                st.info(q['explanation'])
        
        st.markdown("---")
    
    # Submit button
    if len(st.session_state.answers) == 100:
        if st.button("🎯 COMPLETE QUIZ & VIEW FINAL RESULTS"):
            process_results()

def process_results():
    correct = sum(1 for i, q in enumerate(QUESTIONS) if i in st.session_state.answers and st.session_state.answers[i] == q["correct"])
    st.session_state.final_score = (correct / 100) * 100
    st.session_state.correct_count = correct
    st.session_state.completion_time = (time.time() - st.session_state.start_time) / 60 if hasattr(st.session_state, 'start_time') else 0
    st.session_state.quiz_completed = True
    
    # XP Calculation Logic
    base_xp = correct * 15
    bonus = 0
    
    if st.session_state.final_score == 100:
        bonus = 500
        st.balloons()
        if "Perfect Century" not in st.session_state.achievements:
            st.session_state.achievements.append("Perfect Century")
    elif st.session_state.final_score >= 90:
        bonus = 300
    elif st.session_state.final_score >= 80:
        bonus = 200
    elif st.session_state.final_score >= 70:
        bonus = 100
    else:
        bonus = 50
    
    # Speed Demon Achievement
    if st.session_state.completion_time < 30 and st.session_state.final_score >= 80:
        if "Speed Demon" not in st.session_state.achievements:
            st.session_state.achievements.append("Speed Demon")
        bonus += 150
    
    if "Century Club" not in st.session_state.achievements:
        st.session_state.achievements.append("Century Club")
    
    total_xp = base_xp + bonus
    award_xp(total_xp, f"Challenge: {st.session_state.final_score:.1f}%")
    st.rerun()

def display_results():
    st.markdown("# 🎉 QUIZ 1 COMPLETE!")
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
                st.success(f"✅ Q{i+1}: CORRECT - {q['question']}")
            else:
                st.error(f"❌ Q{i+1}: INCORRECT - {q['question']}")
            with st.expander(f"Context Q{i+1}"):
                st.info(f"Correct: **{q['options'][q['correct']]}**")
                st.markdown(q['explanation'])
    
    if st.session_state.achievements:
        st.markdown("### 🏆 Achievements")
        for ach in st.session_state.achievements:
            st.success(f"🏆 {ach}")
    
    if st.button("🔄 RETAKE QUIZ"):
        st.session_state.quiz_started = False
        st.session_state.answers = {}
        st.session_state.quiz_completed = False
        st.session_state.total_xp = 0
        st.session_state.achievements = []
        st.rerun()
    
    # Hyperlink added after results
    st.markdown("---")
    st.markdown(f"**<a href='https://his220-launcher.streamlit.app/' target='_self'>⬅️ Go back to Main Page/Quiz Launcher</a>**", unsafe_allow_html=True)


# --- Custom Styling (Kept simple) ---
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

# --- Title Header (Updated to remove previous styling) ---
st.markdown("""
<div style='text-align: center; margin: 20px 0;'>
    <h1>🏛️ QUIZ 1: HIS 220 HISTORY OF MICHIGAN</h1>
    <h2>Source: "Michigan A History of the Wolverine State"</h2>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Status ---
st.sidebar.markdown("# 🎯 Challenge Status")
st.sidebar.metric("Total XP", st.session_state.total_xp)
st.sidebar.metric("Achievements", len(st.session_state.achievements))

if st.session_state.quiz_completed:
    st.sidebar.metric("Final Score", f"{st.session_state.final_score:.1f}%")
    
# --- Main App Execution ---
display_quiz()
