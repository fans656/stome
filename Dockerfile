FROM python:stretch
WORKDIR /backend
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install aiofiles
RUN pip install jwt
COPY ./backend /backend
COPY ./frontend/out /frontend/out
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "app:app"]
