#start with a Python 3.x container
FROM python:3

#grab repository from github
RUN git clone --recursive https://github.com/tobi-wan-kenobi/bumblebee-status.git /var/bumblebee-status
#run the statusline with no modules or themes specified
CMD python3 /var/bumblebee-status/bumblebee-status
