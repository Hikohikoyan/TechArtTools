import random
import time
from datetime import datetime
from typing import List, Dict, Any, Optional  # Add Optional import
import json
from Header import AINPC  # <mcsymbol name="AINPC" filename="Header.py" path="F:\TechFuture\TechArtTools\GamePreview\Header.py" startline="4" type="class"></mcsymbol>

class EnhancedAINPC(AINPC):
    """增强版AI玩家，添加规则理解能力"""
    def __init__(self, npc_id: int, api_key: str, persona: Dict):
        super().__init__(npc_id, api_key, persona)
        self.memory = []

    def _get_legal_actions(self, phase: str) -> List[str]:  # 新增方法定义
        """根据阶段获取基础合法行动"""
        base_actions = []
        if phase == 'build':
            base_actions = ['build_node', 'repair', 'attack']
        elif phase == 'trade':
            base_actions = ['public_trade', 'secret_negotiate']
        elif phase == 'crisis':
            base_actions = ['vote', 'challenge', 'claim_leadership']
        return base_actions

    def _build_prompt(self, game_state: Dict) -> str:
        with open(r'F:\TechFuture\TechArtTools\GamePreview\gamerule.txt', 'r', encoding='utf-8') as f:
            rules = f.read()[:2000]

        prompt = f"""你正在参与一个策略桌游, 请严格遵循以下规则：
{rules}

当前游戏状态：
{json.dumps(game_state, indent=2, ensure_ascii=False)}

你的角色设定：{self.persona}
可用行动类型：{self._get_legal_actions(game_state.get('phase', ''))}  # 现在可以正确调用

请用JSON格式返回：
{{"action": "行动类型", "target": "目标玩家/卡牌", "dialogue": "角色台词", "reason": "策略说明"}}"""
        return prompt

    async def make_decision(self, game_state: Dict) -> Dict:
        """核心决策方法（新增）"""
        try:
            prompt = self._build_prompt(game_state)
            response = await self._call_llm_api(prompt)  # 假设已有API调用方法
            return json.loads(response)
        except json.JSONDecodeError:
            print("JSON解析失败，返回默认行动")
            return {"action": "pass", "target": None, "dialogue": "", "reason": "解析失败"}

class AIGameLogger:
    """游戏过程记录器"""
    def __init__(self):
        self.log = []
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def save_log(self):
        filename = f"output_{self.start_time}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            # 添加空日志检查
            if not self.log:
                f.write("本局游戏没有记录任何行动\n")
                return
                
            for entry in self.log:
                f.write(f"[Phase {entry['phase']}] Player {entry['player']}:\n")
                f.write(f"资源: {entry['resources']}\n")
                f.write(f"行动: {entry['action']['action']} -> {entry['action']['dialogue']}\n")
                f.write(f"策略理由: {entry['action'].get('reason','')}\n\n")
        print(f"日志已保存至: {filename}")  # 添加保存路径提示

class AIGameEngine:
    async def run_simulation(self, rounds=3):
        """运行AI对战模拟"""
        # 添加初始化日志
        self.logger.log_turn(-1, {"action": "system", "dialogue": "游戏开始"}, self.state)
        
        # 游戏循环
        for round in range(rounds):
            await self._run_phase('build', '建造阶段')
            await self._run_phase('trade', '交易阶段')
            await self._run_phase('crisis', '危机阶段')
            
            # 轮次结算
            self._apply_global_effects()
        
        # 确保文件保存被执行
        try:
            self.logger.save_log()
        except Exception as e:
            print(f"保存日志失败: {str(e)}")
    def _apply_global_effects(self):  # 新增全局效果应用方法
        """处理轮次结算的全局效果"""
        # 简单示例：每个玩家获得1金币
        for player_state in self.state['players']:
            player_state['resources']['gold'] += 1