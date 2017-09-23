# Item Catelog

Item Catalog provides a list of items within a variety of categories as well as a user registration and authentication system. Registered users have the ability to post, edit, and delete their own categories and items.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)
* A [Google Account](https://accounts.google.com/SignUp) in order to log in to the application once it is running.

### Installing

Below is a step by step series of instructions that guide you through getting a development env running.

1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/). For instruction on how to install either follow the links.

2. Clone the [item-catelog](https://github.com/zoleitschuk/item-catalog/tree/master) repository. A [Vagrantfile](vagrant/Vagrantfile) is included to configure your Vagrant VM.

3. Launch the Vagrant VM by typing `vagrant up` in the directory `item-catelog/vagrant` from the terminal.

```
Zacharys-MacBook-Pro:catalog Zach$ vagrant up
```

4. Log in to the Vagrant VM by typing `vagrant ssh` in the terminal.

```
Zacharys-MacBook-Pro:catalog Zach$ vagrant ssh
```

5. Navigate to the directory `/vagrant/catalog` in the Vagrant VM by typing `cd /vagrant/catalog` in the terminal.

```
vagrant@vagrant:~$ cd /vagrant/catalog
```

6. Start the application by typing `python3 application.py` in the directory `/vagrant/catalog` of the Vagrant VM in the terminal.

```
vagrant@vagrant:/vagrant/catalog$ python3 application.py
```

7. In your browser go to [http://localhost:8000](http://localhost:8000) to view the application. In order to log in to the application you will need a google account.

To exit the application, simply type `CTRL+C`  in the terminal running `application.py`. You can then log out and shut down the Vagrant VM by typing `exit` into the terminal, then typing `vagrant halt`.

```
vagrant@vagrant:/vagrant/catalog$ python3 application.py
 * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 925-200-313
^Cvagrant@vagrant:/vagrant/catalog$ exit
logout
Connection to 127.0.0.1 closed.
Zacharys-MacBook-Pro:catalog Zach$ vagrant halt
==> default: Attempting graceful shutdown of VM...
Zacharys-MacBook-Pro:catalog Zach$ 
```

## Built With

* [Flask](http://flask.pocoo.org/) - Framework for Python
* [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper
* [Google OAuth](https://developers.google.com/identity/protocols/OAuth2) - Authentication
* [Python 3.x](https://www.python.org/) - Language

## Authors

* **Zachary Oleitschuk** - [zoleitschuk](https://github.com/zoleitschuk/)

## Thanks

This project was created in as part of required course work for the [Udacity Full-Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). I used the code in the [udacity/OAuth2.0 repo](https://github.com/udacity/OAuth2.0) to guide my work in completing the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
