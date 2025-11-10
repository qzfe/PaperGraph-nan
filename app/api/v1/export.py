"""数据导出接口"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.schemas.export import (
    ExportRequest, ExportJobResponse, ExportStatusResponse
)
from app.services.export_service import ExportService
from app.repositories.mysql_dao import ExportDAO
from app.database import get_db
from sqlalchemy.orm import Session
from loguru import logger
import os

router = APIRouter(prefix="/export", tags=["数据导出"])

def get_export_service(db: Session = Depends(get_db)):
    dao = ExportDAO(db)
    return ExportService(dao)

@router.post("/file", response_model=ExportJobResponse, summary="创建导出任务")
async def create_export_job(
    request: ExportRequest,
    background_tasks: BackgroundTasks,
    service: ExportService = Depends(get_export_service)
):
    try:
        export_params = {
            "export_type": request.export_type,
            "format": request.format,
            "filters": request.filters,
            "fields": request.fields
        }
        
        result = service.create_job(user_id=None, export_params=export_params)
        
        return ExportJobResponse(**result)
    
    except Exception as e:
        logger.error(f"创建导出任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/job/{job_id}", response_model=ExportStatusResponse, summary="查询导出状态")
async def get_export_status(
    job_id: str,
    service: ExportService = Depends(get_export_service)
):
    try:
        status = service.get_status(job_id)
        
        if status is None:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return ExportStatusResponse(**status)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询导出状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{job_id}", summary="下载导出文件")
async def download_export_file(
    job_id: str,
    service: ExportService = Depends(get_export_service)
):
    try:
        status = service.get_status(job_id)
        
        if status is None:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        if status["status"] != "done":
            raise HTTPException(status_code=400, detail="文件尚未生成")
        
        file_path = status["file_path"]
        
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        filename = os.path.basename(file_path)
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下载文件失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
