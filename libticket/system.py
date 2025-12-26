from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .kb import KnowledgeArticle, TicketKB
from .ticket import Ticket, TicketStore


@dataclass
class ChatResponse:
    """Result of processing a user message."""

    resolution: str
    article: Optional[KnowledgeArticle] = None
    ticket: Optional[Ticket] = None

    def to_dict(self) -> Dict[str, str]:
        payload: Dict[str, str] = {"resolution": self.resolution}
        if self.article:
            payload["article_id"] = self.article.id
            payload["article_title"] = self.article.title
        if self.ticket:
            payload["ticket_id"] = str(self.ticket.id)
        return payload


class TicketSystem:
    """Routes chat-style questions to KB answers or ticket creation."""

    def __init__(self, kb: TicketKB, store: TicketStore):
        self.kb = kb
        self.store = store
        self.default_detail_prompts = [
            "身份与证件号（学生/老师/校友等）",
            "联系方式（邮箱或电话）",
            "问题发生的时间与地点（如设备编号、阅览室、网站链接）",
            "具体报错信息或截图",
            "期望的解决时限",
        ]

    def handle_question(self, question: str) -> ChatResponse:
        article = self.kb.find_best_match(question)
        if article:
            resolution = (
                f"为您找到了相关指引：《{article.title}》。\n"
                f"建议方案：{article.answer}\n"
                f"参考资料：{'; '.join(article.references) if article.references else '（暂无资料链接）'}"
            )
            return ChatResponse(resolution=resolution, article=article)

        ticket = self.store.create(question=question, requested_details=self.default_detail_prompts)
        resolution_lines: List[str] = [
            "暂时没有找到可以直接回复的知识库答案。为了加快处理，请补充以下信息：",
        ]
        for item in self.default_detail_prompts:
            resolution_lines.append(f"- {item}")
        resolution_lines.append(
            f"已为您创建工单 #{ticket.id}，收到补充信息后系统馆员将跟进。"
        )
        resolution = "\n".join(resolution_lines)
        return ChatResponse(resolution=resolution, ticket=ticket)


__all__ = ["ChatResponse", "TicketSystem"]
