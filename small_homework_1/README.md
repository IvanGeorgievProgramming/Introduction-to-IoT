# Introduction to IoT - Small Homework 1

## Building the Docker Image

```bash
docker build -t ivan_g.iot.small_hw_1:v1 .
```

By using the docker build command, we are building a docker image from a Dockerfile.
- The -t flag is used to give a name and a tag to the image.

## Running the Docker Container

```bash
docker run --name my_flask_app -p 5000:5000 --rm ivan_g.iot.small_hw_1:v1
```

By using the docker run command, we are running a docker container from the image we built in the previous step.
- The --name flag is used to give a name to the container.
- The -p flag is used to map the port 5000 of the container to the port 5000 of the host machine.
- The --rm flag is used to remove the container after it exits.

## Removing the Docker Image

```bash
docker image rm ivan_g.iot.small_hw_1:v1
```

- By using the docker image rm command, we are removing the image we built in the first step.

## P.S.
I wanted to make the flask application in an organized and structured way, but there was a problem with finding the mark.csv file. So, I had to put the mark.csv file in the same directory as the flask application. Can you please tell me how to fix this problem? Thank you in advance!