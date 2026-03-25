import logging, os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from rec_service_helper import Recommendations, SimilarItems
from dotenv import load_dotenv

logger = logging.getLogger("uvicorn.info")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("test_service.log")
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

rec_store = Recommendations()
sim_items_store = SimilarItems()

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    logger.info("Starting")
    sim_items_store.load(
        f"s3://{os.getenv('S3_BUCKET')}/recsys/recommendations/similar.parquet",
        engine="pyarrow",
        storage_options={
            "key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "client_kwargs": {
                "endpoint_url": os.getenv("S3_ENDPOINT_URL")
            }
        }
        )
    rec_store.load(
        "personal",
        f"s3://{os.getenv('S3_BUCKET')}/recsys/recommendations/recommendations.parquet",
        engine="pyarrow",
        storage_options={
            "key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "client_kwargs": {
                "endpoint_url": os.getenv("S3_ENDPOINT_URL")
            }
        }
    )

    rec_store.load(
        "default",
        f"s3://{os.getenv('S3_BUCKET')}/recsys/recommendations/top_popular.parquet",
        engine="pyarrow",
        storage_options={
            "key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "client_kwargs": {
                "endpoint_url": os.getenv("S3_ENDPOINT_URL")
            }
        }
    )
    
    logger.info("Ready!")
    yield
    rec_store.stats()
    logger.info("Stopping")

app = FastAPI(title="recommendations", lifespan=lifespan)

@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 100):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """

    recs = rec_store.get(user_id, k)

    return {"recs": recs}


@app.post("/similar_items")
async def recommendations(item_id: int, k: int = 10):
    """
    Возвращает список похожих объектов длиной k для item_id
    """
    i2i = sim_items_store.get(item_id, k)

    return i2i

@app.post("popular_items")
async def recommendations(k: int = 10):
    """
    Возвращает список популярных объектов длиной k
    """


