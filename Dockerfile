FROM selenium/standalone-chrome:106.0 as build

# isntalling `xvfb` is required for headfull Chrome; it's the virtual screen
RUN sudo apt update && sudo apt install -y python3-pip xvfb && sudo apt upgrade -y

# this line is just for Python
ENV PYTHONUNBUFFERED=1

# required for headfull Chrome
ENV DISPLAY=:0

# these lines are just for Python
WORKDIR /home/seluser
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./main.py .

# chromedriver is required for selenium
COPY ./lib/chromedriver/Linux/106/chromedriver ./lib/chromedriver/Linux/106/chromedriver

# now, replace `python3 main.py` with the command invocation that will employ headfull Chrome
CMD xvfb-run --server-args="-screen 0 1900x1200x24" python3 main.py
