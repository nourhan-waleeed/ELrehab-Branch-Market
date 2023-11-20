# Elrehab Branch Market
dashboard using dash plotly and deploy it on heroku 
https://elrehab788-fathallah-f034065f8442.herokuapp.com/
heroku steps:

1) open the terminal, cd folder_location
2) to remove any previous git init  ( rmdir /s /q .git ) 
3) git init 
4) git add . 
5) git commit -m "initial commit"
6) heroku login
7) heroku create -n "app_name"
8) heroku git:remote -a app_name
9) git push heroku master
10) heroku ps:scale web=1
# for update
11) login
12) cd to folder
13) heroku git:clone -a elrehab788-fathallah
14) cd elrehab788-fathallah
15) git add .
16) git commit -am "make it better"
17) git push heroku master
