FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY ../server /app/server

# Expose the port the app runs on
EXPOSE 11434

# Command to run your application
CMD ["python", "server/scraper/LinkedIn/main.py"]