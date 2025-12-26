# libTicket

面向图书馆系统馆员的轻量级聊天式工单助手。系统根据知识库内容判断问题是否可以直接解答，否则自动提示需补充的信息并创建工单。

## 功能概览
- 通过关键词匹配知识库（`data/ticket_kb.json`）快速返回已有 Wiki/资料的答案。
- 无匹配时自动生成需要补充的细节清单并创建工单记录。
- 提供简单的 CLI 体验，方便在终端演示和验证流程。

## 快速开始
1. 确认环境中已安装 Python 3.10+。
2. 直接运行 CLI，使用默认知识库示例：
   ```bash
   python app.py "图书馆 wifi 一直认证失败"
   ```
3. 使用自定义知识库：
   ```bash
   python app.py "自助打印机卡纸了" --kb path/to/your_kb.json
   ```

## 知识库格式
`data/ticket_kb.json` 使用一个数组存储文章条目，每个条目包含：
- `id`: 唯一标识
- `title`: 条目标题
- `keywords`: 用于匹配问题的关键词列表
- `answer`: 推荐回复/操作步骤
- `references`: 可选的参考链接列表

## 目录结构
- `app.py`: CLI 入口，展示完整的问答到工单流程。
- `libticket/kb.py`: 知识库加载与匹配逻辑。
- `libticket/system.py`: 主流程，负责答案生成与工单创建。
- `libticket/ticket.py`: 工单数据结构与简易存储。
- `data/ticket_kb.json`: 示例知识库内容。
