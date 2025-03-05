import random
import pandas as pd
import time
from typing import List, Dict


# ========== 数据加载 ==========
class CardLoader:
    def __init__(self):
        self.cards = pd.read_csv("BKT.csv").dropna(how='all')
        self.identity_cards = self._parse_cards("阵营身份")
        self.action_cards = self._parse_cards("关键行动")
        self.point_cards = self._parse_cards("情报来源")
        self.effect_cards = self._parse_cards("档案内容")
        self.buff_cards = self._parse_cards("Buff")

    def _parse_cards(self, card_type: str) -> List[Dict]:
        return [self._parse_card(row) for _, row in self.cards[self.cards['类型'] == card_type].iterrows()]
    def _parse_cards_subtype(self, card_type: str,subtype: str) -> List[Dict]:
        list = [self._parse_card(row) for _, row in self.cards[self.cards['类型'] == card_type].iterrows()]
        return list

    def _parse_card(self, row) -> Dict:
        return {
            "ID": row['ID'],
            "type": row['类型'],
            "name": row['名称'],
            "content": row['内容']
        }


# ========== 游戏实体类 ==========
class Player:
    def __init__(self, pid: int):
        self.pid = pid
        self.identity = None
        self.backup = None
        self.hand = []
        self.resources = {'gold': 3, 'intel': 2, 'water': 1}
        self.buffs = []
        self.strategy_model = "deepseek-r1"  # 模拟API推理模型

    def choose_action(self, legal_actions):
        """模拟AI决策过程（简化版随机策略）"""
        print(f"Player {self.pid} 正在思考...（策略模型：{self.strategy_model}）")
        return random.choice(legal_actions) if legal_actions else None

    def __repr__(self):
        return f"Player{self.pid}（资源：{self.resources}）"


class GameState:
    def __init__(self, players: List[Player]):
        self.players = players
        self.global_buffs = []
        self.treasury = {'gold': 10, 'intel': 5}
        self.phase = "setup"


# ========== 游戏逻辑 ==========
class GameEngine:
    def __init__(self):
        self.card_pool = CardLoader()
        self.players = [Player(i) for i in range(5)]
        self.state = GameState(self.players)

    def _setup_game(self):
        # 初始化身份分配
        for p in self.players:
            identities = random.sample(self.card_pool.identity_cards, 2)
            mainbuff = random.sample(self.card_pool.identity_cards, 2)
            p.identity = identities[0]
            p.backup = identities[1]
            print(f"Player {p.pid} 获得身份：{p.identity['name'],p.backup['name']}")

            # 初始手牌抽取
            p.hand = random.sample(self.card_pool.action_cards, 3)
            print(f"初始手牌：{[c['name'] for c in p.hand]}")

    def _build_phase(self):
        print("\n=== 建造阶段 ===")
        for p in self.players:
            legal_actions = [c for c in p.hand if "建造" in c['content']]
            chosen = p.choose_action(legal_actions)
            if chosen:
                print(f"Player {p.pid} 打出 {chosen['name']}")
                self._resolve_card_effect(p, chosen)

    def _resolve_card_effect(self, player, card):
        # 简化的效果解析（示例）
        if "获得" in card['content']:
            if "金币" in card['content']:
                gain = min(3, self.state.treasury['gold'])
                player.resources['gold'] += gain
                self.state.treasury['gold'] -= gain
                print(f"从国库获得{gain}金币")

    def run_simulation(self):
        self._setup_game()
        self._build_phase()
        # 其他阶段可在此扩展...
    def _log_action(self, text):
        """记录行动日志并计算耗时"""
        self.log.append(text)
        time.sleep(len(text) * 0.1)  # 根据字数模拟耗时

# ========== 平衡性分析公式 ==========
def balance_metric(card):
    """卡牌平衡性校准参数公式"""
    cost = len([k for k in ['金币', '情报', '水'] if k in card['content']])
    impact = 1 + card['content'].count('获得') * 0.5 - card['content'].count('消耗') * 0.3
    flexibility = 0.5 if "需" in card['content'] else 1
    return (impact * flexibility) / (cost + 1)
# 平衡系数 = (效果强度 × 灵活性) / (消耗成本 + 1)
# 其中：
# - 效果强度 = 1 + 获得类效果数量×0.5 - 消耗类效果数量×0.3
# - 灵活性 = 0.5（有条件限制时）或 1（无条件）
# - 消耗成本 = 涉及资源类型的数量（金币/情报/水）

# ========== 执行示例 ==========
if __name__ == "__main__":
    game = GameEngine()
    game.run_simulation()

    # 平衡性报告
    print("\n=== 卡牌平衡性评估 ===")
    for card in game.card_pool.action_cards:
        score = balance_metric(card)
        print(f"{card['name']}: {score:.2f}")