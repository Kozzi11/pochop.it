# pochop.it
Webove stranky spolku pochopit

## instalace
1. instalce pycharm (profession edition)
2. pokud v pycharm vybereme ze chceme zalozit django projekt tak by se mel naistalovat jak python tak django
3. pokud v kroku dva nedoslo k naistalovani pythonu nebo djanga tak je naistalujeme rucne
  * instalace python 3.x - https://www.python.org/downloads/
  * instalace pip: https://pip.pypa.io/en/latest/installing/#install-pip
  * `pip install Django` - u linuxu je mozne ze budete potrebovat prikaz spustit jako `sudo`
4. `pip install django-bootstrap3` - u linuxu je mozne ze budete potrebovat prikaz spustit jako `sudo`
5. `pip install django-eztables` - u linuxu je mozne ze budete potrebovat prikaz spustit jako `sudo`
6. `pip install django-tinymce`
7. pull projektu z [githubu](https://github.com/Kozzi11/pochop.it) 
8. v jiz pulnutem projektu spustit v terminalu:
  * `cp pochopit/settings.py.example pochopit/settings.py`
  * `python manage.py makemigrations`
  * `python manage.py migrate`
9. vytvoreni super usera
  * `python manage.py createsuperuser`
10. Na widlich je potreba jeste naistalovat getttext [navod](https://docs.djangoproject.com/en/1.7/topics/i18n/translation/#gettext-on-windows)
11. spusteni severu bud pres **pycharm** nebo rucne: `manage.py runserver`
  * mozno predat *ip* a *port* viz : `runserver [port or address:port]`
