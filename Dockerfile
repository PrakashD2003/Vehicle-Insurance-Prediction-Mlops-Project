FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# 1) Copy just the files pip needs to build/install your package:
COPY setup.py pyproject.toml requirements.txt ./

# 2) Install dependencies and then your package in editable mode:
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Copy your application code
COPY . .  

# Expose the port FastAPI will run on
EXPOSE 5000

# Command to run the FastAPI app
CMD ["python3", "app.py"]

