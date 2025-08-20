from encryption import encrypt, decrypt
import sqlite3

# Connect to the database
conn = sqlite3.connect('contest.db')
conn.row_factory = sqlite3.Row  # Allows access by column name

# Drop the BakingContestPeople table if it exists
conn.execute("DROP TABLE IF EXISTS BakingContestPeople")

# Create the BakingContestPeople table
conn.execute("""
    CREATE TABLE BakingContestPeople (
        UserId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Age INTEGER NOT NULL,
        PhNum TEXT NOT NULL,
        SecurityLevel INTEGER NOT NULL,
        LoginPassword TEXT NOT NULL
    )
""")

# Drop the BakingContestEntry table if it exists
conn.execute("DROP TABLE IF EXISTS BakingContestEntry")

# Create the BakingContestEntry table
conn.execute("""
    CREATE TABLE BakingContestEntry (
        EntryId INTEGER PRIMARY KEY AUTOINCREMENT,
        UserId INTEGER NOT NULL,
        NameOfBakingItem TEXT NOT NULL,
        NumExcellentVotes INTEGER NOT NULL,
        NumOkVotes INTEGER NOT NULL,
        NumBadVotes INTEGER NOT NULL,
        FOREIGN KEY(UserId) REFERENCES BakingContestPeople(UserId)
    )
""")

# Add test users with encrypted fields
users = [
    (encrypt("PDiana"), 34, encrypt("1234567890"), 1, encrypt("password1")),
    (encrypt("TJones"), 45, encrypt("0987654321"), 2, encrypt("password2")),
    (encrypt("KarenWorks"), 29, encrypt("1122334455"), 3, encrypt("password3"))
]

for user in users:
    conn.execute("""
        INSERT INTO BakingContestPeople (Name, Age, PhNum, SecurityLevel, LoginPassword)
        VALUES (?, ?, ?, ?, ?)
    """, user)

# test entries to BakingContestEntry
entries = [
    (1, "Chocolate Cake", 5, 3, 2),
    (2, "Vanilla Muffin", 8, 2, 0),
    (3, "Apple Pie", 4, 4, 1)
]

for entry in entries:
    conn.execute("""
        INSERT INTO BakingContestEntry (UserId, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes)
        VALUES (?, ?, ?, ?, ?)
    """, entry)

conn.commit()

# Display the BakingContestPeople table data (decrypted for verification)
cursor = conn.execute("SELECT * FROM BakingContestPeople")
print("BakingContestPeople Table:")
for row in cursor:
    print({
        "UserId": row["UserId"],
        "Name": decrypt(row["Name"]),
        "Age": row["Age"],
        "PhNum": decrypt(row["PhNum"]),
        "SecurityLevel": row["SecurityLevel"],
        "LoginPassword": decrypt(row["LoginPassword"])
    })

# Display the BakingContestEntry table data
cursor = conn.execute("SELECT * FROM BakingContestEntry")
print("\nBakingContestEntry Table:")
for row in cursor:
    print({
        "EntryId": row["EntryId"],
        "UserId": row["UserId"],
        "NameOfBakingItem": row["NameOfBakingItem"],
        "NumExcellentVotes": row["NumExcellentVotes"],
        "NumOkVotes": row["NumOkVotes"],
        "NumBadVotes": row["NumBadVotes"]
    })

conn.close()
