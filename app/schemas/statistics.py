"""统计相关 Schema"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class StatisticsQueryRequest(BaseModel):
    metric: str = Field(..., description="指标名称")
    dimensions: Optional[Dict[str, Any]] = Field(default_factory=dict, description="聚合维度")
    start_year: Optional[int] = Field(None, description="起始年份")
    end_year: Optional[int] = Field(None, description="结束年份")
    group_by: Optional[str] = Field(None, description="分组字段")
    limit: Optional[int] = Field(100, description="返回结果数量限制")

class StatisticsDataPoint(BaseModel):
    label: str = Field(..., description="数据标签")
    value: float = Field(..., description="数据值")
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict, description="额外信息")

class StatisticsQueryResponse(BaseModel):
    metric: str = Field(..., description="指标名称")
    data: List[StatisticsDataPoint] = Field(..., description="统计数据")
    total: Optional[int] = Field(None, description="总数")
    updated_at: Optional[datetime] = Field(None, description="数据更新时间")
