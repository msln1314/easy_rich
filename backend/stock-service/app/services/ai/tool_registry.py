"""
工具注册中心模块

提供工具的定义、注册、管理和执行功能，支持转换为 OpenAI Function Calling 格式。
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import inspect
import functools


@dataclass
class ToolParameter:
    """工具参数

    定义工具的参数信息，包括名称、类型、描述等。

    Attributes:
        name: 参数名称
        type: 参数类型，支持 string, number, integer, boolean, array, object
        description: 参数描述
        required: 是否必需，默认为 True
        enum: 枚举值列表，用于限制参数值范围
        default: 默认值
    """

    name: str
    type: str  # string, number, integer, boolean, array, object
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    default: Any = None

    def __post_init__(self):
        """验证参数类型"""
        valid_types = {"string", "number", "integer", "boolean", "array", "object"}
        if self.type not in valid_types:
            raise ValueError(f"无效的参数类型 '{self.type}'，必须是: {valid_types}")


@dataclass
class ToolDefinition:
    """工具定义

    定义工具的完整信息，包括名称、描述、参数和处理函数。

    Attributes:
        name: 工具名称
        description: 工具描述
        parameters: 参数列表
        handler: 工具处理函数
        category: 工具类别，支持 data, analysis, search, action
    """

    name: str
    description: str
    parameters: List[ToolParameter]
    handler: Callable
    category: str = "data"  # data, analysis, search, action

    def __post_init__(self):
        """验证工具类别"""
        valid_categories = {"data", "analysis", "search", "action"}
        if self.category not in valid_categories:
            raise ValueError(f"无效的工具类别 '{self.category}'，必须是: {valid_categories}")

    def _params_json_schema(self) -> dict:
        """生成参数 JSON Schema

        根据 ToolParameter 列表生成符合 JSON Schema 规范的参数定义。

        Returns:
            包含 type、properties 和 required 字段的字典
        """
        properties = {}
        required = []

        for param in self.parameters:
            prop = {
                "type": param.type,
                "description": param.description,
            }

            if param.enum is not None:
                prop["enum"] = param.enum

            if param.default is not None:
                prop["default"] = param.default

            properties[param.name] = prop

            if param.required:
                required.append(param.name)

        schema = {
            "type": "object",
            "properties": properties,
        }

        if required:
            schema["required"] = required

        return schema

    def to_openai_tool(self) -> dict:
        """转换为 OpenAI 工具格式

        将工具定义转换为 OpenAI Function Calling 所需的格式。

        Returns:
            符合 OpenAI 工具格式的字典
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._params_json_schema(),
            },
        }


class ToolRegistry:
    """工具注册中心

    管理工具的注册、查询和执行。提供统一的工具管理接口。

    Attributes:
        _tools: 工具名称到工具定义的映射字典
    """

    def __init__(self):
        """初始化工具注册中心"""
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool_def: ToolDefinition) -> None:
        """注册工具

        将工具定义添加到注册中心。如果同名工具已存在，将覆盖原有定义。

        Args:
            tool_def: 工具定义对象

        Raises:
            ValueError: 如果 tool_def 不是 ToolDefinition 实例
        """
        if not isinstance(tool_def, ToolDefinition):
            raise ValueError("tool_def 必须是 ToolDefinition 实例")

        self._tools[tool_def.name] = tool_def

    def unregister(self, name: str) -> None:
        """注销工具

        从注册中心移除指定名称的工具。

        Args:
            name: 工具名称

        Raises:
            KeyError: 如果工具不存在
        """
        if name not in self._tools:
            raise KeyError(f"工具 '{name}' 不存在")

        del self._tools[name]

    def get(self, name: str) -> Optional[ToolDefinition]:
        """获取工具

        根据名称获取工具定义。

        Args:
            name: 工具名称

        Returns:
            工具定义对象，如果不存在则返回 None
        """
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[ToolDefinition]:
        """列出工具

        列出所有注册的工具，可按类别筛选。

        Args:
            category: 可选的类别筛选条件

        Returns:
            工具定义列表
        """
        if category is None:
            return list(self._tools.values())

        return [tool for tool in self._tools.values() if tool.category == category]

    def list_names(self) -> List[str]:
        """列出工具名称

        返回所有已注册工具的名称列表。

        Returns:
            工具名称列表
        """
        return list(self._tools.keys())

    def execute(self, name: str, **kwargs) -> Any:
        """执行工具

        根据名称执行对应的工具处理函数。

        Args:
            name: 工具名称
            **kwargs: 传递给工具处理函数的参数

        Returns:
            工具执行结果

        Raises:
            KeyError: 如果工具不存在
            TypeError: 如果参数不匹配
            Exception: 工具执行过程中的其他异常
        """
        tool_def = self.get(name)
        if tool_def is None:
            raise KeyError(f"工具 '{name}' 不存在")

        # 验证必需参数
        missing_params = []
        for param in tool_def.parameters:
            if param.required and param.name not in kwargs:
                if param.default is None:
                    missing_params.append(param.name)

        if missing_params:
            raise TypeError(f"缺少必需参数: {missing_params}")

        # 设置默认值
        for param in tool_def.parameters:
            if param.name not in kwargs and param.default is not None:
                kwargs[param.name] = param.default

        try:
            return tool_def.handler(**kwargs)
        except Exception as e:
            raise RuntimeError(f"执行工具 '{name}' 失败: {e}") from e

    def to_openai_tools(self) -> List[dict]:
        """转换为 OpenAI 工具列表

        将所有注册的工具转换为 OpenAI Function Calling 格式的列表。

        Returns:
            OpenAI 工具格式列表
        """
        return [tool.to_openai_tool() for tool in self._tools.values()]

    def __contains__(self, name: str) -> bool:
        """检查工具是否已注册

        Args:
            name: 工具名称

        Returns:
            工具是否已注册
        """
        return name in self._tools

    def __len__(self) -> int:
        """返回已注册工具的数量

        Returns:
            工具数量
        """
        return len(self._tools)


def _infer_parameters(func: Callable) -> List[ToolParameter]:
    """从函数签名推断参数

    分析函数的签名和文档字符串，自动生成 ToolParameter 列表。

    Args:
        func: 要分析的函数

    Returns:
        推断出的 ToolParameter 列表
    """
    sig = inspect.signature(func)
    parameters = []

    # 解析文档字符串中的参数描述
    param_docs = _parse_param_docs(func.__doc__)

    for param_name, param in sig.parameters.items():
        # 跳过 self 和 cls 参数
        if param_name in ("self", "cls"):
            continue

        # 推断参数类型
        param_type = _infer_type(param.annotation, param.default)

        # 获取参数描述
        description = param_docs.get(param_name, f"参数 {param_name}")

        # 判断是否必需
        required = param.default is inspect.Parameter.empty

        # 获取默认值
        default = None if param.default is inspect.Parameter.empty else param.default

        parameters.append(
            ToolParameter(
                name=param_name,
                type=param_type,
                description=description,
                required=required,
                default=default,
            )
        )

    return parameters


def _infer_type(annotation: Any, default: Any) -> str:
    """从类型注解推断 JSON Schema 类型

    Args:
        annotation: 类型注解
        default: 默认值

    Returns:
        JSON Schema 类型字符串
    """
    # 如果有类型注解
    if annotation is not inspect.Parameter.empty:
        # 处理 Optional 类型
        origin = getattr(annotation, "__origin__", None)
        if origin is Optional:
            # 提取 Optional 内部的实际类型
            args = getattr(annotation, "__args__", ())
            if args:
                annotation = args[0]

        # 类型映射
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            List: "array",
            dict: "object",
            Dict: "object",
        }

        if annotation in type_map:
            return type_map[annotation]

        # 处理 typing 模块的泛型类型
        type_name = getattr(annotation, "__name__", str(annotation))
        if "str" in type_name.lower():
            return "string"
        elif "int" in type_name.lower():
            return "integer"
        elif "float" in type_name.lower() or "number" in type_name.lower():
            return "number"
        elif "bool" in type_name.lower():
            return "boolean"
        elif "list" in type_name.lower() or "array" in type_name.lower():
            return "array"
        elif "dict" in type_name.lower() or "map" in type_name.lower():
            return "object"

    # 根据默认值推断类型
    if default is not inspect.Parameter.empty and default is not None:
        if isinstance(default, str):
            return "string"
        elif isinstance(default, bool):
            return "boolean"
        elif isinstance(default, int):
            return "integer"
        elif isinstance(default, float):
            return "number"
        elif isinstance(default, list):
            return "array"
        elif isinstance(default, dict):
            return "object"

    # 默认返回 string 类型
    return "string"


def _parse_param_docs(docstring: Optional[str]) -> Dict[str, str]:
    """解析文档字符串中的参数描述

    支持 Google 和 NumPy 风格的文档字符串。

    Args:
        docstring: 函数的文档字符串

    Returns:
        参数名到描述的映射字典
    """
    if not docstring:
        return {}

    param_docs = {}
    lines = docstring.split("\n")
    current_param = None
    current_desc = []

    in_args_section = False

    for line in lines:
        stripped = line.strip()

        # 检测参数部分的开始
        if stripped.lower() in ("args:", "arguments:", "parameters:", "params:"):
            in_args_section = True
            continue

        # 检测其他部分，结束参数部分
        if in_args_section and stripped.endswith(":") and not stripped.startswith(" "):
            if current_param:
                param_docs[current_param] = " ".join(current_desc).strip()
                current_param = None
                current_desc = []
            break

        # 解析参数行
        if in_args_section:
            # 匹配 "param_name: description" 或 "param_name (type): description"
            if ":" in stripped:
                parts = stripped.split(":", 1)
                param_part = parts[0].strip()

                # 提取参数名（去掉可能的类型注解）
                param_name = param_part.split("(")[0].strip()

                if param_name and not param_name.startswith("Returns"):
                    # 保存上一个参数
                    if current_param:
                        param_docs[current_param] = " ".join(current_desc).strip()

                    current_param = param_name
                    current_desc = [parts[1].strip()] if len(parts) > 1 else []
            elif current_param and stripped:
                # 继续上一个参数的描述
                current_desc.append(stripped)

    # 保存最后一个参数
    if current_param:
        param_docs[current_param] = " ".join(current_desc).strip()

    return param_docs


# 全局默认注册中心实例
_default_registry: Optional[ToolRegistry] = None


def get_default_registry() -> ToolRegistry:
    """获取默认注册中心

    返回全局默认的工具注册中心实例。如果实例不存在，将创建一个新实例。

    Returns:
        默认的 ToolRegistry 实例
    """
    global _default_registry
    if _default_registry is None:
        _default_registry = ToolRegistry()
    return _default_registry


def tool(
    name: str,
    description: str,
    category: str = "data",
    parameters: Optional[List[ToolParameter]] = None,
    registry: Optional[ToolRegistry] = None,
):
    """工具装饰器

    将函数注册为工具。支持自动从函数签名推断参数。

    Args:
        name: 工具名称
        description: 工具描述
        category: 工具类别，默认为 "data"
        parameters: 参数列表，如果为 None 则自动推断
        registry: 目标注册中心，如果为 None 则使用默认注册中心

    Returns:
        装饰器函数

    Example:
        @tool(
            name="get_weather",
            description="获取指定城市的天气信息",
            category="search"
        )
        def get_weather(city: str, days: int = 1) -> dict:
            '''
            获取天气信息

            Args:
                city: 城市名称
                days: 预报天数
            '''
            # 实现代码
            pass
    """

    def decorator(func: Callable) -> Callable:
        # 推断或使用提供的参数
        tool_params = parameters if parameters is not None else _infer_parameters(func)

        # 创建工具定义
        tool_def = ToolDefinition(
            name=name,
            description=description,
            parameters=tool_params,
            handler=func,
            category=category,
        )

        # 注册到指定的注册中心或默认注册中心
        target_registry = registry if registry is not None else get_default_registry()
        target_registry.register(tool_def)

        # 保留原函数的元数据
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # 添加工具定义引用
        wrapper._tool_definition = tool_def  # type: ignore

        return wrapper

    return decorator