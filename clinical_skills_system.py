import sqlite3

db = sqlite3.connect("clinical_skills.db")
cr = db.cursor()

cr.execute("""
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    progress INTEGER,
    user_id INTEGER
)
""")

staff_id = 1

def show_skills():
    cr.execute("SELECT name, progress FROM skills WHERE user_id = ?", (staff_id,))
    results = cr.fetchall()

    if not results:
        print("No skills found.")
    else:
        for skill in results:
            print(f"{skill[0]} - {skill[1]}%")

def add_skill():
    skill = input("Enter skill: ").strip().lower()

    cr.execute("SELECT * FROM skills WHERE name = ? AND user_id = ?", (skill, staff_id))
    if cr.fetchone():
        print("Skill exists.")
        return

    while True:
        progress = input("Enter progress (0-100): ")
        if progress.isdigit() and 0 <= int(progress) <= 100:
            break
        print("Invalid input.")

    cr.execute("INSERT INTO skills (name, progress, user_id) VALUES (?, ?, ?)",
               (skill, progress, staff_id))
    db.commit()
    print("Skill added.")

def delete_skill():
    skill = input("Enter skill: ").strip().lower()

    cr.execute("DELETE FROM skills WHERE name = ? AND user_id = ?", (skill, staff_id))
    db.commit()

    if cr.rowcount:
        print("Deleted.")
    else:
        print("Not found.")

def update_skill():
    skill = input("Enter skill: ").strip().lower()
    progress = input("Enter new progress: ")

    cr.execute("UPDATE skills SET progress = ? WHERE name = ? AND user_id = ?",
               (progress, skill, staff_id))
    db.commit()

    if cr.rowcount:
        print("Updated.")
    else:
        print("Not found.")


while True:
    choice = input("""
s → Show
a → Add
d → Delete
u → Update
q → Quit
""").lower()

    if choice == "s":
        show_skills()
    elif choice == "a":
        add_skill()
    elif choice == "d":
        delete_skill()
    elif choice == "u":
        update_skill()
    elif choice == "q":
        print("Bye")
        db.close()
        break
    else:
        print("Invalid")
