# Database Documentation 

### Created by Emanuel, Tim, Kevin on November 10, 2019
#### Explains the basics for using the MySQL database with Python and Jinja. 

## Database 

MySQL Reference Manual: https://dev.mysql.com/doc/refman/8.0/en/

## To Make a Query From The Database: 

An example of searching the database:

`SELECT P.title, P.description, C.name, P.image FROM posts P, categories C WHERE P.category = C.cID AND C.name = '%s'" %(category)`

In the above statement, the query is requesting from the database the title and description of the post, the name of the category, and an image of the post that have the conditions: post category name and categories ID match, and the name of the categories is entered. It is pulling from the tables: “posts” and “categories”

Syntax of the query:
Select [columns] from [table1], [table2], etc where [conditions] 

### In app.py file:

Import Flask mysql by putting the following line in the file:

`from flaskext.mysql import MySQL`

Configure the MySQL database in the following way:

```
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'DATABASE NAME'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
```

In the function that’s going to query the database use:

```
conn = mysql.connect()
cursor = conn.cursor()
```
**If you do this outside of the function being used, the connection to the database will timeout and crash the app!!!**

The actual query should be done as follows (in the function requiring the query): 

```
cursor.execute(*QUERY*)
conn.commit()
```

Put the string query inside the cursor.execute function call *this follows MySQL syntax*.



To retrieve the data queried, use:

`data = cursor.fetchall()`

Where data will be the field that is returned to the html file.

To render the template after querying, and pass the data from the query to the html file:

```
return render_template(‘HTML PAGE YOU WANT TO RENDER’, LIST OF DATA YOU WANT TO RENDER)

E.g. return render_template(‘search.html’, query=query, data=data, cats=cats)

The above example renders the template with query = text entered in search bar (to make it persistence), data = data retrieved from database, and cats = category names.
```




### IN THE HTML FILE requiring the data

Python uses *jinja* to handle data templating/templating in the html files. 

Official Jinja documentation: https://jinja.palletsprojects.com/en/2.10.x/

Jinja uses braces: ``{{}}`` to denote data fields; and allows for some basic features such as loops, concatenation, basic calculations/operators, etc. 

To insert the data from the query, if the query contained a single data item (i.e. a single string), it can be inserted into ANY html: 

`<p>{{ data }}</p>`

If the query requested multiple fields, from multiple columns or tables, the data should be stored in a list of tuples and can be accessed dynamically: 

```
{% for cat in cats %}
<option> {{cat[0]}} </option>
{% endfor %}
```
Where each cat in cats is an entry, and the index is the specific field (i.e. `cat[0]` is the name)

**MySQL Server

To access the MySQL server, log into MySQL using:

`mysql -u root -p`

Then type in the password and hit enter:

`password`

To learn how to use MySQL, refer to the MySQL Reference Manual.





# NEW DATABASE MANAGEMENT THROUGH FLASK-MIGRATE:

## To create the db migration repo (**Not a git repo**): 
Enter the following in the terminal (inside the project)
  `$ flask db init`

This assumes that the environment variable Flaskapp was set up via 

`$ FLASK_APP=buysell.py`

and uses the `flask` command with flask-migrate's added db functionality.

Flask-migrate supports version control: 

With the migration repo in place, the first database migration us done via: 

`flask db migrate`

where the flag `-m <message content>` can be used to specify the changes in the migration.

`flask db upgrade` applies the changes to the database

`flask db downgrade` removes the last changes to the database.

**Note that in MySQL the database has to be created via the mysql shell *BEFORE* upgrading.**

Also note that Flask-SQLAlchemy uses snake_case by default, such that table names will be applied as follows: 

User becomes **user**

AddressAndPhone becomes **address_and_phone**

However this can be changed by adding the attr. `__tablename__` to the corresponding class