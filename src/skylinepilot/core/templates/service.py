"""
模板服务层（兼容层）
"""
import re
import time
from typing import Dict, List, Optional, Tuple

from template_manager import template_manager


class TemplatesService:
    """模板业务封装，逐步收敛模板规则"""

    def list_templates(self, category: Optional[str] = None) -> List[Dict]:
        return template_manager.list_templates(category=category)

    def build_template_payload(self, request: Dict) -> Tuple[str, str, str, str, List[str]]:
        """规范化模板入参，兼容简化写法"""
        content = request.get("content")
        if not content:
            raise ValueError("缺少消息内容")

        if not request.get("template_id") and not request.get("name"):
            template_id = f"template_{int(time.time() * 1000) % 1000000}"
            variables = list(set(re.findall(r"\{(\w+)\}", content)))
            name = content[:20] + ("..." if len(content) > 20 else "")
            category = "general"
        else:
            template_id = request.get("template_id")
            name = request.get("name")
            category = request.get("category", "general")
            variables = request.get("variables", [])

        return template_id, name, content, category, variables

    def add_template(self, request: Dict) -> Tuple[bool, str, str]:
        template_id, name, content, category, variables = self.build_template_payload(request)
        success = template_manager.add_template(template_id, name, content, category, variables)
        return success, template_id, name

    def delete_template(self, template_id: str) -> bool:
        return template_manager.delete_template(template_id)

    def preview_template(self, template_id: str, vars_payload: Optional[str]) -> str:
        import json
        template_vars = json.loads(vars_payload) if vars_payload else {}
        return template_manager.render_template(template_id, **template_vars)


templates_service = TemplatesService()

