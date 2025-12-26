from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional
import json
import pathlib


@dataclass
class KnowledgeArticle:
    """Represents a knowledge base article.

    Attributes:
        id: Unique identifier for the article.
        title: Short title for the issue.
        keywords: Keywords that indicate the article is relevant.
        answer: Suggested resolution text.
        references: Optional list of references for further reading.
    """

    id: str
    title: str
    keywords: List[str]
    answer: str
    references: List[str]

    @classmethod
    def from_dict(cls, payload: dict) -> "KnowledgeArticle":
        return cls(
            id=str(payload["id"]),
            title=payload["title"],
            keywords=list(payload.get("keywords", [])),
            answer=payload.get("answer", ""),
            references=list(payload.get("references", [])),
        )


class TicketKB:
    """Lightweight knowledge base backed by static JSON."""

    def __init__(self, articles: Iterable[KnowledgeArticle]):
        self._articles = list(articles)

    @classmethod
    def load(cls, path: pathlib.Path) -> "TicketKB":
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        articles = [KnowledgeArticle.from_dict(item) for item in payload]
        return cls(articles)

    def find_best_match(self, question: str, threshold: float = 0.35) -> Optional[KnowledgeArticle]:
        """Return the article with the highest keyword overlap.

        Args:
            question: User-submitted text.
            threshold: Minimum hit ratio required to consider the answer actionable.
        """

        best_article: Optional[KnowledgeArticle] = None
        best_score = 0.0
        normalized_question = question.lower()

        for article in self._articles:
            hits = sum(1 for keyword in article.keywords if keyword.lower() in normalized_question)
            if not article.keywords:
                continue
            score = hits / len(article.keywords)
            if score > best_score:
                best_score = score
                best_article = article

        if best_score >= threshold:
            return best_article
        return None

    def to_dict(self) -> List[dict]:
        return [
            {
                "id": article.id,
                "title": article.title,
                "keywords": article.keywords,
                "answer": article.answer,
                "references": article.references,
            }
            for article in self._articles
        ]


__all__ = ["KnowledgeArticle", "TicketKB"]
