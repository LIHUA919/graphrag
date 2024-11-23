import os
import sys
import logging
from importlib import import_module

# 设置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def check_python_version(required_version=(3, 8)):
    """
    检查 Python 版本是否符合项目要求
    """
    logging.info("Checking Python version...")
    if sys.version_info < required_version:
        logging.error(f"Python {required_version} or higher is required. Current version: {sys.version}")
        sys.exit(1)
    logging.info(f"Python version is OK: {sys.version}")

def check_dependencies(requirements_file="requirements.txt"):
    """
    检查依赖是否安装
    """
    logging.info("Checking dependencies...")
    try:
        with open(requirements_file, "r") as f:
            dependencies = f.readlines()
        for dep in dependencies:
            dep_name = dep.strip().split("==")[0]  # 获取包名
            try:
                import_module(dep_name)
                logging.info(f"Dependency OK: {dep_name}")
            except ImportError:
                logging.error(f"Missing dependency: {dep_name}. Install it using 'pip install {dep_name}'")
    except FileNotFoundError:
        logging.error(f"Requirements file not found: {requirements_file}")

def debug_project_structure(project_path="."):
    """
    检查项目结构是否完整
    """
    logging.info(f"Checking project structure in: {project_path}")
    required_files = ["main.py", "config.py", "README.md"]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(project_path, f))]
    
    if missing_files:
        logging.error(f"Missing required files: {', '.join(missing_files)}")
    else:
        logging.info("Project structure is OK")

def main():
    """
    主函数：依次运行调试任务
    """
    logging.info("Starting graphrag debugging script...")
    check_python_version()  # 检查 Python 版本
    check_dependencies()  # 检查依赖
    debug_project_structure()  # 检查项目结构
    logging.info("Debugging completed.")

if __name__ == "__main__":
    main()
