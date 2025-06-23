@echo off
call venv\bin\activate
uvicorn main:api --reload
