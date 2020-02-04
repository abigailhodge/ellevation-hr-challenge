## HR Management System

### Design idea
I decided to implement this problem as an API using JWTs as authentication/authorization tokens.
Upon login, the user will receive a JWT containing their username, user type (EMPLOYEE, ADMIN, or MANAGER), and their 
department (relevant for HR users). For all further interactions with the system, the user passes in their JWT as a Bearer
token under an authorization header. The API backend decodes the JWT and gets the user claims, and uses these claims to 
determine if the user can do what they're requesting. This is more secure than passing the username/password back and forth
with each request.

### Architecture and Setup Instructions
This is a lightweight  API that uses the python Flask framework, and an in-memory SQLite database. All requirements
can be installed by running 

`pip install -r requirements.txt`

From there, you can start the application by running

`flask run`

The application can be accessed on 127.0.0.1:5000 using your preferred REST client

### Endpoints

####/login
GET: Given a username header and a password header, gives back JWT with user roles. This JWT should be passed into all other
requests as an Authentication: Bearer {JWT} header. Returns a status code of 401 if the user isn't in the system. Check out
initUsers.sql to see what users are already in the system. There are a few Managers, a few non-HR employees, an HR employee,
and an admin user. Note that the JWT expires, and if it expires, you will trigger an Internal Server Error if you try to use
it. I tried to catch this error but the way that Flask wraps its endpoints makes that difficult, so unfortunately it doesn't
return 401. 

####/users 
GET: Gets all users visible to the provided user. If user type is admin, this is every user. If user type is manager, it's all
users with this user as their manager. If user is in the HR department, it's all non-HR users. For all other cases,
it's just the provided user.

POST: Allows Admin and HR users to add new users to the system. User is in the request body and must be in the form
````
{
username: "username",
password: "password",
department: "department",
user_type: "user_type" (Either ADMIN, MANAGER, or EMPLOYEE),
manager_username: "manager_username",
salary: "salary",
annual_bonus: "annual_bonus",
vacation_history: "vacaion_history"

} 
````

####/user/{username}
PUT: Updates the given user, if the user accessing this endpoint has permission. Can include any fields above 
(username, salary, etc.) in the request body, any field provided will be updated in the database. If salary is updated, a new
salary history is automatically created in the salary history table.

####salaries/{username}
GET: Returns all salary history for the given username if the user accessing has permission to view it.


