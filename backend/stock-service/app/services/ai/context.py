# -*- coding: utf-8 -*-
"""Agent上下文 - 多Agent数据传递

提供多Agent协作过程中的共享上下文，支持数据传递、观点收集和风险标记。
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class AgentContext:
    """Agent共享上下文

    在多Agent协作过程中，用于存储和传递共享数据。
    支持收集各Agent的观点、风险标记和元数据。

    Attributes:
        query: 用户查询问题
        stock_code: 股票代码
        stock_name: 股票名称
        session_id: 会话ID
        data: 收集的数据字典
        opinions: Agent观点列表
        risk_flags: 风险标记列表
        meta: 元数据字典
        created_at: 创建时间戳
    """

    query: str = ""
    stock_code: str = ""
    stock_name: str = ""
    session_id: str = ""

    # 收集的数据
    data: Dict[str, Any] = field(default_factory=dict)

    # Agent观点列表
    opinions: List[Any] = field(default_factory=list)  # AgentOpinion

    # 风险标记
    risk_flags: List[Dict[str, Any]] = field(default_factory=list)

    # 元数据
    meta: Dict[str, Any] = field(default_factory=dict)

    # 时间戳
    created_at: float = field(default_factory=time.time)

    def add_opinion(self, opinion: Any) -> None:
        """添加观点

        Args:
            opinion: Agent观点对象
        """
        self.opinions.append(opinion)

    def add_risk_flag(
        self, category: str, description: str, severity: str = "medium"
    ) -> None:
        """添加风险标记

        Args:
            category: 风险类别
            description: 风险描述
            severity: 严重程度 (low, medium, high)
        """
        self.risk_flags.append(
            {
                "category": category,
                "description": description,
                "severity": severity,
                "timestamp": time.time(),
            }
        )

    def get_data(self, key: str, default: Any = None) -> Any:
        """获取数据

        Args:
            key: 数据键名
            default: 默认值

        Returns:
            数据值，如果不存在则返回默认值
        """
        return self.data.get(key, default)

    def set_data(self, key: str, value: Any) -> None:
        """设置数据

        Args:
            key: 数据键名
            value: 数据值
        """
        self.data[key] = value

    @property
    def has_risk_flags(self) -> bool:
        """是否有风险标记

        Returns:
            是否存在风险标记
        """
        return len(self.risk_flags) > 0

    @property
    def has_high_risk(self) -> bool:
        """是否有高风险标记

        Returns:
            是否存在高风险标记
        """
        return any(flag.get("severity") == "high" for flag in self.risk_flags)

    def get_risks_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """按严重程度获取风险标记

        Args:
            severity: 严重程度 (low, medium, high)

        Returns:
            符合条件的风险标记列表
        """
        return [flag for flag in self.risk_flags if flag.get("severity") == severity]

    def get_opinions_by_agent(self, agent_name: str) -> List[Any]:
        """按Agent名称获取观点

        Args:
            agent_name: Agent名称

        Returns:
            该Agent的观点列表
        """
        return [
            op
            for op in self.opinions
            if hasattr(op, "agent_name") and op.agent_name == agent_name
        ]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典

        Returns:
            包含上下文数据的字典
        """
        return {
            "query": self.query,
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "session_id": self.session_id,
            "data": self.data,
            "opinions": [
                op.__dict__ if hasattr(op, "__dict__") else str(op)
                for op in self.opinions
            ],
            "risk_flags": self.risk_flags,
            "meta": self.meta,
            "created_at": self.created_at,
        }

    @classmethod
    def create(cls, stock_code: str, query: str = "") -> "AgentContext":
        """创建上下文

        Args:
            stock_code: 股票代码
            query: 用户查询问题

        Returns:
            新的AgentContext实例
        """
        return cls(
            stock_code=stock_code,
            query=query,
            session_id=str(uuid.uuid4()),
        )