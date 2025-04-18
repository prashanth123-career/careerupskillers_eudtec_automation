import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime

# --- Authenticate with YOUR service account JSON ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

st.title("📊 AI Sales CRM (Streamlit + Google Sheets)")

st.markdown("💡 Share your Google Sheet with this email: `your-service-account@your-project.iam.gserviceaccount.com`")

sheet_url = st.text_input("🔗 Paste your Google Sheet URL (edit access)", "")

if sheet_url:
    try:
        sheet_key = sheet_url.split("/d/")[1].split("/")[0]
        sheet = client.open_by_key(sheet_key).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        st.success("✅ Connected to your CRM Sheet!")
        st.dataframe(df)

        # Option to add new lead
        with st.form("add_lead_form"):
            st.subheader("➕ Add New Lead")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            status = st.selectbox("Status", ["New", "Follow-Up", "Converted"])
            submit = st.form_submit_button("Add Lead")

            if submit:
                today = datetime.date.today().strftime('%Y-%m-%d')
                sheet.append_row([name, email, phone, status, today])
                st.success("✅ Lead added!")

    except Exception as e:
        st.error(f"❌ Failed to connect: {e}")
