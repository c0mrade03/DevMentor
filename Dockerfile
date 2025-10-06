# Use an official lightweight Python image as the base.
FROM python:3.10-slim

# Set the working directory for subsequent commands inside the container.
WORKDIR /app

# Take arguments for requirements file based on your system cpu or gpu
ARG REQS_FILE=requirements.txt

# Copy the requirements file first to leverage Docker's layer caching.
COPY ${REQS_FILE} ./requirements.txt

# Install the Python dependencies listed in the requirements file.
RUN pip install --no-cache-dir -r requirements.txt

# Inform Docker that the container listens on the specified network port at runtime.
EXPOSE 8501

# Copy the rest of the application's source code into the container.
COPY . .

# Specify the default command to run when the container starts.
CMD ["streamlit", "run", "app.py"]
