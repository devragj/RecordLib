# Start up development servers.
# this requires running `npm run watch` in one process
# and flask run in another.

from multiprocessing import Process
import subprocess

def yarn():
    subprocess.run("cd frontend && yarn start", shell=True)

def django():
    #subprocess.run("pipenv run flask run", shell=True)
    subprocess.run("cd backend && pipenv run python manage.py runserver", shell=True)

if __name__ == '__main__':
    yarn_p = Process(target=yarn)
    django_p = Process(target=django)
    yarn_p.start()
    django_p.start()
