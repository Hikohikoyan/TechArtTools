import openai  # 或对应AI平台的SDK
from typing import Dict, Any


class AINPC:
    def __init__(self, npc_id: int, api_key: str, persona: Dict):
        self.npc_id = npc_id
        self.api_key = api_key
        self.persona = persona  # NPC角色设定
        self.memory = []  # 记忆存储
        self.last_action = None

    def _build_prompt(self, game_state: Dict) -> str:
        """构建符合角色设定的提示词"""
        prompt_template = f"""
        {self.persona['background']}
        当前游戏状态：
        - 玩家位置：{game_state['player_pos']}
        - NPC资源：{game_state['npc_resources']}
        - 近期事件：{game_state['recent_events']}

        请以{self.persona['name']}的身份思考，根据以下原则做出决策：
        1. {self.persona['behavior_rules'][0]}
        2. {self.persona['behavior_rules'][1]}
        3. 保持行为符合角色设定：{self.persona['personality']}

        请用JSON格式返回决策，包含以下字段：
        "action": 执行的动作类型,
        "target": 目标对象,
        "dialogue": 要说的台词
        """
        return prompt_template

    async def make_decision(self, game_state: Dict) -> Dict:
        """调用AI模型生成决策"""
        prompt = self._build_prompt(game_state)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.7,
                max_tokens=500
            )

            decision = self._parse_response(response.choices[0].message.content)
            self._update_memory(decision)
            return decision

        except Exception as e:
            return self._fallback_behavior()

    def _parse_response(self, raw_response: str) -> Dict:
        """解析AI返回的自然语言为结构化数据"""
        # 这里可以加入格式校验和逻辑过滤
        try:
            return json.loads(raw_response)
        except:
            return {
                "action": "wait",
                "target": None,
                "dialogue": "（似乎正在思考）"
            }

    def _update_memory(self, decision: Dict):
        """更新NPC记忆，限制最大记忆长度"""
        self.memory.append(decision)
        if len(self.memory) > 10:
            self.memory.pop(0)

    def _fallback_behavior(self):
        """API调用失败时的备用策略"""
        return {
            "action": "move",
            "target": "random",
            "dialogue": "我需要时间考虑..."
        }


class EnhancedAINPC(AINPC):
    def _build_prompt(self, game_state: Dict) -> str:
        """增强的上下文构建方法"""
        context_window = "\n".join(
            [f"{i + 1}. {m['action']} -> {m['dialogue']}"
             for i, m in enumerate(self.memory[-3:])]
        )

        return f"""
        {super()._build_prompt(game_state)}

        近期行为记录：
        {context_window}

        请确保新决策与近期行为保持逻辑连贯性
        """


class ValidatedAINPC(AINPC):
    ACTION_WHITELIST = ["move", "attack", "trade", "dialogue"]

    def _parse_response(self, raw_response: str) -> Dict:
        decision = super()._parse_response(raw_response)

        # 校验动作类型
        if decision["action"] not in self.ACTION_WHITELIST:
            decision["action"] = "wait"

        # 过滤敏感词
        banned_words = ["kill", "destroy"]
        for word in banned_words:
            decision["dialogue"] = decision["dialogue"].replace(word, "***")

        return decision


from functools import lru_cache


class CachedAINPC(AINPC):
    @lru_cache(maxsize=100)
    def _get_cached_response(self, prompt_hash: int) -> Dict:
        """对相似场景使用缓存决策"""
        return super().make_decision()

    async def make_decision(self, game_state: Dict) -> Dict:
        prompt = self._build_prompt(game_state)
        prompt_hash = hash(prompt[:200])  # 取前200字符的哈希

        if random.random() < 0.7:  # 70%概率使用缓存
            return self._get_cached_response(prompt_hash)
        else:
            return await super().make_decision(game_state)


class BatchAINPC(AINPC):
    async def batch_decide(self, npc_list: List[AINPC], game_states: List[Dict]):
        """批量处理NPC决策请求"""
        prompts = [npc._build_prompt(gs) for npc, gs in zip(npc_list, game_states)]

        # 使用API的批量请求接口
        responses = await openai.BatchCompletion.create(
            inputs=prompts,
            batch_size=10
        )

        return [self._parse_response(r) for r in responses]

class CostControlledAINPC(AINPC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monthly_budget = 100  # 美元
        self.token_counter = 0

    async def make_decision(self, game_state: Dict) -> Dict:
        if self._check_budget():
            return super().make_decision(game_state)
        else:
            return self._budget_fallback()

    def _check_budget(self) -> bool:
        """基于token计算的成本控制"""
        # 假设每1000 tokens $0.02
        estimated_cost = self.token_counter * 0.02 / 1000
        return estimated_cost < self.monthly_budget

    def _budget_fallback(self):
        return {
            "action": "wait",
            "dialogue": "我需要休息一下..."
        }


# 监控装饰器示例
def monitor_api_call(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        logging.info(f"API调用耗时：{duration:.2f}s")
        MonitoringSystem.record_call(
            npc_id=args[0].npc_id,
            success=result is not None,
            tokens_used=result.get('usage', 0)
        )
        return result

    return wrapper