# Whatsapp Web Bot 

Send messages from a Google Sheets to whatsapp.

## Sheet format

| column  | content                                                                  |
|---------|--------------------------------------------------------------------------|
| First   | Don't mind.                                                              |
| Second  | Don't mind.                                                              |
| Third   | Number to send the message                                               |
| Fourth  | Approbation boolean (1: approved, other: not approved)                   |
| Fifth   | Message sended verification (1: send, other: not send)                   |
| Sixth   | Date first message was sended (yyyy-mm-dd)                               |
| Seventh | Customer response (1: response confirmation, other: no response)         |
| Eight   | Whatsapp number existence (1: number exists, other: number don't exists) |

## Empty Folders

> The folders "images", "qr_codes", "keys" and "temp" are empty because this data is not public.

## How to use it on Docker

~~~bash
docker-compose up -d --build
~~~

> To see the FastAPI interface, go to http://localhost:8000/docs
> 
> To see the selenium interface, go to http://localhost:4444/ui#

## How to use it on local

~~~bash
# On a virtual environment
pip install poetry
~~~

~~~bash
poetry install
~~~

## Some useful poetry commands to manage dependencies

- Update all required packages

    ```bash
    poetry update
    ```
  
- Delete a required package

    ```bash
    poetry remove package_name
    ```

- Add a required package. See [How to write version constrains](https://python-poetry.org/docs/dependency-specification/)

    ```bash
    poetry add package_name="version"
    ```

- Synchronize poetry lock and requirements.txt

    ~~~bash
    poetry export -f requirements.txt --output requirements.txt --without-hashes
    ~~~
