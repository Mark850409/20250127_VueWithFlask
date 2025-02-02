from sqlalchemy import text
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

def execute_query(session: Session, query: str, params: Dict[str, Any] = None) -> List[Any]:
    """
    執行 SELECT 查詢
    
    Args:
        session: SQLAlchemy session
        query: SQL 查詢語句
        params: 查詢參數 (可選)
    
    Returns:
        查詢結果列表
    """
    try:
        result = session.execute(text(query), params or {})
        return result.all()
    except Exception as e:
        print(f"查詢執行錯誤: {str(e)}")
        session.rollback()
        raise

def execute_insert(session: Session, table: str, data: Dict[str, Any]) -> int:
    """
    執行 INSERT 操作
    
    Args:
        session: SQLAlchemy session
        table: 資料表名稱
        data: 要插入的資料字典
    
    Returns:
        插入的記錄 ID
    """
    try:
        columns = ', '.join(data.keys())
        values = ', '.join(f':{k}' for k in data.keys())
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        result = session.execute(text(query), data)
        session.commit()
        return result.lastrowid
    except Exception as e:
        print(f"插入執行錯誤: {str(e)}")
        session.rollback()
        raise

def execute_update(session: Session, table: str, data: Dict[str, Any], condition: str, 
                  condition_params: Dict[str, Any]) -> int:
    """
    執行 UPDATE 操作
    
    Args:
        session: SQLAlchemy session
        table: 資料表名稱
        data: 要更新的資料字典
        condition: WHERE 條件語句
        condition_params: 條件參數
    
    Returns:
        更新的記錄數量
    """
    try:
        set_clause = ', '.join(f"{k} = :{k}" for k in data.keys())
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        params = {**data, **condition_params}
        result = session.execute(text(query), params)
        session.commit()
        return result.rowcount
    except Exception as e:
        print(f"更新執行錯誤: {str(e)}")
        session.rollback()
        raise

def execute_delete(session: Session, table: str, condition: str, 
                  condition_params: Dict[str, Any]) -> int:
    """
    執行 DELETE 操作
    
    Args:
        session: SQLAlchemy session
        table: 資料表名稱
        condition: WHERE 條件語句
        condition_params: 條件參數
    
    Returns:
        刪除的記錄數量
    """
    try:
        query = f"DELETE FROM {table} WHERE {condition}"
        result = session.execute(text(query), condition_params)
        session.commit()
        return result.rowcount
    except Exception as e:
        print(f"刪除執行錯誤: {str(e)}")
        session.rollback()
        raise

def execute_batch_insert(session: Session, table: str, data_list: List[Dict[str, Any]]) -> int:
    """
    執行批量 INSERT 操作
    
    Args:
        session: SQLAlchemy session
        table: 資料表名稱
        data_list: 要插入的資料字典列表
    
    Returns:
        插入的記錄數量
    """
    try:
        if not data_list:
            return 0
            
        columns = data_list[0].keys()
        columns_str = ', '.join(columns)
        values_str = ', '.join(f'({", ".join(f":{col}_{i}" for col in columns)})' 
                             for i in range(len(data_list)))
        
        # 構建參數字典
        params = {}
        for i, data in enumerate(data_list):
            for col in columns:
                params[f"{col}_{i}"] = data[col]
        
        query = f"INSERT INTO {table} ({columns_str}) VALUES {values_str}"
        result = session.execute(text(query), params)
        session.commit()
        return len(data_list)
    except Exception as e:
        print(f"批量插入執行錯誤: {str(e)}")
        session.rollback()
        raise

def execute_transaction(session: Session, operations: List[Dict[str, Any]]) -> bool:
    """
    執行事務操作
    
    Args:
        session: SQLAlchemy session
        operations: 操作列表，每個操作是一個字典，包含 'type' 和相應的參數
    
    Returns:
        是否成功執行所有操作
    """
    try:
        for op in operations:
            op_type = op.pop('type')
            if op_type == 'insert':
                execute_insert(session, **op)
            elif op_type == 'update':
                execute_update(session, **op)
            elif op_type == 'delete':
                execute_delete(session, **op)
            elif op_type == 'batch_insert':
                execute_batch_insert(session, **op)
        
        session.commit()
        return True
    except Exception as e:
        print(f"事務執行錯誤: {str(e)}")
        session.rollback()
        raise 