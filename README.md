# RAMP GUI
This is a graphical user interface for the load profile generation software [RAMP](https://rampdemand.org/).

The graphical user interface was developed by the 
[Information Systems Institute](https://iwi.uni-hannover.de) at Leibniz Universität Hannover, Germany, during the development of the energy system simulator [NESSI](https://nessi.iwi.uni-hannover.de).

The development process of the RAMP GUI is described in the following publication:

Maria C.G. Hart, Sarah Eckhoff, Michael H. Breitner (2023): [Sustainable Energy System Planning in Developing Countries: Facilitating Load Profile Generation in Energy System Simulations](https://hdl.handle.net/10125/102726), 
Proceedings of the Hawaii International Conference on System Sciences (HICSS), Maui 2023

The coding was done by [Sarah Eckhoff](https://www.iwi.uni-hannover.de/de/eckhoff).

# Run a local version on Windows or Mac for the first time:
Start with these steps to get a local version of the application running on your device.
First, install [Docker Desktop](https://www.docker.com/products/docker-desktop) and start the Docker App.

First, you have to make two temporary changes to the code to enable the correct database setup: Open ramp_standalone_app/ramp_app/main/models.py in your preferred IDE.
Comment rows 11 and 12 and uncomment row 14. Make sure that the uncommented row is indented correctly! Save your changes.

Create an environment variable file called ".env" in the folder "ramp_standalone_app" and set the following variables:

    DB_ADMIN=ramp_app_admin
    DB_PASSWORD=some_password
    SECRET_KEY=some_secret_key

Open a terminal, for example in your IDE (Pycharm, VS Code etc.). Navigate to the folder "ramp_standalone app" and run the following command:

    docker-compose up --build -d

Troubleshooting: If an error occurs that a port is already taken, try deleting the example containers Docker has set up upon installment.

The command builds the necessary docker containers. The RAMP GUI consists of three containers. 
Nginx: Reverse proxy for server security that processes https requests and forwards them to the django application
Django: Houses the web app and RAMP, where the simulation happens.
Postgres: Houses a PostgreSQL 13 database.

After the build was successful, run these next commands in the terminal of the django container there.
Set up the database with:

    python manage.py migrate

Create yourself a superuser account to access the admin area with:

    python manage.py createsuperuser
    
After the migrations were applied successfully, you now need to undo the changes you made in models.py.
So, uncomment rows 11 and 12 and comment row 14 again.

Your local RAMP GUI version is now running! 
To view it, open a browser of your choice and type "localhost", nothing else.


# Run a local version after you made changes to the code:
To see how your changes are impacting the application, you need to send your updated code to the Docker containers.
To do that, run this command in a terminal (for example of your IDE) again:

    docker-compose up --build -d


