"""图谱相关 Schema"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class NodeSchema(BaseModel):
    id: str = Field(..., description="节点ID")
    label: str = Field(..., description="节点标签类型")
    properties: Dict[str, Any] = Field(default_factory=dict, description="节点属性")

class EdgeSchema(BaseModel):
    id: str = Field(..., description="边ID")
    source: str = Field(..., description="源节点ID")
    target: str = Field(..., description="目标节点ID")
    type: str = Field(..., description="关系类型")
    properties: Dict[str, Any] = Field(default_factory=dict, description="边属性")

class GraphResponse(BaseModel):
    nodes: List[NodeSchema] = Field(default_factory=list, description="节点列表")
    edges: List[EdgeSchema] = Field(default_factory=list, description="边列表")

class NodeDetailResponse(BaseModel):
    id: str = Field(..., description="节点ID")
    label: str = Field(..., description="节点类型")
    properties: Dict[str, Any] = Field(..., description="节点详细属性")

class LayoutPosition(BaseModel):
    node_id: str = Field(..., description="节点ID")
    x: float = Field(..., description="X坐标")
    y: float = Field(..., description="Y坐标")

class LayoutPersistRequest(BaseModel):
    layout_name: Optional[str] = Field(None, description="布局名称")
    positions: List[LayoutPosition] = Field(..., description="节点位置列表")

class LayoutPersistResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
