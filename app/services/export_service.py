"""导出业务逻辑"""
from typing import Dict, Any, Optional
from app.repositories.mysql_dao import ExportDAO
import uuid
from loguru import logger

class ExportService:
    def __init__(self, dao: ExportDAO):
        self.dao = dao
    
    def create_job(self, user_id: Optional[int], export_params: Dict[str, Any]) -> Dict[str, Any]:
        job_id = f"exp_{uuid.uuid4().hex[:12]}"
        
        try:
            success = self.dao.insert_job(job_id, user_id, export_params)
            
            if success:
                return {
                    "job_id": job_id,
                    "status": "pending",
                    "message": "导出任务已创建"
                }
            else:
                raise Exception("创建导出任务失败")
        
        except Exception as e:
            logger.error(f"创建导出任务失败: {e}")
            raise
    
    def get_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        try:
            status = self.dao.query_status(job_id)
            
            if status:
                if status["status"] == "done" and status["file_path"]:
                    status["download_url"] = f"/api/v1/export/download/{job_id}"
                
                return status
            
            return None
        
        except Exception as e:
            logger.error(f"查询任务状态失败: {e}")
            raise
    
    def update_status(self, job_id: str, status: str, file_path: Optional[str] = None, error_msg: Optional[str] = None) -> bool:
        try:
            return self.dao.update_status(job_id, status, file_path, error_msg)
        except Exception as e:
            logger.error(f"更新任务状态失败: {e}")
            return False

