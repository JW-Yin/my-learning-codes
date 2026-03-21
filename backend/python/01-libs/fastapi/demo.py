from fastapi import FastAPI
from pydantic import BaseModel

# 1. 创建 FastAPI 应用实例
app = FastAPI(title="最小 FastAPI 实战")

# 2. 定义请求体模型（POST 用）
class AddDataRequest(BaseModel):
    name: str
    age: int = 18  # 默认值 18

# 3. 定义响应模型
class AddDataResponse(BaseModel):
    success: bool
    message: str
    data_id: int

# 4. GET 请求：根路径
@app.get("/")
def root():
    return {"message": "欢迎来到最小 FastAPI 实战！", "docs": "/docs"}

# 5. GET 请求：路径参数 + 查询参数
@app.get("/user/{user_id}")
def get_user(user_id: int, keyword: str = ""):
    return {"user_id": user_id, "keyword": keyword, "name": "用户{}".format(user_id)}

# 6. POST 请求：请求体 + 响应模型
@app.post("/add_data", response_model=AddDataResponse)
def add_data(request: AddDataRequest):
    return {
        "success": True,
        "message": "数据新增成功",
        "data_id": 1001  # 假设生成的 ID 是 1001
    }
