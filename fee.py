import streamlit as st
import pandas as pd
import io

st.title("📄 Medical Fee Lookup App")
st.write("Upload your Excel file to automatically fetch fee details.")

uploaded_file = st.file_uploader("🔼 Upload Your Input Excel File", type=["xlsx"])

SHEET_ID = "1492402795"
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

@st.cache_data
def load_fee_table():
    return pd.read_excel("fee_table.xlsx")  # Master fee table in same folder

if uploaded_file:
    input_df = pd.read_excel(uploaded_file)
    fee_df = load_fee_table()

    # Strip whitespace from headers (optional)
    input_df.columns = input_df.columns.str.strip()
    fee_df.columns = fee_df.columns.str.strip()

    # Merge on State + Institute Name + Quota
    result = pd.merge(
        input_df,
        fee_df,
        on=["State", "Institute Name", "Quota"],
        how="left"
    )

    st.success("✅ Fee details merged successfully!")
    st.dataframe(result.head(15))  # Preview

    towrite = io.BytesIO()
    result.to_excel(towrite, index=False, engine='openpyxl')
    towrite.seek(0)

    st.download_button(
        label="📥 Download Result Excel",
        data=towrite,
        file_name="fee_lookup_result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("⚠️ Please upload your input file to begin.")

