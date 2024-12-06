# 金融风险评估模型

基于 Moonshot AI 的智能金融分析助手，提供专业的金融市场分析、投资策略和风险管理建议。

## 环境配置

1. 创建 `.env` 文件并配置以下环境变量：

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=your_base_url
OPENAI_TIMEOUT=30.0  # 可选，默认 30 秒
OPENAI_MAX_RETRIES=3  # 可选，默认 3 次
```

## 快速开始

```python
from src.backend import analyzer

# 初始化聊天环境
chatenv = analyzer.new_chatenv()

# 发送单次查询
response = analyzer.chat(chatenv, "请分析当前市场的主要风险因素")

# 打印响应
print(response)

# 继续对话（会保持上下文）
follow_up = analyzer.chat(chatenv, "针对这些风险，有什么建议的应对策略？")
print(follow_up)

# 清除对话历史（保留系统提示）
analyzer.clear_history(chatenv)
```

## 功能特点

- 专业金融分析：市场分析、投资策略、风险管理
- 智能对话：保持对话上下文，支持多轮交互
- 风险控制：内置风险提示和合规检查
- 双语支持：擅长中文和英文的专业对话

## 使用建议

1. 提问时尽可能具体，包含关键信息
2. 对于复杂问题，建议分步骤提问
3. 注意查看风险提示和局限性说明
4. 重要决策请结合多方面信息

## 错误处理

如果遇到错误，请检查：
- 环境变量是否正确配置
- 网络连接是否正常
- API 密钥是否有效

## 注意事项

- 该模型仅提供分析建议，不构成投资建议
- 所有投资决策请自行承担风险
- 请遵守相关法律法规和金融监管要求