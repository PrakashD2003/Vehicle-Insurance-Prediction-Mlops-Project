# ┌─────────────────────────────┐
# │ 1) Builder stage           │
# └─────────────────────────────┘
FROM python:3.11-slim AS builder

# 1.1 Install build dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1.2 Copy only things needed to build your package
COPY pyproject.toml setup.py requirements.txt ./

# 1.3 Build wheels for all deps + your package
RUN pip install --upgrade pip wheel \
 && pip wheel --no-cache-dir --wheel-dir /wheels \
      -r requirements.txt \
 && pip wheel --no-cache-dir --wheel-dir /wheels .



# ┌─────────────────────────────┐
# │ 2) Runtime stage           │
# └─────────────────────────────┘
FROM python:3.11-slim

# 2.1 Install only runtime OS deps (if any)
#    Leave out gcc, dev libs, etc.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq5 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2.2 Copy in wheels and install them
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
&& rm -rf /wheels

# Copy the project-root marker
COPY .project-root ./
# 2.3 Copy only your app’s runtime code
COPY app.py          .
COPY src/   src/
COPY static/ static/
COPY templates/ templates/

# 2.4 Expose and run
EXPOSE 5000
CMD ["python", "app.py"]
