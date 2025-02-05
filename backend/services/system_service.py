from typing import Optional

class SystemService:
    @staticmethod
    def get_client_ip(headers: dict, remote_addr: str) -> str:
        """獲取客戶端 IP 地址
        
        Args:
            headers (dict): 請求頭
            remote_addr (str): 遠程地址
            
        Returns:
            str: 客戶端 IP 地址
        """
        if headers.get('X-Forwarded-For'):
            return headers.get('X-Forwarded-For').split(',')[0].strip()
        return remote_addr 