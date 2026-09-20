from tools.core.base_tool import BaseTool, ToolExecutionContext
from tools.core.registry import ToolRegistry
from tools.web.web_search import WebSearchTool
from tools.stubs import (
    CRMTool,
    FinanceTool,
    MessagingTool,
    EmailTool,
    DatabaseTool,
    AnalyticsTool,
    BrowserTool,
)

# Register default mock tools
ToolRegistry.register(WebSearchTool())
ToolRegistry.register(CRMTool())
ToolRegistry.register(FinanceTool())
ToolRegistry.register(MessagingTool())
ToolRegistry.register(EmailTool())
ToolRegistry.register(DatabaseTool())
ToolRegistry.register(AnalyticsTool())
ToolRegistry.register(BrowserTool())

__all__ = [
    "BaseTool",
    "ToolExecutionContext",
    "ToolRegistry",
    "WebSearchTool",
    "CRMTool",
    "FinanceTool",
    "MessagingTool",
    "EmailTool",
    "DatabaseTool",
    "AnalyticsTool",
    "BrowserTool",
]
