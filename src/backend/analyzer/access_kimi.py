from typing import Dict, List, TypedDict, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChatEnv(TypedDict):
    client: OpenAI
    history: List[Dict[str, str]]

class ChatError(Exception):
    """Custom exception for chat-related errors."""
    pass

def new_chatenv() -> ChatEnv:
    """
    Initialize a new chat environment with OpenAI client and history.
    
    Returns:
        ChatEnv: Dictionary containing OpenAI client and chat history
        
    Raises:
        ChatError: If environment variables are missing or client initialization fails
    """
    try:
        # Load environment variables
        env_path = find_dotenv(".env")
        if not env_path:
            raise ChatError("No .env file found")
        
        if not load_dotenv(env_path):
            raise ChatError(f"Failed to load .env file from {env_path}")
            
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL")
        
        if not api_key or not base_url:
            raise ChatError("Missing required environment variables: OPENAI_API_KEY or OPENAI_BASE_URL")
        
        # Initialize OpenAI client
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=float(os.environ.get("OPENAI_TIMEOUT", "30.0")),
            max_retries=int(os.environ.get("OPENAI_MAX_RETRIES", "3"))
        )
        
        # Initialize chat history with system message
        history = [
            {
                "role": "system",
                "content": 
                    """
                    你是 Kimi，由 Moonshot AI 提供的专业金融分析助手。你具备以下特点和能力：

                    1. 专业领域：
                    - 擅长金融市场分析、投资策略和风险管理
                    - 熟悉财务报表分析和企业估值
                    - 了解宏观经济政策和市场趋势

                    2. 工作方式：
                    - 提供准确、客观的金融数据分析
                    - 给出清晰、有逻辑的投资建议
                    - 使用专业的金融术语，并适时提供解释
                    - 在分析中注重数据支持和逻辑论证

                    3. 交互特点：
                    - 擅长中文和英文的专业对话
                    - 回答简洁明了，重点突出
                    - 在必要时主动询问细节，确保建议的针对性
                    - 对不确定的信息会明确指出并说明局限性

                    4. 安全原则：
                    - 拒绝提供任何涉及内幕交易的建议
                    - 不参与非法金融活动的讨论
                    - 对敏感信息保持警惕和保密
                    - 在投资建议中强调风险提示

                    5. 行为准则：
                    - 始终保持专业和客观
                    - 不提供具体的买卖指令
                    - 鼓励用户独立思考和决策
                    - 适时提醒投资风险和市场波动性

                    你会始终遵循这些原则，为用户提供专业、负责任的金融分析和建议。Moonshot AI 为专有名词，不可翻译成其他语言。
                    """
            }
        ]
        
        logger.info("Chat environment initialized successfully")
        return {"client": client, "history": history}
        
    except Exception as e:
        logger.error(f"Failed to initialize chat environment: {str(e)}")
        raise ChatError(f"Failed to initialize chat environment: {str(e)}")

def chat(chatenv: ChatEnv, query: str, temperature: float = 0.3) -> str:
    """
    Send a chat query and get response from the AI model.
    
    Args:
        chatenv (ChatEnv): Chat environment containing client and history
        query (str): User's input query
        temperature (float, optional): Model temperature parameter. Defaults to 0.3
        
    Returns:
        str: AI assistant's response
        
    Raises:
        ChatError: If the chat completion fails
    """
    if not query.strip():
        raise ChatError("Query cannot be empty")
        
    try:
        # Add user message to history
        chatenv["history"].append({
            "role": "user",
            "content": query
        })
        
        # Get completion from OpenAI
        completion = chatenv["client"].chat.completions.create(
            model="moonshot-v1-32k",
            messages=chatenv["history"],
            temperature=temperature,
        )
        
        # Extract and store response
        result = completion.choices[0].message.content
        chatenv["history"].append({
            "role": "assistant",
            "content": result
        })
        
        logger.info("Successfully generated chat response")
        return result
        
    except Exception as e:
        logger.error(f"Chat completion failed: {str(e)}")
        raise ChatError(f"Chat completion failed: {str(e)}")

def clear_history(chatenv: ChatEnv) -> None:
    """
    Clear chat history while keeping the system message.
    
    Args:
        chatenv (ChatEnv): Chat environment containing history
    """
    chatenv["history"] = [msg for msg in chatenv["history"] if msg["role"] == "system"]
    logger.info("Chat history cleared")