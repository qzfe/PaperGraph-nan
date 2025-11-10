"""图谱展示接口"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.schemas.graph import (
    GraphResponse, NodeDetailResponse,
    LayoutPersistRequest, LayoutPersistResponse,
    NodeSchema, EdgeSchema
)
from app.services.graph_service import GraphService
from app.repositories.neo4j_dao import GraphDAO
from app.database import get_neo4j_session, get_redis_client
from loguru import logger

router = APIRouter(prefix="/graph", tags=["图谱展示"])

def get_graph_service():
    neo4j_session = next(get_neo4j_session())
    redis_client = get_redis_client()
    dao = GraphDAO(neo4j_session)
    return GraphService(dao, redis_client)

@router.get("/root", response_model=GraphResponse, summary="获取根节点图谱")
async def get_root_graph(
    limit: int = Query(100, ge=1, le=1000, description="返回节点数量限制"),
    service: GraphService = Depends(get_graph_service)
):
    try:
        params = {"limit": limit}
        result = service.get_root(params)
        
        return GraphResponse(
            nodes=[NodeSchema(**node) for node in result["nodes"]],
            edges=[EdgeSchema(**edge) for edge in result["edges"]]
        )
    
    except Exception as e:
        logger.error(f"获取根节点图谱失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/children/{node_id}", response_model=GraphResponse, summary="展开/折叠节点")
async def get_node_children(
    node_id: str,
    service: GraphService = Depends(get_graph_service)
):
    try:
        result = service.get_children(node_id)
        
        return GraphResponse(
            nodes=[NodeSchema(**node) for node in result["nodes"]],
            edges=[EdgeSchema(**edge) for edge in result["edges"]]
        )
    
    except Exception as e:
        logger.error(f"获取节点子节点失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/node/{node_id}", response_model=NodeDetailResponse, summary="查看节点详情")
async def get_node_detail(
    node_id: str,
    service: GraphService = Depends(get_graph_service)
):
    try:
        node_info = service.get_node_info(node_id)
        
        if node_info is None:
            raise HTTPException(status_code=404, detail="节点不存在")
        
        return NodeDetailResponse(**node_info)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取节点详情失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/layout/persist", response_model=LayoutPersistResponse, summary="保存节点布局")
async def persist_layout(
    request: LayoutPersistRequest,
    service: GraphService = Depends(get_graph_service)
):
    try:
        layout_data = [
            {"node_id": pos.node_id, "x": pos.x, "y": pos.y}
            for pos in request.positions
        ]
        
        success = service.persist_layout(layout_data)
        
        if success:
            return LayoutPersistResponse(success=True, message="布局保存成功")
        else:
            return LayoutPersistResponse(success=False, message="布局保存失败")
    
    except Exception as e:
        logger.error(f"保存布局失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
