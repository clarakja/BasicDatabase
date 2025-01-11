import streamlit as st
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect(":memory:")  # 메모리 기반 SQLite DB
cur = conn.cursor()

# Streamlit 앱 제목
st.title("Database Management App")

# 메뉴 선택
menu = st.sidebar.selectbox(
    "Select an Action",
    ["Table Creation", "Insert Data", "Update Data", "Search Data"]
)

# 테이블 생성 기능
if menu == "Table Creation":
    st.header("Create a Table")
    table_name = st.text_input("Enter the table name:")
    columns = st.text_area(
        "Enter column definitions (e.g., id INTEGER PRIMARY KEY, name TEXT NOT NULL):",
        placeholder="id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER"
    )

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

# 데이터 삽입 기능
elif menu == "Insert Data":
    st.header("Insert Data into a Table")
    
    # 생성된 테이블 확인
    st.subheader("Created Tables")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    
    table_name = st.text_input("Enter the table name for insertion:")

    if table_name:
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = cur.fetchall()

        if columns:
            data = {}
            for col in columns:
                col_name = col[1]  # Column name
                col_type = col[2]  # Column type
                data[col_name] = st.text_input(f"Enter value for {col_name} ({col_type}):")

            if st.button("Insert Data"):
                try:
                    col_names = ", ".join(data.keys())
                    placeholders = ", ".join(["?" for _ in data.values()])
                    cur.execute(f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})", tuple(data.values()))
                    conn.commit()
                    st.success(f"Data inserted into '{table_name}' successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning(f"Table '{table_name}' does not exist.")

# 데이터 수정 기능
elif menu == "Update Data":
    st.header("Update Data in a Table")
    table_name = st.text_input("Enter the table name for update:")

    if table_name:
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = cur.fetchall()

        if columns:
            col_to_update = st.selectbox("Select the column to update:", [col[1] for col in columns])
            new_value = st.text_input(f"Enter new value for {col_to_update}:")
            condition = st.text_input("Enter the condition for update (e.g., id=1):")

            if st.button("Update Data"):
                try:
                    cur.execute(f"UPDATE {table_name} SET {col_to_update} = ? WHERE {condition}", (new_value,))
                    conn.commit()
                    st.success(f"Data in '{table_name}' updated successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning(f"Table '{table_name}' does not exist.")

# 데이터 검색 기능
elif menu == "Search Data":
    st.header("Search Data in a Table")
    table_name = st.text_input("Enter the table name for search:")

    if table_name:
        query = st.text_area("Enter your SQL query (e.g., SELECT * FROM table_name WHERE condition):")

        if st.button("Search"):
            try:
                cur.execute(query)
                results = cur.fetchall()
                if results:
                    st.write("Query Results:")
                    for row in results:
                        st.write(row)
                else:
                    st.write("No results found.")
            except Exception as e:
                st.error(f"Error: {e}")

# 데이터베이스 종료 버튼
if st.sidebar.button("Close Connection"):
    cur.close()
    conn.close()
    st.info("Database connection closed.")
