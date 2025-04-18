import streamlit as st
import requests
import datetime

# ----------------- CONFIG -----------------
st.set_page_config(page_title="AI Growth Assistant", layout="wide")
RAZORPAY_PAYMENT_LINK = "https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view"
MAX_FREE_USAGE = 5  # Max free actions before asking for payment

# ----------------- USER LOGIN -----------------
st.title("🚀 AI Growth Assistant for EdTech")
user_email = st.text_input("Enter your email to get started")
session_id = f"{user_email}-{datetime.date.today()}"

if "usage" not in st.session_state:
    st.session_state.usage = 0

# ----------------- USAGE TRACKING -----------------
def track_usage():
    st.session_state.usage += 1

def check_limit():
    return st.session_state.usage >= MAX_FREE_USAGE

# ----------------- PAYMENT GATE -----------------
if check_limit():
    st.warning("You’ve reached your free usage limit.")
    st.markdown(f"**[Unlock Full Access ₹499]({RAZORPAY_PAYMENT_LINK})**")
    st.stop()

# ----------------- MARKET RESEARCH -----------------
st.header("📊 Market Research (Gemini Style)")

topic = st.text_input("What topic or course do you want to research?", "AI for Schools")

if st.button("Run Market Research"):
    research_output = f"""
    🔍 *Market trends on*: **{topic}**

    - Demand for AI in education has surged 200% since 2022.
    - Students aged 13–22 are increasingly interested in gamified learning.
    - Top keywords: "AI for students", "future skills", "coding with AI".
    - Competitor: LearnAI, OpenAI Academy, Byju's AI Labs

    *(Generated using Gemini-style intelligence – based on public data)*
    """
    track_usage()
    st.success("Market research completed!")
    st.markdown(research_output)

# ----------------- AD COPY GENERATOR -----------------
st.header("✍️ Ad Copy Generator")

platform = st.selectbox("Choose Platform", ["Facebook", "Instagram", "Google", "LinkedIn", "YouTube"])
headline = st.text_input("Ad Headline", "Unlock the Power of AI in Education")
benefit = st.text_area("Highlight the Benefit", "Learn AI from scratch and boost your career in tech")

if st.button("Generate Ad Copy"):
    ad_text = f"""
    ✅ **Platform**: {platform}
    ✍️ **Ad Copy**:
    “{headline}”  
    {benefit}  
    Start your journey today. Limited seats available!
    """
    track_usage()
    st.success("Ad copy generated!")
    st.code(ad_text)

# ----------------- WHATSAPP & EMAIL AUTOMATION -----------------
st.header("📬 Lead Follow-Up Automation")

with st.form("lead_form"):
    lead_name = st.text_input("Lead Name", "John Doe")
    lead_email = st.text_input("Lead Email", "john@example.com")
    lead_phone = st.text_input("Lead WhatsApp Number", "+91XXXXXXXXXX")
    submit = st.form_submit_button("Send WhatsApp & Email Follow-Up")

if submit:
    webhook_url = "https://n8n.yourdomain.com/webhook/lead_followup"  # Replace with your actual n8n webhook URL
    payload = {
        "name": lead_name,
        "email": lead_email,
        "phone": lead_phone,
        "message": f"Hi {lead_name}, thank you for showing interest in our AI courses! Let’s get you started."
    }
    try:
        res = requests.post(webhook_url, json=payload)
        if res.status_code == 200:
            track_usage()
            st.success("Follow-up sent via WhatsApp and Email!")
        else:
            st.error("Failed to send follow-up. Check n8n webhook.")
    except Exception as e:
        st.error(f"Error: {e}")

# ----------------- INNOVATIVE BONUS FEATURES -----------------
st.header("🎁 Bonus: Download Lead Script")

if st.button("Download Free Follow-Up Script"):
    sample_text = f"""
    Subject: Welcome to AI Future, {lead_name}!

    Dear {lead_name},

    Thank you for your interest in our AI programs. Here's how you can benefit:
    - Learn directly from industry experts
    - Hands-on real projects
    - Career support included

    Click to know more: https://careerupskillers.com/ai-course
    """
    st.download_button("📩 Download Follow-Up Script", data=sample_text, file_name="FollowupScript.txt")

# ----------------- SIDEBAR -----------------
st.sidebar.markdown("✅ **Free Tier:** 5 actions/day")
st.sidebar.markdown("💰 [Upgrade to Full Access](" + RAZORPAY_PAYMENT_LINK + ")")
