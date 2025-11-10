"""统计图表接口"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.statistics import (
    StatisticsQueryRequest, StatisticsQueryResponse, StatisticsDataPoint
)
from app.services.statistics_service import StatisticsService
from app.repositories.mysql_dao import StatisticsDAO
from app.database import get_db, get_redis_client
from sqlalchemy.orm import Session
from loguru import logger

router = APIRouter(prefix="/statistics", tags=["数据统计"])

def get_statistics_service(db: Session = Depends(get_db)):
    redis_client = get_redis_client()
    dao = StatisticsDAO(db)
    return StatisticsService(dao, redis_client)

@router.post("/query", response_model=StatisticsQueryResponse, summary="查询统计数据")
async def query_statistics(
    request: StatisticsQueryRequest,
    service: StatisticsService = Depends(get_statistics_service)
):
    try:
        query_params = {
            "metric": request.metric,
            "dimensions": request.dimensions,
            "start_year": request.start_year,
            "end_year": request.end_year,
            "group_by": request.group_by,
            "limit": request.limit
        }
        
        result = service.query_statistics(query_params)
        
        return StatisticsQueryResponse(
            metric=result["metric"],
            data=[StatisticsDataPoint(**item) for item in result["data"]],
            total=result.get("total")
        )
    
    except Exception as e:
        logger.error(f"查询统计数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cache", summary="清除统计缓存")
async def clear_statistics_cache(
    metric: str = None,
    service: StatisticsService = Depends(get_statistics_service)
):
    try:
        service.clear_cache(metric)
        return {"message": "缓存清除成功"}
    
    except Exception as e:
        logger.error(f"清除缓存失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
