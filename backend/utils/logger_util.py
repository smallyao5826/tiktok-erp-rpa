import logging
import sys
import os
import json

# 检查是否在Tauri环境中
is_tauri = os.environ.get('TAURI_ENV') == 'true'

def get_logger(name: str):
    """
    获取统一格式的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 确保日志级别为INFO
    logger.setLevel(logging.INFO)
    
    # 防止重复添加 Handler
    if not logger.handlers and not is_tauri:
        # 定义格式：时间 - 名称 - 级别 - 消息
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 输出到控制台
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

class TauriLogHandler(logging.Handler):
    """
    发送日志到Tauri前端的处理器
    """
    def __init__(self):
        super().__init__()
        # 设置日期格式
        self.datefmt = '%Y-%m-%d %H:%M:%S'
    
    def emit(self, record):
        if not is_tauri:
            return
        
        try:
            # 格式化日志记录
            log_data = {
                'timestamp': self.formatTime(record, self.datefmt),
                'level': record.levelname,
                'name': record.name,
                'message': record.getMessage()
            }
            
            # 将日志发送到stdout，Tauri会捕获并通过事件发送到前端
            print(f"__TAURI_LOG__{json.dumps(log_data)}")
            sys.stdout.flush()
        except Exception as e:
            print(f"TauriLogHandler error: {e}")

# 配置根日志记录器
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# 清除根日志记录器的所有handler，避免重复
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# 添加Tauri日志处理器到根日志记录器（只在Tauri环境中）
if is_tauri:
    tauri_handler = TauriLogHandler()
    root_logger.addHandler(tauri_handler)
else:
    # 在非Tauri环境中，添加控制台handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)