import sqlite3


def get_list_id(connection):
    c = connection.cursor()
    c.execute('SELECT MAX(ID_LISTA) FROM LISTA')
    id = c.fetchone()[0]+1
    if (id is None):
        id = 0
    return id


def new_attendace_list(info):
    connection = sqlite3.connect('clan.db')
    list_id = get_list_id(connection)
    c = connection.cursor()
    c.execute("INSERT INTO LISTA VALUES (?, ?, ?)",
              (list_id, info))
    connection.commit()
    connection.close()
    return list_id


def new_rover(u_id, nickname):
    connection = sqlite3.connect('clan.db')
    c = connection.cursor()
    c.execute("SELECT * FROM ROVER WHERE ID-ID_USUARIO=?", u_id)
    c.execute("INSERT INTO ROVER VALUES (?, ?)", (u_id, nickname))
    connection.commit()
    connection.close()


def add_attendant(u_id, l_id, status):
    connection = sqlite3.connect('clan.db')
    c = connection.cursor()
    # Test if the user has already voted
    result = c.execute('''SELECT * FROM ASISTENCIA WHERE ID_USUARIO=:u_id
    AND ID_LISTA=:l_id''', {'u_id': u_id, 'l_id': l_id})
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
    connection = sqlite3.connect('clan.db')
    c = connection.cursor()
    c.execute("SELECT INFO_L FROM LISTA WHERE ID_LISTA=?", (l_id))
    list_info = c.fetchone()[0]

    # Fetch attendants
    attendants = list()
    non_attendants = list()
    maybe_attendants = list()
    c.execute('''SELECT NOMBRE_U, ESTADO FROM ASISTENCIA NATURAL JOIN ROVER
    WHERE ID_LISTA=?''',
              (l_id))
    untreated_list = c.fetchall()
    connection.close()

    # Treat attendants
    for row in untreated_list:
        if row[1] == 'YES':
            attendants.append(row[0])
        elif row[2] == 'NO':
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
