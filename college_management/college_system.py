import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",password="",database="college")
command_handler = db.cursor(buffered=True)

def student_session(username):
    while 1:
        print("")
        print("Student Menu")
        print("1. View Register")
        print("2. Download Register")
        print("3. Logout")
        user_option = input(str("[~] Option : "))

        if user_option == "1":
            print("Displaying Register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()

            for record in records:
                print("Username : ",record[1] + "       Date : ",record[0] + "      Status : ", record[2])
        
        elif user_option == "2":
            print("Downloading Register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()

            for record in records:
                with open("Register.txt","w") as file:
                    file.write(str(records))
                file.close()
            print("[+] All Records Downloaded Successfully")
        elif user_option == "3":
            print("Logged Out\n")
            break
        

def auth_student():
    print("")
    print("Student Login\n")
    username = input(str("[~] Username : "))
    password = input(str("[~] Password : "))
    query_values = (username,password)
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = 'student'",query_values)
    #username = command_handler.fetchone()

    if command_handler.rowcount <= 0:
        print("[-] Login Details Not Recogized")
    else:
        student_session(username)


def teacher_session():
    while 1:
        print("")
        print("Teachers Menu\n")
        print("1. Mark Student Register")
        print("2. View Register")
        print("3. Logout")

        user_option = input(str("[~] Option : "))
        if user_option == "1":
            print("")
            print("Marking Student Register")
            command_handler.execute("SELECT username FROM  users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("[~] Date : DD/MM/YYY : "))

            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")

                status = input(str("[~] Status For " + str(record) + " ( P/A/L ) : "))
                query_values = (str(record),date,status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES (%s,%s,%s)",query_values)
                db.commit()
                print("[+] " + record + " Marked As " + status)

        elif user_option == "2":
            print("")
            print("Viewing Student Register")
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            print("Displaying Student Register")
            
            for record in records:
                print("Username : ",record[0] + "       Date : ",record[1] + "      Status : ", record[2])
                print("")
        elif  user_option == "3":
            print("")
            print("[+] Logged Out")
            break
        else:
            print("[x] No valid option selected")





def administrator_session():
    while 1:
        print("")
        print("Administrator Menu\n")
        print("1. Register New Student")
        print("2. Register New Teacher")
        print("3. Delete Existing Student")
        print("4. Delete Existing Teacher")
        print("5. Log Out")

        user_option = input(str("[~] Option : "))
        if user_option == "1":
            print("")
            print("Register New Student")
            username = input(str("[~] Student username : "))
            password = input(str("[~] Student password : "))
            query_values = (username,password)
            command_handler.execute("INSERT INTO users(username, password,privilege) VALUES (%s,%s,'student')",query_values)
            db.commit()
            print("[+] " + username + " has been registered successfully as a student.")
        
        elif user_option == "2":
            print("")
            print("Register New Teacher")
            username = input(str("[~] Teacher username : "))
            password = input(str("[~] Teacher password : "))
            query_values = (username,password)
            command_handler.execute("INSERT INTO users(username, password,privilege) VALUES (%s,%s,'teacher')",query_values)
            db.commit()
            print("[+] " + username + " has been registered as successfully a teacher.")

        elif user_option == "3":
            print("")
            print("Delete Existing Student Account\n")
            username = input(str("[~] Student username : "))
            query_values = (username,'student')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s",query_values)
            db.commit()
            if command_handler.rowcount < 1:
                print("[-] User not found")
            else:
                print(username + " has been deleted successfully")

        elif user_option == "4":
            print("")
            print("Delete Existing Teacher Account\n")
            username = input(str("[~] Teacher username : "))
            query_values = (username,'teacher')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s",query_values)
            db.commit()
            if command_handler.rowcount < 1:
                print("[-] User not found")
            else:
                print(username + " has been deleted successfully")
        
        elif user_option == "5":
            break
        
        else:
            print("[x] No Valid Option Selected!")


def auth_administrator():
    print("")
    print("Administration Login\n")
    username = input(str("[~] Username : "))
    password = input(str("[~] Password : "))

    if username == "admin":
        if password == "password":
            administrator_session()
        else:
            print("Incorrect password!")
    else:
        print("[-] Login Details Not Recognized")

def auth_teacher():
    print("")
    print("Teacher Login\n")
    username = input(str("[~] Username : "))
    password = input(str("[~] Password : "))
    query_values = (username,password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'",query_values)
    if command_handler.rowcount <= 0:
        print("[-] Login Details Not Recognized\n")
    else:
        teacher_session()


def main():
    while 1:
        print("Welcome To The College System\n")
        print("1. Login as Student")
        print("2. Login as Teacher")
        print("3. Login as Administrator")

        user_option = input(str("[~] Option : "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_administrator()
        else:
            print("No valid option was selected")


main()