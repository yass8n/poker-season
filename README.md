# poker-season

## Purpose

The purpose of this python project is to keeps track of poker league standings and enable us to caclulate useful player stats like longest win streak, longest losing streak, avg points per game, etc. In the past we were keeping track of this on a google doc which involved manually inputting and scrunching numbers after each game... not fun! And very prone to human error

## Limitations

We play online at [pokerstars.net](www.pokerstars.net) which doesn't offer an open API for fetching individual game results. Since this feature doesn't exist, we still have to manually input some data after each game.

## Technical Details

* The application is written using the [flask](https://flask.palletsprojects.com/en/1.1.x/) framework. 

* It's hosted for free on [heroku](heroku.com)

* For the UI I used [bootstrap](https://getbootstrap.com/) css library

## Check it out

You can visit the website [here](https://poker-season-app.herokuapp.com/season/2). Please excuse the UI, it's not my passion ;) 

Lastly, Since it is hosted for free on heroku, the server will go to sleep after 30 minutes of inactivity. So expect slow response times for the initial request


