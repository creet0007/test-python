FROM python:3.9-slim

WORKDIR /app

# Copy all application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the tests
RUN pytest

# Expose port for the application
EXPOSE 8080
# Run the main application if tests pass
CMD ["python", "app.py"]