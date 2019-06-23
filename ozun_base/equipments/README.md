find . -name "*.pyc" -exec rm -f {} \;

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete 


manage.py collectstatic --noinput --clear

