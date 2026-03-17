import sqlite3

db = sqlite3.connect("clinical_skills.db")
cr = db.cursor()

def commit_and_close():
    db.commit()
    db.close()
    print("Database connection closed")

staff_id = 1

input_message = """

Clinical Skills Management System

What do you want to do?

s → Show all clinical skills
a → Add a new clinical skill
d → Delete a skill
u → Update skill progress
q → Quit

Choose option:
"""

user_input = input(input_message).strip().lower()

commands_list = ["s", "a", "d", "u", "q"]

def show_skills():
    cr.execute("SELECT name, progress FROM skills WHERE user_id = ?", (staff_id,))
    results = cr.fetchall()

    print(f"\nYou have {len(results)} clinical skills recorded:")

    if len(results) == 0:
        print("No clinical skills recorded yet.")
    else:
        for skill in results:
            print(f"Skill: {skill[0]} | Progress: {skill[1]}")

    commit_and_close()

def add_skill():
    skill = input("Enter clinical skill name: ").strip().capitalize()

    cr.execute("SELECT name FROM skills WHERE name = ? AND user_id = ?", (skill, staff_id))
    result = cr.fetchone()

    if result:
        print("Skill already exists.")
    else:
        progress = input("Enter training progress (%): ").strip()
        cr.execute(
            "INSERT INTO skills (name, progress, user_id) VALUES (?, ?, ?)",
            (skill, progress, staff_id)
        )
        print("Clinical skill added.")

    commit_and_close()

def delete_skill():
    skill = input("Enter clinical skill name to delete: ").strip().capitalize()

    cr.execute(
        "DELETE FROM skills WHERE name = ? AND user_id = ?",
        (skill, staff_id)
    )

    print("Skill removed.")
    commit_and_close()

def update_skill():
    skill = input("Enter clinical skill name: ").strip().capitalize()
    progress = input("Enter new progress (%): ").strip()

    cr.execute(
        "UPDATE skills SET progress = ? WHERE name = ? AND user_id = ?",
        (progress, skill, staff_id)
    )

    print("Skill progress updated.")
    commit_and_close()

if user_input in commands_list:

    if user_input == "s":
        show_skills()

    elif user_input == "a":
        add_skill()

    elif user_input == "d":
        delete_skill()

    elif user_input == "u":
        update_skill()

    else:
        print("Exiting system")

else:
    print("Invalid command")
