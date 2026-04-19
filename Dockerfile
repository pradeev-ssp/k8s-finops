# Use a tiny Python base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script and requirements
COPY finops_engine.py .
RUN pip install requests

# Run the script when the container starts
CMD ["python", "finops_engine.py"]