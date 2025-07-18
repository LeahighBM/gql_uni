FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the requirements file and install Python dependencies.
RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container.
COPY . /app/

# Expose the port on which the Django development server run.
EXPOSE 8000

# Command to run the Django application.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]