"""
数据库连接管理
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from neo4j import GraphDatabase
import redis
from typing import Generator
from config import settings
from loguru import logger

# SQLAlchemy Base
Base = declarative_base()

# MySQL Engine
engine = create_engine(
    settings.mysql_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Neo4j Driver
class Neo4jConnection:
    """Neo4j 连接管理"""
    
    def __init__(self):
        self._driver = None
    
    def connect(self):
        """建立连接"""
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
                logger.info("Neo4j 连接成功")
            except Exception as e:
                logger.error(f"Neo4j 连接失败: {e}")
                raise
        return self._driver
    
    def close(self):
        """关闭连接"""
        if self._driver:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j 连接已关闭")
    
    def get_session(self):
        """获取会话"""
        if self._driver is None:
            self.connect()
        return self._driver.session()


# 全局 Neo4j 连接实例
neo4j_conn = Neo4jConnection()


def get_neo4j_session():
    """获取 Neo4j 会话"""
    session = neo4j_conn.get_session()
    try:
        yield session
    finally:
        session.close()


# Redis Connection
class RedisConnection:
    """Redis 连接管理"""
    
    def __init__(self):
        self._client = None
    
    def connect(self):
        """建立连接"""
        if self._client is None:
            try:
                if settings.REDIS_PASSWORD:
                    self._client = redis.Redis(
                        host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT,
                        password=settings.REDIS_PASSWORD,
                        db=settings.REDIS_DB,
                        decode_responses=True
                    )
                else:
                    self._client = redis.Redis(
                        host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT,
                        db=settings.REDIS_DB,
                        decode_responses=True
                    )
                # 测试连接
                self._client.ping()
                logger.info("Redis 连接成功")
            except Exception as e:
                logger.error(f"Redis 连接失败: {e}")
                raise
        return self._client
    
    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("Redis 连接已关闭")
    
    def get_client(self):
        """获取 Redis 客户端"""
        if self._client is None:
            self.connect()
        return self._client


# 全局 Redis 连接实例
redis_conn = RedisConnection()


def get_redis_client():
    """获取 Redis 客户端"""
    return redis_conn.get_client()


def init_db():
    """初始化数据库"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("MySQL 表创建成功")
        
        # 测试 Neo4j 连接
        neo4j_conn.connect()
        
        # 测试 Redis 连接
        redis_conn.connect()
        
        logger.info("所有数据库连接初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


def close_db():
    """关闭所有数据库连接"""
    neo4j_conn.close()
    redis_conn.close()
    logger.info("所有数据库连接已关闭")

