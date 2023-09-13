# Poker Leaderboard

## Purpose

The purpose of this python project is to keeps track of poker league standings and enable us to caclulate useful player stats like longest win streak, longest losing streak, avg points per game, etc. In the past we were keeping track of this on a google doc which involved manually inputting and scrunching numbers after each game... not fun! And very prone to human error

## Limitations

We play online at [pokerstars.net](www.pokerstars.net) which doesn't offer an open API for fetching individual game results. Since this feature doesn't exist, we still have to manually input some data after each game.

## Technical Details

* Written using [flask](https://flask.palletsprojects.com/en/1.1.x/) framework

* Hosted for free on [heroku](heroku.com)

* MySql database on AWS

* [bootstrap](https://getbootstrap.com/) css library

## Check it out

You can visit the website [here](https://poker-season-app.herokuapp.com/season/2). Please excuse the UI, it's not my passion ;) 

Lastly, Since it is hosted for free on heroku, the server will go to sleep after 30 minutes of inactivity. So expect slow response times for the initial request
_____
Copyright © Yaseen Aniss 2023

All rights reserved. No part of this code may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the copyright owner, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.

For permission requests, please contact anissyaseen@gmail.com


