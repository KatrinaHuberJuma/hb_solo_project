![Pair of pears logo](/static/img/pear23.png)

# Pair Necessities

![lab page](/static/img/labDetailsPage.png  =300x)

Pair Necessities is a reference tool for bootcamp students to keep track of lab content and pair programming history. Admin can login, create cohorts, create labs and pair students for labs. 

![Admin view of lab page](/static/img/pairStudentsforLab.png  =300x)

A student can login to a cohort she has already joined, or, if she enters the correct cohort password, join a cohort. She can find labs by keyword, add keywords to a lab, find the instructions and see who she paired with, and edit the notes she shares with her lab pair, so that she can keep track of learnings. She can also edit her profile or change her personal password.

## Installation
##### Requires PostgreSQL
+ `createdb katfuntest`
+ git clone the repo
+ inside this directory, create a secret.sh file containing:
```export secret_key="your_random_string_here"```
+ inside this directory, create a virtual environment
+ activate virtual environment
+ pip install requirements 
+ ```source secret.sh```
+ `python test_seed.py` to create tables and seed the database
+ `python server.py` to run the server
+ open your browser to *localhost:5000*

## Tech Stack
+ Python
+ unittest
+ selenium
+ SQLAlchemy
+ Postgresql
+ flask
+ jinja
+ JavaScript
+ jQuery
+ ajax
+ bootstrap


## Credits

A jQuery plugin, [Multiselect](http://loudev.com/), was used for grouping students into pairs.
[Gravatar](https://en.gravatar.com/site/implement/) was used for student profile pictures

