import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime

# ------------------- CONFIG -------------------
st.set_page_config(page_title="\ud83d\udd10 Login + CRM + Dashboard", layout="wide")
st.title("\ud83e\udde0 AI Sales Funnel | CRM + Follow-Up")

# ------------------- LOGIN SYSTEM -------------------
st.sidebar.header("\ud83d\udd10 Login")
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")
login_btn = st.sidebar.button("Login")

# Simple demo user (for real use, link with DB)
DEMO_USER = {"email": "admin@careerupskillers.com", "password": "admin123"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if login_btn:
    if email == DEMO_USER["email"] and password == DEMO_USER["password"]:
        st.session_state.logged_in = True
        st.success("\u2705 Login successful!")
    else:
        st.error("\u274c Invalid credentials!")

# ------------------- GOOGLE SHEETS CRM -------------------
if st.session_state.logged_in:

    st.header("\ud83d\udccb Connect CRM (Google Sheets)")
    sheet_url = st.text_input("\ud83d\udd17 Google Sheet URL (with edit access)", "")

    if sheet_url:
        try:
            # Connect to Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("your-google-credentials.json", scope)
            client = gspread.authorize(creds)

            # Extract key from URL
            sheet_key = sheet_url.split("/d/")[1].split("/")[0]
            sheet = client.open_by_key(sheet_key).sheet1
            data = sheet.get_all_records()
            df = pd.DataFrame(data)

            st.success("\u2705 CRM connected!")
            st.subheader("\ud83d\udcc8 Leads Overview")
            st.dataframe(df)

            # ------------------- DASHBOARD -------------------
            st.subheader("\ud83d\udcca Lead Stats")
            if not df.empty:
                st.metric("\ud83d\udcbc Total Leads", len(df))
                today = datetime.date.today().strftime('%Y-%m-%d')
                if 'Date' in df.columns:
                    today_leads = df[df['Date'] == today]
                    st.metric("\u23f3 Today's Leads", len(today_leads))

            # ------------------- FOLLOW-UP & REPORT -------------------
            st.subheader("\ud83d\udd04 Daily Follow-Up Report")
            if not df.empty:
                follow_ups = df[df['Status'].str.lower() == 'pending']
                st.write("\ud83d\udcc5 Pending Follow-Ups:")
                st.dataframe(follow_ups)

                with open("daily_report.txt", "w") as f:
                    f.write("Daily Follow-Up Summary\n")
                    f.write(f"Total Leads: {len(df)}\n")
                    f.write(f"Pending Follow-Ups: {len(follow_ups)}\n")
                    f.write(f"Follow-Up Names: {', '.join(follow_ups['Name']) if 'Name' in follow_ups else ''}\n")
                st.success("\u2705 Daily report generated as 'daily_report.txt'")

        except Exception as e:
            st.error(f"\u274c Could not connect: {e}")
else:
    st.warning("Please login to continue.")
