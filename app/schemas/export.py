"""导出相关 Schema"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ExportRequest(BaseModel):
    export_type: str = Field(..., description="导出类型")
    format: str = Field("csv", description="导出格式")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="筛选条件")
    fields: Optional[list] = Field(None, description="导出字段列表")

class ExportJobResponse(BaseModel):
    job_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    message: str = Field(..., description="消息")

class ExportStatusResponse(BaseModel):
    job_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    progress: Optional[float] = Field(None, description="进度")
    file_path: Optional[str] = Field(None, description="文件路径")
    download_url: Optional[str] = Field(None, description="下载链接")
    error_msg: Optional[str] = Field(None, description="错误信息")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
