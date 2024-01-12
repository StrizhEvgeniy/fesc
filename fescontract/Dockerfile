FROM node:19.5.0-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json package-lock.json index.html vite.config.js .gitignore .eslintrc.cjs ./
COPY ./src ./src
COPY ./public ./public
RUN npm install
RUN npm run build

# Build step #2: build the API with the client as static files
FROM python:3.9
WORKDIR /app
COPY --from=build-step /app/dist/. .

RUN mkdir ./api
COPY ./api/. ./api
RUN pip install -r ./api/requirements.txt
ENV FLASK_ENV production
#RUN venv/bin/flask run --no-debugger

EXPOSE 3000
WORKDIR /app/api
CMD ["gunicorn", "-b", ":3000", "run:app"]