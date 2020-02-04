CREATE TABLE users (
    username TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    department TEXT NOT NULL,
    user_type TEXT,
    manager_username TEXT,
    salary INTEGER,
    annual_bonus INTEGER,
    vacation_history INTEGER,
    FOREIGN KEY (manager_username) REFERENCES users (username)
);

CREATE TABLE salary_history (
  salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  date_changed TEXT NOT NULL,
  salary INTEGER NOT NULL,
  FOREIGN KEY (username) REFERENCES users (username)
);

INSERT INTO users(username, password, department, user_type, salary, annual_bonus, vacation_history)
VALUES ('manager1', 'testpw123', 'software', 'MANAGER', 1000, 500, 10);

INSERT INTO users(username, password, department, user_type, salary, annual_bonus, vacation_history)
VALUES ('manager2', 'testpw123', 'software', 'MANAGER', 2000, 400, 10);

INSERT INTO users(username, password, department, user_type, manager_username, salary, annual_bonus, vacation_history)
VALUES ('employee1', 'testpw123', 'software', 'EMPLOYEE', 'manager1', 400, 0, 0);

INSERT INTO users(username, password, department, user_type, manager_username, salary, annual_bonus, vacation_history)
VALUES ('employee2', 'testpw123', 'software', 'EMPLOYEE', 'manager1', 600, 100, 5);
INSERT INTO users(username, password, department, user_type, manager_username, salary, annual_bonus, vacation_history)
VALUES ('employee3', 'testpw123', 'software', 'EMPLOYEE', 'manager2', 700, 30, 0);
INSERT INTO users(username, password, department, user_type, manager_username, salary, annual_bonus, vacation_history)
VALUES ('employee4', 'testpw123', 'HR', 'EMPLOYEE', 'manager2', 1500, 200, 8);
INSERT INTO users(username, password, department, user_type) VALUES ('adminuser', 'testpw123', 'software', 'ADMIN');
INSERT INTO salary_history(username, date_changed, salary) VALUES('employee1', DATE('now'), 500);
INSERT INTO salary_history(username, date_changed, salary) VALUES('employee3', DATE('now'), 600);