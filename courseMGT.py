import sqlite3

# 데이터베이스 초기화 함수
def initialize_database():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    
    # 기존 테이블 삭제 (올바른 동작을 위하여 혹시 남아 있을 잔재를 삭제)
    cursor.execute("DROP TABLE IF EXISTS Enrollments")
    cursor.execute("DROP TABLE IF EXISTS Students")
    cursor.execute("DROP TABLE IF EXISTS Courses")

    # 학생 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    ''')

    # 강의 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        course_code TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        credits INTEGER NOT NULL
    )
    ''')

    # 학생-강의 관계 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        course_code TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (course_code) REFERENCES Courses(course_code)
    )
    ''')

    conn.commit()
    conn.close()

# 학생 추가 함수
def add_student(student_id, name, email, phone):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Students (student_id, name, email, phone) VALUES (?, ?, ?, ?)", (student_id, name, email, phone))
    conn.commit()
    conn.close()

# 강의 추가 함수
def add_course(course_code, title, credits):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Courses (course_code, title, credits) VALUES (?, ?, ?)", (course_code, title, credits))
    conn.commit()
    conn.close()

# 수강 신청 함수
def enroll_student(student_id, course_code):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Enrollments (student_id, course_code) VALUES (?, ?)", (student_id, course_code))
    conn.commit()
    conn.close()

# 학생 목록 조회 함수
def view_students():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    conn.close()

    return students

# 강의 목록 조회 함수
def view_courses():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Courses")
    courses = cursor.fetchall()
    conn.close()

    return courses

# 학생 수강 내역 조회 함수
def view_enrollments():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT Students.name, Courses.title
    FROM Enrollments
    JOIN Students ON Enrollments.student_id = Students.student_id
    JOIN Courses ON Enrollments.course_code = Courses.course_code
    ''')

    enrollments = cursor.fetchall()
    conn.close()

    return enrollments

# 메인 실행 함수
def main():
    initialize_database()

    while True:
        print("\n=== 학사관리 시스템 ===")
        print("1. 학생 추가")
        print("2. 강의 추가")
        print("3. 수강 신청")
        print("4. 학생 목록 보기")
        print("5. 강의 목록 보기")
        print("6. 수강 내역 보기")
        print("7. 종료")

        choice = input("선택: ")

        if choice == "1":
            student_id = input("학번: ")
            name = input("학생 이름: ")
            email = input("이메일: ")
            phone = input("전화번호: ")
            add_student(student_id, name, email, phone)
            print("학생이 추가되었습니다.")

        elif choice == "2":
            course_code = input("과목 코드: ")
            title = input("강의 제목: ")
            credits = int(input("강의 학점: "))
            add_course(course_code, title, credits)
            print("강의가 추가되었습니다.")

        elif choice == "3":
            student_id = input("학생 학번: ")
            course_code = input("강의 코드: ")
            enroll_student(student_id, course_code)
            print("수강 신청이 완료되었습니다.")

        elif choice == "4":
            students = view_students()
            print("\n=== 학생 목록 ===")
            for student in students:
                print(f"학번: {student[0]}, 이름: {student[1]}, 이메일: {student[2]}, 전화번호: {student[3]}")

        elif choice == "5":
            courses = view_courses()
            print("\n=== 강의 목록 ===")
            for course in courses:
                print(f"과목 코드: {course[0]}, 제목: {course[1]}, 학점: {course[2]}")

        elif choice == "6":
            enrollments = view_enrollments()
            print("\n=== 수강 내역 ===")
            for enrollment in enrollments:
                print(f"학생: {enrollment[0]}, 강의: {enrollment[1]}")

        elif choice == "7":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 선택입니다. 다시 시도하세요.")

# 프로그램 실행
if __name__ == "__main__":
    main()
