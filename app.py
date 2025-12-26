from __future__ import annotations

import argparse
import pathlib

from libticket.kb import TicketKB
from libticket.system import TicketSystem
from libticket.ticket import TicketStore


def build_system(data_path: pathlib.Path) -> TicketSystem:
    kb = TicketKB.load(data_path)
    store = TicketStore()
    return TicketSystem(kb=kb, store=store)


def main():
    parser = argparse.ArgumentParser(description="图书馆馆员聊天式工单助手")
    parser.add_argument("question", help="用户提出的问题，使用引号包裹")
    parser.add_argument(
        "--kb",
        default="data/ticket_kb.json",
        help="知识库 JSON 路径，默认使用 data/ticket_kb.json",
    )
    args = parser.parse_args()

    kb_path = pathlib.Path(args.kb)
    system = build_system(kb_path)

    response = system.handle_question(args.question)
    print("=== 处理结果 ===")
    print(response.resolution)

    if response.article:
        print(f"\n命中知识库：{response.article.title} (ID: {response.article.id})")
    if response.ticket:
        print(f"\n工单已创建：#{response.ticket.id}")

    if response.ticket:
        print("\n当前工单池：")
        for ticket in system.store.all():
            print(f"- #{ticket.id} | {ticket.question} | 状态: {ticket.status}")


if __name__ == "__main__":
    main()
