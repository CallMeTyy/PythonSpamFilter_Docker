# Make sure to start in a directory with a data folder which has a video named video.mp4 and an audio file named audio.mp4

FROM ubuntu

WORKDIR /workspace
RUN chmod -R a+w /workspace
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git
RUN apt-get install -y python3-pip
RUN git clone https://github.com/CallMeTyy/PythonSpamFilter.git

RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install Flask

ADD data /workspace
#ADD data/data200.model /workspace

EXPOSE 5000
CMD ["python3","app.py"]
