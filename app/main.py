import os
import pprint

import uvicorn
from dotenv import load_dotenv

from fastapi import BackgroundTasks, FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from maps_bot.bot import MapsBot
from maps_bot.schema import Lead
from wpp_bot.bot import WppBot

load_dotenv('../docker/fastapi/.env')


app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

def send_message_to_whatsapp_task(spreadsheet: str, sheet: str, text: str, path: str):
    with open("log_wpp.txt", mode="w") as file:
        spreadsheet = "MarkeBot"
        sheet = "Hoja_de_pruebas"
        text = "Hola, soy un bot"
        path = "private_files/images/growth.jpg"

        wpp_bot = WppBot(spreadsheet, sheet)
        history = wpp_bot.send_messages_to_sheet_numbers(sheet, text, path)
        pprint.pprint(history, stream=file)
        print("process finished")

def google_maps_search_task(search_text: str):
    with open("log_maps.txt", mode="w") as file:
        maps_bot = MapsBot()
        results = maps_bot.search(search_text)
        pprint.pprint(results, stream=file)
        db_lead = Lead(
            name=results["name"],
            score=results["score"],
            number_of_opinions=results["number_of_opinions"],
            phone_number=results["phone_number"],
            website=results["website"],
            email=results["email"],
            country_scraped="Colombia"
        )
        db.session.add(db_lead)
        db.session.commit()
        print("process finished")

@app.get("/fastapi/send_messages/")
async def send_messages(spreadsheet: str, sheet: str, text: str, path: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message_to_whatsapp_task, spreadsheet, sheet, text, path)
    return {"message": "Search started! The results will be found in the log_wpp.txt file."}

@app.get("/maps_bot/search/")
async def search(search_text: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(google_maps_search_task, search_text=search_text)
    return {"message": "Search started! The results will be found in the log_maps.txt file."}


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
