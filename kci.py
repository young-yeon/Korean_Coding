from Interpreter import interpreter
from sys import argv
import os

if __name__ == "__main__":
    argc = len(argv)

    if argc < 2:
        message = \
    """
    국어코딩 사용법
    ===========================
    python kci.py [실행 할 파일명.kc]
    """
        print(message)
        exit(0)
    
    file_name = argv[1]
    interpreter(file_name)

