FROM openscad/openscad:latest

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

# Copy the Flask app
COPY app.py .

# Install Flask
RUN pip3 install Flask

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python3", "app.py"]