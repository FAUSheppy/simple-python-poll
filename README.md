# What is python-simple-poll?
A simple open-source web-based poll, inspired by [Strawpoll](https://www.strawpoll.me/). It's build uppon the [Flask-Microframework](http://flask.pocoo.org/) and supports voting-tokens.

This software is intended to be an easy deployable alternative to more complex solutions like [LimeSurvey](https://www.limesurvey.org).

Also many existing solution use a massive amount of third-party CSS and JavaScript, the resulting web-pages are complex, slow and the overuse of JavaScript in the backend makes it difficult to understand in general. Most also require a full-scale Database setup.

# Running behind a reverse proxy
If you are running the server behind a reverse proxy you need to set a header with the correct hostname. In nginx that would be:

    add_header X-REAL-HOSTNAME $hostname;

# Supported Features
* single choice
* multiple choice
* hide results
* token based voting
* changing your vote [not yet implemented]
* sqlite-backend
* mysql-backend [not yet implemented]