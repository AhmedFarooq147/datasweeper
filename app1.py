import os
import streamlit as st # type: ignore
import pandas as pd # type: ignore
from io import BytesIO



st.set_page_config(page_title="Data Sweeper", layout="wide")
st.markdown(
     """
    <style>
    .main {
        background-color: #f4f4f4;
    }
    .stButton>button {
        background-color:rgb(255, 42, 0);
        color: white;
        font-size: 16px;
        border-radius: 8px;
    }
    .stDownloadButton>button {
        background-color: #28a745;
        color: white;
        font-size: 16px;
        border-radius: 8px;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🧹Data Sweeper")
st.write("This app is used to sweep data from a csv file to xlsx file and vice versa.")

uploaded_files = st.file_uploader("📂Upload a file", type=["csv", "xlsx"])

if uploaded_files:
    file_extension = os.path.splitext(uploaded_files.name)[1].lower()
    if file_extension == ".csv":
        df = pd.read_csv(uploaded_files)
        st.write(df)
    elif file_extension == ".xlsx":
        df = pd.read_excel(uploaded_files)
        st.write(df)
    else:
        st.write(f"Invalid file type: {file_extension}")
    
    st.subheader("🧹 Data Cleaning option")
    if st.checkbox(f"clean data of this {uploaded_files.name}"):
        st.subheader("📌Select columns to keep")
        columns = st.multiselect("Select columns", df.columns,default=df.columns)
        df = df[columns]
        st.write(df)
    
    st.subheader("🔃 Conversion options")
    conversion_type = st.radio(f"convert this {uploaded_files.name} to",["CSV","XLSX"])
    if st.button(f"convert {uploaded_files.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer,index=False)
            file_name = uploaded_files.name.replace(file_extension,".csv")
            mime_type = "text/csv"
        elif conversion_type == "XLSX":
            df.to_excel(buffer,index=False)
            file_name = uploaded_files.name.replace(file_extension,".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
        st.download_button(label="Download",data=buffer,file_name=file_name,mime=mime_type)
        st.success("🎉All files are converted successfully")

