from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from models.scraper import ScrapeData
from scraper.extract import ScrapeWebsite

scraper_router = APIRouter(prefix="/scraper")


@scraper_router.get("/get-scrape-data")
async def get_scrape_data(_: Request, link: str):

    try:
        scraper = ScrapeWebsite(link)
        scrape_data = scraper.return_article()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Could not scrape data due to timeout: {e}"
        )

    scrape_data = ScrapeData(content=scrape_data)
    return jsonable_encoder(scrape_data)
