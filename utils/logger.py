import logging
import os
from datetime import datetime
import sys
from dotenv import load_dotenv

def setup_logger(name):
    # .env 파일에서 로깅 설정 로드
    load_dotenv()
    enable_logging = os.getenv('ENABLE_LOGGING', 'true').lower() == 'true'
    enable_console_logging = os.getenv('ENABLE_CONSOLE_LOGGING', 'true').lower() == 'true'
    log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
    
    # 로거 설정
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # 이전 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    if enable_logging:
        # 파일 로깅 설정
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # 로그 핸들러 설정 (UTF-8 인코딩)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(file_handler)
    
    if enable_console_logging:
        # 콘솔 출력 핸들러 추가
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(console_handler)
    
    return logger 