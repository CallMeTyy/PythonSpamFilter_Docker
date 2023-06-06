# PythonSpamFilter_Docker

This repository contains a dockerfile and flask script to run the PythonSpamFilter repository in a simple to use web interface.

## Prerequisites
- Docker Desktop

## Usage - Fresh Docker
1. Clone the repository
2. Place all the training data into ./data/TrainingData
3. Open the command prompt and change the directory to where the repository was cloned to (e.g. `cd C:/git/PythonSpamFilter_Docker`)
4. Run the command `docker build -t pyspam .` and wait for it to finish
5. Run the command `docker -p 80:80 run pyspam`
6. Go to a webbrowser and go to the site [localhost](https://localhost)
7. (Optional) Train the model using the data placed into TrainingData or upload fresh data and Train the algorithm using that data.
8. Upload evaluation data using Choose Files and either run a pre-trained evaluation or evaluate using the trained model.
