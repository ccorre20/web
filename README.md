The project contained within this folder is made up of a series of scripts and models, made for deployment on the
Heroku PaaS as a Flask Web application. The models used for this project were constructed using the companion scripts in
the other part of the project.

The other part of this project can be found at: https://github.com/ccorre20/Reto3

Within this folder you will find:

app.py: This contains the main code for image handling and rendering the website.

processing.py: This contains methods for loading the models, processing incoming images and rendering the results.

*.pkl: These are the models to be used by the application.

requirements.txt: This contains the python dependencies so that the software may run on the container. It is similar to a
Pipfile.

Aptfile: This defines a collection of apt-get packages to be installed on the heroku vm for it to function adequately.

Procfile: This defines how heroku will launch the web application.

In order to deploy this project, it is necessary to use the following buildpack https://github.com/heroku/heroku-buildpack-apt

