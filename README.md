### YOU CAN CONNECT YOUR POJECTS WITH THIS ```LOGIN``` AND ```REGISTRATION``` PAGES I HAVE MADE SO FOLLOW THESE STEPS AND ALSO THESE ARE AVALABLE IN ```DOCKER HUB```

#### BREIF introduction about it :
- It has a backend file ```(app.py)```
- It has few page which are interconnected using this function  
```html 
<a href="{{ url_for('your_page_name') }}">button_name</a>
```
- You can add your own pages in ```templates``` folder and name it as ```.html```and link them using the above function.
- It also had a ```postgreSQL database``` to store the ```users credientials```
- This all setup is deployed using ```docker```.

#### 🔑 Step 1: Generate an App Password
1️⃣. Go to this link ⬇ 
 ```
 https://myaccount.google.com/apppasswords?utm_source=chatgpt.com
```
2️⃣. And sign in using your gmail.
3️⃣. Click on ```create``` and add your app name then ```create``` it will give a ```16- digit password ```copy it.

![alt text](<Screenshot (47).png>)

4️⃣. Go ```utils.py``` file and add your ```G-mail``` and the ```16-digit password```

![alt text](<Screenshot (48).png>)
in my case this is the password.

### 📒Note: Dont forgot to make step1.

#### Step 2: To start this project using docker
```bash 
docker-compose up --build
```
#### Note : Before build make sure postgreSQL is installed in you docker and then build and start the server.
#### Step 3:To watch the data in database
- Check wheather the postgres is running or not in docker using this command
```bash 
docker ps
```
- you will see the postgresql db is running
```bash 
docker exec -i your_container_name psql -U user_name -d database_name -c "\dt"
```
- In our case
    Container name is ```postgres_db```.
    User name is ```postgres```.
    Database name is ```users_db```.
-
+ It will list the tables created.
+ Go into the table created for user credientials 
+ Run this command in cmd
```bash 
"SELECT * FROM your_table_name;
```
In our case table name is ```users```

- Now you can watch the data stored in the databse.
- To delete ```all the data``` in the Database run this command
```bash
DELETE FROM users;
```
- To delete ```Specific row data``` in database
```bash
DELETE FROM users WHERE id = 1;
```
- Change the id = which row you want to delete.
- Run this command to exit
```bash
\q
```





