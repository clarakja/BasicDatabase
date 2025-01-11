import streamlit as st
import sqlite3

# Streamlit 앱 제목
st.title("Dynamic Table Creator")

# 데이터베이스 연결
conn = sqlite3.connect(":memory:")  # 메모리 기반 SQLite DB
cur = conn.cursor()

# 사용자 입력 섹션
st.header("Table Information")
table_name = st.text_input("Enter the table name:")

st.subheader("Define Table Columns")
columns = st.text_area(
    "Enter column definitions (e.g., id INTEGER PRIMARY KEY, name TEXT NOT NULL):",
    placeholder="id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER"
)

# 테이블 생성 버튼
if st.button("Create Table"):
    if table_name and columns:
        try:
            # SQL 명령어 실행
            create_table_query = f"CREATE TABLE {table_name} ({columns});"
            cur.execute(create_table_query)
            conn.commit()
            st.success(f"Table '{table_name}' created successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please provide both table name and column definitions.")

# 생성된 테이블 확인
st.subheader("Created Tables")
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

if tables:
    st.write("Existing Tables in Database:")
    for table in tables:
        st.write(f"- {table[0]}")
else:
    st.write("No tables created yet.")

# 데이터베이스 종료
if st.button("Close Connection"):
    cur.close()
    conn.close()
    st.info("Database connection closed.")
