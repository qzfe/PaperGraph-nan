"""通用 Schema"""
from pydantic import BaseModel, Field
from typing import Optional, Any

class ResponseBase(BaseModel):
    code: int = Field(200, description="响应代码")
    message: str = Field("success", description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
