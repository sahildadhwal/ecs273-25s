from fastapi import FastAPI
from pydantic.functional_validators import BeforeValidator
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi.middleware.cors import CORSMiddleware

from http.client import HTTPException
import logging

# from data_scheme import StockListModel, StockModelV1, StockModelV2, StockNewsModel, tsneDataModel
# from data_scheme import StockListModel, StockModelV1, StockNewsModel, tsneDataModel
from data_scheme import StockListModel, StockModelV1, StockNewsModelList, tsneDataModel

# MongoDB connection (localhost, default port)
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.stock_sahildadhwal # please replace the database name with stock_[your name] to avoid collision at TA's side

app = FastAPI(
    title="Stock tracking API",
    summary="An aplication tracking stock prices and respective news"
)

# Enables CORS to allow frontend apps to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock_list", 
         response_model=StockListModel
    )
async def get_stock_list():
    """
    Get the list of stocks from the database
    """
    stock_name_collection = db.get_collection("stock_list")
    stock_list = await stock_name_collection.find_one()
    return stock_list








logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/stocknews/", 
        # response_model=StockNewsModel
        response_model=StockNewsModelList
    )
# async def get_stock_news(stock_name: str = 'XOM') -> StockNewsModel:
async def get_stock_news(stock_name: str = 'XOM') -> StockNewsModelList:
    # to look into: do i need to remove  str = 'XOM'? (idk if that is a default value if no input, or if it will overwrite the input)
    """
    Get the list of news for a specific stock from the database
    The news is sorted by date in ascending order
    """
    stock_news_collection = db.get_collection("stock_news")
    # stock_list = await stock_name_collection.find_one()
    stock_news = await stock_news_collection.find_one({"Stock" : stock_name})

    if not stock_news:
        logger.warning(f"No news found for stock: {stock_name}")
        # raise HTTPException(status_code=404, detail=f"No news found for stock: {stock_name}")


    # return [] # replace with your code to get the news from the database
    # return stock_news["News"]
    # return {"news": stock_news["News"]}
    return {"Stock": stock_name, "News": stock_news["News"]}






# @app.get("/stock/{stock_name}", 
#         response_model=StockModelV2
#     )
# async def get_stock() -> StockModelV2:
#     """
#     Get the stock data for a specific stock
#     Parameters:
#     - stock_name: The name of the stock
#     """
#     return [] # replace with your code to get the news from the database

@app.get("/stock/{stock_name}", 
        response_model=StockModelV1
    )
# async def get_stock() -> StockModelV1:
async def get_stock(stock_name: str = 'XOM') -> StockModelV1:
    """
    Get the stock data for a specific stock
    Parameters:
    - stock_name: The name of the stock
    """
    stock_data_collection = db.get_collection("stock_data")
    stock_data = await stock_data_collection.find_one({"name" : stock_name})
    
    # return [] # replace with your code to get the news from the database
    return stock_data  # 

@app.get("/tsne/",
        response_model=tsneDataModel
    )
async def get_tsne(stock_name: str = 'XOM') -> tsneDataModel:
    """
    Get the t-SNE data for a specific stock
    """
    tsne_collection = db.get_collection("tsne_data")
    
    tsne_data = await tsne_collection.find_one({"Stock" : stock_name})
    
    # return [] # replace with your code to get the news from the database
    return tsne_data  