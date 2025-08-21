FROM alpine
RUN apk add bmake python3 py3-requests

WORKDIR /app
CMD ["bmake", "PYTHON=python3", "json"]
