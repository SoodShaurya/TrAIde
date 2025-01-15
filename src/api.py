from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo.collection import Collection  # For type hinting


class API:
    def __init__(self, collection: Collection):
        self.app = FastAPI()
        self.collection = collection
        self._create_routes()

    def _create_routes(self):
        @self.app.get("/")
        async def index():
            return {"message": "Welcome!"}

        @self.app.get("/reddit/ticker/{ticker}")
        async def get_ticker(ticker: str):
            try:
                aggregation = self.collection.aggregate([
                    {'$match': {'tickers': ticker}},
                    {'$sort': {'timestamp': 1}}
                ])
                results = list(aggregation)
                if not results:
                    raise HTTPException(status_code=404, detail="No data found for the given ticker.")
                return JSONResponse(content=results)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error retrieving ticker data: {str(e)}")

        @self.app.get("/reddit/get_lb_alltime")
        async def sort_alltime_upvotes():
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

        @self.app.get("/reddit/get_lb_day")
        async def sort_daily_upvotes():
            try:
                one_day_ago = datetime.now() - timedelta(days=1)
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

    def __call__(self) -> FastAPI:
        return self.app