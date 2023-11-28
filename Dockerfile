FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set FLASK_APP environment variable
ENV FLASK_APP=app.py

# Expose the port on which Flask will run
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]