# PythonSpamFilter_Docker

This repository contains a dockerfile and flask script to run the PythonSpamFilter repository in a simple to use web interface.

## Prerequisites
- Docker Desktop
- Training Data (Corpus)

## Usage - Fresh Docker
For this setup a custom image is built instead of using a pre-built one. This allows for custom large data-sets, as the interface has a file limit and attaching a local file is currently unsupported. To use the pre-built image please follow the instructions below this paragraph.
1. Open Docker Desktop
2. Clone the repository
3. Place all the training data into ./data/TrainingData (e.g. part 1 to 9 from the corpus)
4. Open the command prompt and change the directory to where the repository was cloned to (e.g. `cd C:/git/PythonSpamFilter_Docker`)
5. Run the command `docker build -t pyspam .` and wait for it to finish
6. Run the command `docker run -p 80:80 pyspam`
7. Go to a webbrowser and go to your local host [127.0.0.1](https://127.0.0.1)
8. (Optional) Train the model using the data placed into TrainingData or upload fresh data and Train the algorithm using that data.
9. Upload evaluation data using Choose Files and either run a pre-trained evaluation or evaluate using the trained model.

## Usage - Dockerhub
Please note that in the pre-built image there is already pre-entered data for training. To use your own data please use a fresh Docker.
Attaching a custom folder to support the use of a lot of custom data might be added in the future but is outside of the scope for what is aimed in this project.
For smaller amounts of custom data the web interface can be used to upload and train data.
1. Open Docker Desktop
2. Open the command prompt and run `docker pull callmety/pythonspamfilter:latest`
3. Run the docker with `docker run -p 80:80 callmety/pythonspamfilter:latest`
4. Go to your local host [127.0.0.1](https://127.0.0.1)
