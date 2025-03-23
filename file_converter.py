import streamlit as st
import pandas as pd
from io import BytesIO

# 🎯 Set page configuration
st.set_page_config(page_title="File Converter", page_icon="🛠️", layout="wide")

# 🔹 Page title and description
st.title("📂 File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# 📤 File uploader (accepts multiple files)
files = st.file_uploader("📥 Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split('.')[-1].lower()

        try:
            # 📝 Read file based on extension
            if ext == 'csv':
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, engine="openpyxl")  # Safer alternative to xlsxwriter for reading

            # 🔍 Show file preview
            st.subheader(f"📋 {file.name} - Preview")
            st.write(f"📝 **File Type:** `{ext.upper()}` | 📏 **Rows:** {df.shape[0]} | 📊 **Columns:** {df.shape[1]}")
            st.dataframe(df.head())

            # 🗑️ Remove duplicates
            if st.checkbox(f"🗑️ Remove Duplicates - {file.name}", key=f"remove_duplicates_{file.name}"):
                df = df.drop_duplicates()
                st.success("✅ Duplicates removed!")
                st.dataframe(df.head())

            # ✍️ Fill missing values
            if st.checkbox(f"📝 Fill Missing Values - {file.name}", key=f"fill_missing_{file.name}"):
                fill_value = st.text_input("Enter a value to fill missing cells:", value="0", key=f"fill_value_{file.name}")
                df.fillna(fill_value, inplace=True)
                st.success("✅ Missing values filled!")
                st.dataframe(df.head())

            # 🔄 Select columns for conversion
            selected_columns = st.multiselect(
                f"🎯 Select Columns to Keep - {file.name}", 
                df.columns.tolist(), 
                default=df.columns.tolist(), 
                key=f"select_columns_{file.name}"
            )
            if selected_columns:
                df = df[selected_columns]
                st.success("✅ Selected columns retained!")
                st.dataframe(df.head())

            # 📊 Show Chart (if numeric columns exist)
            if st.checkbox(f"📊 Show Chart - {file.name}", key=f"show_chart_{file.name}"):
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    st.bar_chart(numeric_df)
                    st.success("✅ Chart displayed!")
                else:
                    st.warning("⚠️ No numeric data available for chart!")

            # 🔄 Choose format conversion
            format_choice = st.radio(f"📌 Convert {file.name} to:", ("CSV", "Excel"), key=f"format_choice_{file.name}")

            # 📥 Download converted file
            if st.button(f"📥 Download {file.name} as {format_choice}", key=f"download_{file.name}"):
                buffer = BytesIO()

                if format_choice == "CSV":
                    df.to_csv(buffer, index=False)
                    mime_type = "text/csv"
                    file_ext = "csv"
                else:
                    df.to_excel(buffer, index=False, engine='xlsxwriter')
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    file_ext = "xlsx"

                buffer.seek(0)
                st.download_button(
                    label=f"📥 Download {file.name} as {file_ext.upper()}",
                    data=buffer,
                    file_name=file.name.replace(ext, file_ext),
                    mime=mime_type
                )
                st.success("✅ Conversion Completed!")

        except Exception as e:
            st.error(f"❌ Error processing {file.name}: {str(e)}")
