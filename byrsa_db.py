import sqlite3
from os import environ

DATABASE_PATH = environ.get('BOT_DATABASE_PATH')


def get_list_id(connection):
    c = connection.cursor()
    c.execute('SELECT MAX(ID_LISTA) FROM LISTA')
    id = c.fetchone()[0]
    if (id is None):
        return 0
    else:
        return id+1


def new_attendace_list(info):
    connection = sqlite3.connect(DATABASE_PATH)
    list_id = get_list_id(connection)
    c = connection.cursor()
    c.execute("INSERT INTO LISTA VALUES (?, ?)",
              (list_id, info))
    connection.commit()
    connection.close()
    return list_id


def new_rover(u_id, nickname):
    connection = sqlite3.connect(DATABASE_PATH)
    c = connection.cursor()
    c.execute("SELECT * FROM ROVER WHERE ID_USUARIO=?", (u_id,))
    if (c.fetchone() is None):
        c.execute("INSERT INTO ROVER VALUES (?, ?)", (u_id, nickname))
    else:
        c.execute('UPDATE ROVER SET NOMBRE_U=:nickname WHERE ID_USUARIO=:u_id',
                  {'u_id': u_id, 'nickname': nickname})
    connection.commit()
    connection.close()


def add_attendant(u_id, l_id, status):
    connection = sqlite3.connect(DATABASE_PATH)
    c = connection.cursor()
    # Test if the user has already voted
    c.execute('''SELECT * FROM ASISTENCIA WHERE ID_USUARIO=:u_id
    AND ID_LISTA=:l_id''', {'u_id': u_id, 'l_id': l_id})
    result = c.fetchone()
    # If first time, create new entry. Else modify entry
    if (result is None):
        c.execute("INSERT INTO ASISTENCIA VALUES (?, ?, ?)",
                  (u_id, l_id, status))
    else:
        c.execute('''UPDATE ASISTENCIA SET ESTADO=:status WHERE ID_USUARIO=:u_id
        AND ID_LISTA=:l_id''', {'u_id': u_id, 'l_id': l_id, 'status': status})
    connection.commit()
    connection.close()


def get_attendance_text(l_id):
    # Fetch list name
    connection = sqlite3.connect(DATABASE_PATH)
    c = connection.cursor()
    c.execute("SELECT INFO_L FROM LISTA WHERE ID_LISTA=?", (l_id,))
    list_info = c.fetchone()[0]

    # Fetch attendants
    attendants = list()
    non_attendants = list()
    maybe_attendants = list()
    c.execute('''SELECT NOMBRE_U, ESTADO FROM ASISTENCIA JOIN ROVER
    WHERE ID_LISTA=:l_id''', {'l_id': l_id})
    untreated_list = c.fetchall()
    connection.close()

    # Treat attendants
    for row in untreated_list:
        if row[1] == 'YES':
            attendants.append(row[0])
        elif row[1] == 'NO':
            non_attendants.append(row[0])
        else:
            maybe_attendants.append(row[0])

    # Produce string
    text = "#ASISTENCIA " + list_info + "\nSI:\n"
    for s in attendants:
        text += "-" + s + "\n"
    text += "\nNO:\n"
    for s in non_attendants:
        text += "-" + s + "\n"
    text += "\nDEPENDE:"
    for s in maybe_attendants:
        text += "\n-" + s
    print(text)
    return text
