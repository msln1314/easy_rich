import pytest
import json
import math
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 添加一个自定义的JSON编码器来处理特殊浮点值
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            if math.isnan(obj):
                return None
            if math.isinf(obj):
                return None if obj < 0 else float(1e308)  # 使用一个非常大的数代替无穷大
        return super().default(obj)

# 添加一个辅助函数来检查响应数据是否可以序列化为JSON
def check_json_serializable(data):
    try:
        json.dumps(data, cls=CustomJSONEncoder)
        return True
    except Exception as e:
        print(f"JSON序列化错误: {e}")
        return False

def test_get_concept_boards():
    """测试获取概念板块列表接口"""
    response = client.get("/api/v1/sector/concept")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "code" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]

def test_get_concept_board():
    """测试获取单个概念板块接口"""
    # 先获取一个有效的板块代码
    response = client.get("/api/v1/sector/concept")
    assert response.status_code == 200
    data = response.json()
    board_code = data[0]["code"]
    
    # 测试获取单个板块
    response = client.get(f"/api/v1/sector/concept/{board_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == board_code
    assert "name" in data
    assert "price" in data

def test_get_concept_board_spot():
    """测试获取概念板块实时行情详情（通过名称）接口"""
    # 使用一个常见的概念板块名称
    board_name = "可燃冰"
    # 更新为新的路由路径
    response = client.get(f"/api/v1/sector/concept/by-name/spot?name={board_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == board_name
    assert "price" in data
    assert "change_percent" in data

def test_get_concept_board_spot_by_code():
    """测试获取概念板块实时行情详情（通过代码）接口"""
    # 先获取一个有效的板块代码
    response = client.get("/api/v1/sector/concept")
    assert response.status_code == 200
    data = response.json()
    board_code = data[0]["code"]
    
    # 测试获取单个板块实时行情
    response = client.get(f"/api/v1/sector/concept/{board_code}/spot")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "price" in data
    assert "change_percent" in data

def test_get_concept_board_constituents():
    """测试获取概念板块成份股接口"""
    # 使用一个常见的概念板块名称
    board_name = "融资融券"
    # 更新为新的路由路径
    response = client.get(f"/api/v1/sector/concept/by-symbol/constituents?symbol={board_name}")
    assert response.status_code == 200
    data = response.json()
    
    # 确保数据可以序列化为JSON
    assert check_json_serializable(data)
    
    assert len(data) > 0
    assert "code" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]

def test_get_concept_board_constituents_by_code():
    """测试通过板块代码获取概念板块成份股接口"""
    # 先获取一个有效的板块代码
    response = client.get("/api/v1/sector/concept")
    assert response.status_code == 200
    data = response.json()
    board_code = data[0]["code"]
    
    # 测试获取板块成份股
    response = client.get(f"/api/v1/sector/concept/{board_code}/constituents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "code" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]

def test_get_concept_board_info():
    """测试获取概念板块基本信息接口"""
    # 使用一个常见的概念板块名称
    board_name = "可燃冰"
    # 测试新增的接口
    response = client.get(f"/api/v1/sector/concept/by-params/info?name={board_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == board_name
    assert "code" in data
    assert "price" in data

def test_get_industry_boards():
    """测试获取行业板块列表接口"""
    response = client.get("/api/v1/sector/industry")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "code" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]

def test_get_industry_board():
    """测试获取单个行业板块接口"""
    # 先获取一个有效的板块代码
    response = client.get("/api/v1/sector/industry")
    assert response.status_code == 200
    data = response.json()
    board_code = data[0]["code"]
    
    # 测试获取单个板块
    response = client.get(f"/api/v1/sector/industry/{board_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == board_code
    assert "name" in data
    assert "price" in data

def test_get_industry_board_spot():
    """测试获取行业板块实时行情详情（通过名称）接口"""
    # 使用一个常见的行业板块名称
    board_name = "小金属"
    # 更新为新的路由路径
    response = client.get(f"/api/v1/sector/industry/by-name/spot?board_name={board_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == board_name
    assert "price" in data
    assert "change_percent" in data

def test_get_industry_board_spot_by_code():
    """测试获取行业板块实时行情详情（通过代码）接口"""
    # 先获取一个有效的板块代码
    response = client.get("/api/v1/sector/industry")
    assert response.status_code == 200
    data = response.json()
    board_code = data[0]["code"]
    
    # 测试获取单个板块实时行情
    response = client.get(f"/api/v1/sector/industry/{board_code}/spot")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "price" in data
    assert "change_percent" in data

def test_get_industry_board_constituents():
    """测试获取行业板块成份股接口"""
    # 使用一个常见的行业板块名称
    board_name = "小金属"
    # 更新为新的路由路径
    response = client.get(f"/api/v1/sector/industry/by-symbol/constituents?symbol={board_name}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "code" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]

def test_get_industry_board_constituents_by_code():
    """测试通过板块代码获取行业板块成份股接口"""
    # 先获取一个有效的板块代码
    response = client.get("/api/v1/sector/industry")
    assert response.status_code == 200
    data = response.json()
    board_code = data[0]["code"]
    
    # 测试获取板块成份股
    response = client.get(f"/api/v1/sector/industry/{board_code}/constituents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "code" in data[0]
    assert "name" in data[0]
    assert "price" in data[0]