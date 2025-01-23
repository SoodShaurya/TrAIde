# src/api.py
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

class API:
    def __init__(self, collection: Collection):
        self.app = FastAPI()
        self.collection = collection
        self._create_routes()

    def get_ticker(self, ticker: str, sort: str, direction: int):
        try:
            if direction not in [1, -1]:
                raise HTTPException(status_code=400, detail="Direction must be either 1 (ascending) or -1 (descending).")
            aggregation = self.collection.aggregate([
                {'$match': {'tickers': ticker.upper()}},
                {'$sort': {sort: direction}}
            ])
            results = list(aggregation)
            if not results:
                raise HTTPException(status_code=404, detail="No data found for the given ticker.")
            return JSONResponse(content=results)
        except PyMongoError as db_error:
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving ticker data: {str(e)}")
        
    def match(self, match: str, key: str):
        try:
            aggregation = self.collection.aggregate([
                {'$match': {match: key}},
            ])
            results = list(aggregation)
            if not results:
                raise HTTPException(status_code=404, detail="No data found for the given key.")
            return JSONResponse(content=results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving ticker data: {str(e)}")
        
    def sort_alltime_upvotes(self):
        try:
            aggregation = self.collection.aggregate([
                {'$group': {'_id': '$tickers', 'total_upvotes': {'$sum': '$upvotes'}}},
                {'$sort': {'total_upvotes': -1}}
            ])
            items = [item for item in aggregation if len(item['_id']) == 1]
            if not items:
                raise HTTPException(status_code=404, detail="No data available.")
            return JSONResponse(content=items)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error sorting upvotes: {str(e)}")
        
    def sort_daily_upvotes(self):
        try:
            one_day_ago = datetime.timestamp(datetime.now() - timedelta(days=1))
            aggregation = self.collection.aggregate([
                {'$match': {'timestamp': {'$gte': one_day_ago}}},
                {'$group': {'_id': '$tickers', 'total_upvotes': {'$sum': '$upvotes'}}},
                {'$sort': {'total_upvotes': -1}}
            ])
            items = [item for item in aggregation if len(item['_id']) == 1]
            if not items:
                raise HTTPException(status_code=404, detail="No data available for the last 24 hours.")
            return JSONResponse(content=items)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error sorting daily upvotes: {str(e)}")

    def _create_routes(self):
        router = APIRouter(prefix="/api/v1")
        
        @router.get("/")
        async def index():
            return {"message": "Welcome!"}

        @router.get("/reddit/ticker/{ticker}/{sort}/{direction}")
        async def get_ticker_route(ticker: str, sort: str, direction: int):
            return self.get_ticker(ticker, sort, direction)
        
        @router.get("/reddit/match/{match}/{key}")
        async def match_route(match: str, key: str):
            return self.match(match, key)

        @router.get("/reddit/get_lb_alltime")
        async def sort_alltime_upvotes_route():
            return self.sort_alltime_upvotes()

        @router.get("/reddit/get_lb_day")
        async def sort_daily_upvotes_route():
            return self.sort_daily_upvotes()

        self.app.include_router(router)

    def __call__(self) -> FastAPI:
        return self.app