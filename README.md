sudo systemctl start nlpguide
sudo systemctl enable nlpguide
sudo systemctl status nlpguide


sudo vi /etc/systemd/system/nlpguide


Since FastAPI is an asynchronous web framework, it is not compatible with WSGI (which is synchronous). And should Use gunicorn, this one open a socket once setup as a new
service with systemctl that is multitread, once is open I should mange the set up of nginx and guvicorn conf file to make everything works properly
