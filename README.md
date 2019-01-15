# There4U
There4u is a api app which enable thee customers to make order and resturant owners to keep track of their orders

### Requirenments
    Following requirenment need to fullfill for this app to run

#### System requirenments

> Python 2.7.12<br/>
> Postgresql 9.5<br/>
> Django 1.11<br/>


### Instructions 

#### Install PSQL

1. Download and install Postgres using 
> $ sudo apt-get install postgresql postgresql-contrib.

2. Open pg_hba.conf located in postgres installation directory, for eg. /etc/postgresql/9.5/main/pg_hba.conf, and              change the line
    local   all   all    md5/peer 
    to 
    local   all   all    trust

3. Restart postgres server using 
> $ sudo service postgresql restart 
 or
> $ sudo /etc/init.d/postgresql restart.

4. Create a new postgresql role using command 
> $ createuser --interactive -P -U postgres 
    or change password of postgres by

- Start postgres shell using command
> psql -U postgres
    Enter
> alter role postgres password '<\new password>';
    Exit (\q or Ctrl + d)

- Test new user by starting postgres shell using command 
> psql -U <\username> -W template1

#### Install Application dependencies

1. Install pip  https://pip.pypa.io/en/latest/installing.html#using-the-installer’

> sudo apt-get install python-pip

2. Install Virtual Enviromnent https://virtualenv.pypa.io/en/latest/virtualenv.html#installation

> sudo pip install virtualenv

3. Install and use virtual env wrapper http://virtualenvwrapper.readthedocs.org/en/latest/#introduction

> sudo pip install virtualenvwrapper<br/>
> export WORKON_HOME=~/Envs<br/>
> mkdir -p $WORKON_HOME<br/>
> source /usr/local/bin/virtualenvwrapper.sh<br/>
> mkvirtualenv env1<br/>
> workon env1<br/>
> deactivate<br/>
   
**We need to put statements 2 & 4 in our ~/.bashrc file**

Note :- After putting statements in .bashrc you need to use 
> $ source ~/.bashrc 
once in logged in terminal window to access set variables

1. Activate environment usign

> workon env1

2. Install other development dependencies

> sudo apt install libpq-dev python-dev

3. Install JDK (Optional Oracle JDK) 

> sudo apt-add-repository ppa:webupd8team/java<br/>
> sudo apt-get update<br/>
> sudo apt-get install oracle-java8-installer<br/>

4. Install python dependencies

> $ pip install -r requirements.txt --no-index 

#### Run Project

1. Press Ctrl + Shift + P to open Command Palette, Select Python: Create Terminal to start the terminal

2. Then run following commands 
> $ workon env1<br/>
> $ python manage.py migrate to run migrations<br/>
> $ python manage.py runserver<br/>

3. Open http://127.0.0.1:8000/ in your browser.

**Django admin can be use for login and creating new user**