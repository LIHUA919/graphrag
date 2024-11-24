import openai
import faiss
import numpy as np

# 设置 OpenAI API Key
openai.api_key = "your_openai_api_key"

# 示例知识库（文档）
documents = [
    "RAG 是一种结合了检索和生成的 AI 模型架构。",
    "检索器用于从知识库中提取相关信息。",
    "生成器利用上下文生成自然语言回答。",
    "OpenAI 的 GPT 是一个强大的生成器。",
    "向量数据库（如 FAISS）被广泛用于高效检索。",
]

# 创建知识库向量化
def build_vector_store(documents):
    """
    构建向量存储，使用 OpenAI Embeddings 将文档转为向量。
    """
    # 使用 OpenAI 的 Embedding 模型
    embeddings = [
        openai.Embedding.create(input=doc, model="text-embedding-ada-002")["data"][0]["embedding"]
        for doc in documents
    ]
    # 转换为 NumPy 数组
    embeddings = np.array(embeddings).astype("float32")
    
    # 使用 FAISS 构建向量索引
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    
    return index, embeddings

# 检索最相关的文档
def retrieve_top_k(query, index, documents, k=2):
    """
    从知识库中检索与查询最相关的 k 个文档。
    """
    query_embedding = np.array(
        openai.Embedding.create(input=query, model="text-embedding-ada-002")["data"][0]["embedding"]
    ).astype("float32")
    distances, indices = index.search(np.array([query_embedding]), k)
    return [documents[i] for i in indices[0]]

# 生成回答
def generate_answer(query, retrieved_docs):
    """
    利用 GPT 模型生成回答。
    """
    context = "\n".join(retrieved_docs)
    prompt = f"以下是一些相关的上下文信息：\n{context}\n\n基于这些信息，请回答以下问题：\n{query}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
    )
    return response["choices"][0]["text"].strip()

# 主流程
if __name__ == "__main__":
    # 构建向量存储
    print("构建向量存储中...")
    index, _ = build_vector_store(documents)

    # 输入用户查询
    query = input("请输入您的问题： ")

    # 检索相关文档
    print("检索相关信息...")
    top_docs = retrieve_top_k(query, index, documents)

    # 生成回答
    print("生成回答中...")
    answer = generate_answer(query, top_docs)

    print("\n==== 回答 ====")
    print(answer)









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



import subprocess

def run_program(command):
    """
    运行一个命令并检查是否成功执行。

    Args:
        command (str): 要执行的命令。

    Returns:
        bool: 如果执行成功返回 True，否则返回 False。
    """
    try:
        # 使用 subprocess 执行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # 输出命令执行的结果
        print("Command Output:")
        print(result.stdout)
        
        # 检查执行状态码
        if result.returncode == 0:
            print("Program executed successfully.")
            return True
        else:
            print("Program execution failed.")
            print("Error Output:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    # 要检查的命令
    command = input("Enter the command to execute: ")
    
    # 检查程序是否执行成功
    if run_program(command):
        print("The program ran without errors.")
    else:
        print("The program encountered an error.")
