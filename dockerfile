FROM python:3.12.4

COPY ./apps/webshop/requirements /apps/webshop/requirements
WORKDIR /apps/webshop
RUN pip3 install -r /apps/webshop/requirements/prod.txt

COPY ./apps/webshop /apps/webshop

RUN apt update
RUN apt install -y fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatspi2.0-0 libgtk-3-0 libnspr4 libnss3 libx11-xcb1 libxtst6 xdg-utils wkhtmltopdf gettext

COPY ./docker/dev/webshop/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]