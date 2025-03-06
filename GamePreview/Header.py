# try:
#     import openai  # 或对应AI平台的SDK
# except ImportError:
#     raise ImportError("请先安装openai包: pip install openai")
from typing import Dict, Any
import time
import logging

# 方案1：使用HuggingFace Transformers本地模型（需要6GB+显存）
# from transformers import AutoTokenizer, AutoModelForCausalLM

# class AINPC:
#     async def make_decision(self, game_state: Dict) -> Dict:
#         prompt = self._build_prompt(game_state)
        
#         # 使用本地模型（示例使用phi-3-mini）
#         tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini-4k-instruct")
#         model = AutoModelForCausalLM.from_pretrained("microsoft/phi-3-mini-4k-instruct")
        
#         inputs = tokenizer(prompt, return_tensors="pt")
#         outputs = model.generate(**inputs, max_new_tokens=500)
#         raw_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#         decision = self._parse_response(raw_response)
#         self._update_memory(decision)
#         return decision

# 方案2：使用Ollama本地模型服务（需要先安装ollama）
# 安装命令：https://ollama.com/download
class AINPC:
    async def make_decision(self, game_state: Dict) -> Dict:
        try:
            import aiohttp
        except ImportError:
            raise ImportError("请先安装aiohttp包: pip install aiohttp")
        
        # 检查是否存在_build_prompt方法
        # 定义默认的提示词构建方法
        def _build_prompt(self, game_state: Dict) -> str:
            return f"""
            当前游戏状态：{str(game_state)}
            请根据当前状态做出合理决策。
            """
            
        # 使用类的提示词构建方法
        prompt = self._build_prompt(game_state)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",  # 可替换为其他模型
                    "prompt": prompt,
                    "options": {"temperature": 0.7}
                }
            ) as resp:
                raw_response = await resp.text()
        
        decision = self._parse_response(raw_response)
        return decision

# # 方案3：使用HuggingFace Inference API（免费版有限制）
# class AINPC:
#     async def make_decision(self, game_state: Dict) -> Dict:
#         import os
#         from huggingface_hub import AsyncInferenceClient
        
#         prompt = self._build_prompt(game_state)
#         client = AsyncInferenceClient(token=os.getenv("HF_TOKEN"))
        
#         response = await client.text_generation(
#             prompt=prompt,
#             max_new_tokens=500,
#             temperature=0.7
#         )
        
#         decision = self._parse_response(response)
#         return decision
# 合并两个AINPC类定义并添加必要的方法
# class AINPC:
#     def __init__(self, npc_id: int, api_key: str, persona: Dict):
#         self.npc_id = npc_id
#         self.api_key = api_key
#         self.persona = persona
#         self.memory = []
#         self.last_action = None
#
#     def _build_prompt(self, game_state: Dict) -> str:
#         """构建基础提示词模板"""
#         return f"""
#         当前游戏状态：{str(game_state)}
#         请根据当前状态做出合理决策。
#         """
#
#     async def make_decision(self, game_state: Dict) -> Dict:
#         """合并后的决策方法"""
#         try:
#             import aiohttp
#             import json
#         except ImportError as e:
#             raise ImportError(f"缺少依赖包: {e.name}")
#
#         prompt = self._build_prompt(game_state)
#
#         async with aiohttp.ClientSession() as session:
#             async with session.post(
#                 "http://localhost:11434/api/generate",
#                 json={
#                     "model": "llama3",
#                     "prompt": prompt,
#                     "options": {"temperature": 0.7}
#                 }
#             ) as resp:
#                 raw_response = await resp.text()
#
#         return self._parse_response(raw_response)
#
#     def _parse_response(self, raw_response: str) -> Dict:
#         """合并响应解析方法"""
#         import json
#         try:
#             return json.loads(raw_response)
#         except json.JSONDecodeError:
#             return {
#                 "action": "wait",
#                 "target": None,
#                 "dialogue": "（解析响应失败）"
#             }
#
#     def _update_memory(self, decision: Dict):
#         """添加内存更新方法"""
#         self.memory.append(decision)
#         if len(self.memory) > 10:
#             self.memory.pop(0)
# #     def _build_prompt(self, game_state: Dict) -> str:
# #         """构建符合角色设定的提示词"""
# #         prompt_template = f"""
# #         {self.persona['background']}
# #         当前游戏状态：
# #         - 玩家位置：{game_state['player_pos']}
# #         - NPC资源：{game_state['npc_resources']}
# #         - 近期事件：{game_state['recent_events']}
#
# #         请以{self.persona['name']}的身份思考，根据以下原则做出决策：
# #         1. {self.persona['behavior_rules'][0]}
# #         2. {self.persona['behavior_rules'][1]}
# #         3. 保持行为符合角色设定：{self.persona['personality']}
#
# #         请用JSON格式返回决策，包含以下字段：
# #         "action": 执行的动作类型,
# #         "target": 目标对象,
# #         "dialogue": 要说的台词
# #         """
# #         return prompt_template
# #     async def make_decision(self, game_state: Dict) -> Dict:
# #         """调用AI模型生成决策"""
# #         prompt = self._build_prompt(game_state)
# #
# #         try:
# #             response = openai.ChatCompletion.create(
# #                 model="gpt-4",
# #                 messages=[{
# #                     "role": "user",
# #                     "content": prompt
# #                 }],
# #                 temperature=0.7,
# #                 max_tokens=500
# #             )
#
# #             decision = self._parse_response(response.choices[0].message.content)
# #             self._update_memory(decision)
# #             return decision
# #
# #         except Exception as e:
# #             return self._fallback_behavior()
# #
# #     def _parse_response(self, raw_response: str) -> Dict:
# #         """解析AI返回的自然语言为结构化数据"""
# #         # 这里可以加入格式校验和逻辑过滤
# #         import json
# #         try:
# #             return json.loads(raw_response)
# #         except:
# #             return {
# #                 "action": "wait",
# #                 "target": None,
# #                 "dialogue": "（似乎正在思考）"
# #             }
# #
# #     def _update_memory(self, decision: Dict):
# #         """更新NPC记忆，限制最大记忆长度"""
# #         self.memory.append(decision)
# #         if len(self.memory) > 10:
# #             self.memory.pop(0)
# #
# #     def _fallback_behavior(self):
# #         """API调用失败时的备用策略"""
# #         return {
# #             "action": "move",
# #             "target": "random",
# #             "dialogue": "我需要时间考虑..."
# #         }
# #
# #
class EnhancedAINPC(AINPC):
    def _build_prompt(self, game_state: Dict) -> str:
        """增强的上下文构建方法"""
        # 获取最近3条记忆记录
        context_window = "\n".join(
            [f"{i + 1}. {m['action']} -> {m['dialogue']}"
             for i, m in enumerate(self.memory[-3:])]
        ) if hasattr(self, 'memory') else ""

        # 构建基础提示词
        base_prompt = f"""
        当前游戏状态：
        - 玩家位置：{game_state['player_pos']}
        - NPC资源：{game_state['npc_resources']}
        - 近期事件：{game_state['recent_events']}
        """

        # 添加上下文记忆
        return f"""
        {base_prompt}

        近期行为记录：
        {context_window}

        请确保新决策与近期行为保持逻辑连贯性
        """
#
#
class ValidatedAINPC(AINPC):
    ACTION_WHITELIST = ["move", "attack", "trade", "dialogue"]
#
    def _parse_response(self, raw_response: str) -> Dict:
        """解析AI返回的自然语言为结构化数据"""
        import json
        try:
            # 先尝试解析JSON
            decision = json.loads(raw_response)
        except:
            # JSON解析失败时使用默认值
            decision = {
                "action": "wait",
                "target": None,
                "dialogue": "（似乎正在思考）"
            }
#
        # 校验动作类型
        if decision["action"] not in self.ACTION_WHITELIST:
            decision["action"] = "wait"
#
        # 过滤敏感词
        banned_words = ["kill", "destroy"]
        for word in banned_words:
            if "dialogue" in decision:
                decision["dialogue"] = decision["dialogue"].replace(word, "***")
#
        return decision
#
#
from functools import lru_cache
import random
from typing import List
#
#
class CachedAINPC(AINPC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response_cache = {}  # 使用字典作为缓存存储
        self.cache_size = 100  # 最大缓存条目数
#
    def _get_cached_response(self, prompt_key: str, game_state: Dict) -> Dict:
        """对相似场景使用缓存决策"""
        # 使用可哈希的字符串作为键
        return self._response_cache.get(prompt_key)
#
    def _cache_response(self, prompt_key: str, response: Dict):
        """存储响应到缓存"""
        if len(self._response_cache) >= self.cache_size:
            # 如果缓存已满，删除最早的条目
            oldest_key = next(iter(self._response_cache))
            del self._response_cache[oldest_key]
        self._response_cache[prompt_key] = response
#
    async def make_decision(self, game_state: Dict) -> Dict:
        prompt = self._build_prompt(game_state)
        # 使用前200个字符作为缓存键
        prompt_key = prompt[:200]
#
        if random.random() < 0.7:  # 70%概率使用缓存
            cached_response = self._get_cached_response(prompt_key, game_state)
            if cached_response:
                return cached_response
#
        # 如果没有缓存或不使用缓存，生成新响应
        response = await super().make_decision(game_state)
        self._cache_response(prompt_key, response)
        return response
#
class BatchAINPC(AINPC):
    async def batch_decide(self, npc_list: List[AINPC], game_states: List[Dict]):
        """批量处理NPC决策请求"""
        import aiohttp
        
        prompts = [npc._build_prompt(gs) for npc, gs in zip(npc_list, game_states)]

        # 使用 Ollama 的批量请求接口
        async with aiohttp.ClientSession() as session:
            responses = []
            for prompt in prompts:
                async with session.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "options": {"temperature": 0.7}
                    }
                ) as resp:
                    raw_response = await resp.text()
                    responses.append(raw_response)

        return [self._parse_response(r) for r in responses]
class CostControlledAINPC(AINPC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monthly_budget = 100  # 美元
        self.token_counter = 0
#
    async def make_decision(self, game_state: Dict) -> Dict:  # 添加async
        if self._check_budget():
            return await super().make_decision(game_state)  # 添加await
        else:
            return self._budget_fallback()
#
    def _check_budget(self) -> bool:
        """基于token计算的成本控制"""
        # 假设每1000 tokens $0.02
        estimated_cost = self.token_counter * 0.02 / 1000
        return estimated_cost < self.monthly_budget
#
    def _budget_fallback(self):
        return {
            "action": "wait",
            "dialogue": "我需要休息一下..."
        }
#
#
# 监控装饰器示例
def monitor_api_call(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
#
        if not hasattr(logging, 'info'):  # 安全校验日志模块
            print(f"[监控] API调用耗时：{duration:.2f}s")  # 备用输出
        else:
            logging.info(f"API调用耗时：{duration:.2f}s")
        class MonitoringSystem:
            @staticmethod
            def record_call(npc_id: int, success: bool, tokens_used: int):
                pass  # 待实现具体监控逻辑
        return result
#
    return wrapper