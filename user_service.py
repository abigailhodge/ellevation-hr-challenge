import sqlite3

DATABASE = ':memory:'
db = None


def init_db():
    global db
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    with open('initUsers.sql', 'r') as file:
        cur.executescript(file.read())
        print('inited db')
        db.commit()


def rows_to_obj(rows, vals):
    obj_list = []
    for row in rows:
        obj = {}
        for val in vals:
            obj[val] = row[val]
        obj_list.append(obj)
    return obj_list


def insert_user(user):
    global db
    cur = db.cursor()
    cur.execute('INSERT INTO users(username, password, department, user_type, manager_username, '
                'salary, annual_bonus, vacation_history) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [user['username'], user['password'], user['department'], user['user_type'], user['manager_username'],
                 user['salary'], user['annual_bonus'], user['vacation_history']])
    db.commit()


def get_user_info(username, password):
    global db
    cur = db.cursor()
    cur.execute('SELECT username, user_type, department FROM users WHERE username=? AND password=?', [username, password])
    return cur.fetchone()


def get_managed_users(username):
    global db
    cur = db.cursor()
    cur.execute('SELECT * FROM users WHERE manager_username=?', [username])
    rows = cur.fetchall()
    return rows_to_obj(rows, ['username', 'password', 'department', 'user_type', 'manager_username',
                              'salary', 'annual_bonus', 'vacation_history'])


def get_non_hr_users():
    global db
    cur = db.cursor()
    cur.execute('SELECT * FROM users WHERE  department !=\'HR\'')
    rows = cur.fetchall()
    return rows_to_obj(rows, ['username', 'password', 'department', 'user_type', 'manager_username',
                              'salary', 'annual_bonus', 'vacation_history'])


def get_all_users():
    global db
    cur = db.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    return rows_to_obj(rows, ['username', 'password', 'department', 'user_type', 'manager_username',
                              'salary', 'annual_bonus', 'vacation_history'])


def get_user(username):
    global db
    cur = db.cursor()
    cur.execute('SELECT * FROM users where username=?', [username])
    rows = [cur.fetchone()]
    return rows_to_obj(rows, ['username', 'password', 'department', 'user_type', 'manager_username',
                              'salary', 'annual_bonus', 'vacation_history'])


def get_user_if_can_edit(user_type, department, username, user):
    global db
    cur = db.cursor()
    if department == 'HR':
        cur.execute('SELECT * FROM users WHERE username=? AND department !=?', [user, 'HR'])
        row = [cur.fetchone()]
    if user_type == 'ADMIN':
        cur.execute('SELECT * FROM users WHERE username=?', [user])
        row = [cur.fetchone()]
    if user_type == 'MANAGER':
        cur.execute('SELECT * FROM users WHERE username=? AND manager_username=?', [user, username])
        row = [cur.fetchone()]
    if row:
        return rows_to_obj(row, ['username', 'password', 'department', 'user_type', 'manager_username',
                                 'salary', 'annual_bonus', 'vacation_history'])
    else:
        return None


def get_salary_if_can_view(user_type, department, username, user):
    global db
    cur = db.cursor()
    if department == 'HR':
        cur.execute('SELECT sh.username, sh.salary, sh.date_changed ' 
                    'FROM salary_history sh ' 
                    'INNER JOIN users u ON u.username = sh.username '
                    'WHERE u.username=? AND u.department!=?', [user, 'HR'])
        rows = cur.fetchall()
    if user_type == 'ADMIN':
        cur.execute('SELECT sh.username, sh.salary, sh.date_changed ' 
                    'FROM salary_history sh ' 
                    'INNER JOIN users u ON u.username = sh.username '
                    'WHERE u.username=?', [user])
        rows = cur.fetchall()
    if user_type == 'MANAGER':
        cur.execute('SELECT sh.username, sh.salary, sh.date_changed ' 
                    'FROM salary_history sh ' 
                    'INNER JOIN users u ON u.username = sh.username '
                    'WHERE u.username=? AND u.manager_username=?', [user, username])
        rows = cur.fetchall()
    if rows:
        return rows_to_obj(rows, ['username', 'salary', 'date_changed'])
    else:
        return None


def update_user_salary(username, salary):
    global db
    cur = db.cursor()
    cur.execute('INSERT INTO salary_history(username, date_changed, salary) VALUES(?, DATE(\'now\', \'localtime\'), ?)',
                [username,  salary])
    db.commit()


def replace_user(user):
    global db
    cur = db.cursor()
    cur.execute('REPLACE INTO users(username, password, department, user_type, manager_username, '
                'salary, annual_bonus, vacation_history) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [user['username'], user['password'], user['department'], user['user_type'], user['manager_username'],
                 user['salary'], user['annual_bonus'], user['vacation_history']])
    db.commit()

