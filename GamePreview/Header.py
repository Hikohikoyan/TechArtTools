"""
根据游戏规则设计的简化版模拟程序（核心逻辑演示）
注意：由于文本交互限制，这里展示核心数据结构与流程模拟
"""
import csv
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List


# ---------- 数据结构定义 ----------
@dataclass
class Card:
    id: str
    type: str
    name: str
    effect: dict


@dataclass
class Player:
    name: str
    identity: Card = None  # 当前身份
    backup_identity: Card = None
    hand: List[Card] = field(default_factory=list)
    resources: Dict[str, int] = field(default_factory=lambda: {"gold": 5, "intel": 3, "prestige": 1})
    nodes: List[dict] = field(default_factory=list)
    buffs: List[Card] = field(default_factory=list)


@dataclass
class GameState:
    players: List[Player]
    current_phase: str = "preparation"
    global_debuffs: List[Card] = field(default_factory=list)
    treasury: Dict[str, int] = field(default_factory=lambda: {"gold": 20, "water": 10})
    round: int = 0

CSV_Field = {
    "id" : "ID", #唯一索引
    "type":"类型",
    "name" :"名称",
    "effect" :"内容",
}
# ---------- 卡牌配置 ----------
def load_cards() -> List[Card]:
    """示例卡牌数据（实际需要完整实现EXCEL解析）"""
    csv_path = "BKT.csv"
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        return [Card(str(row[CSV_Field['id']]), str(row[CSV_Field['type']]), string(row[CSV_Field['name']]), string(row[CSV_Field['effect']]))
                for row in reader]
    # return {
    #     "阵营身份": {
    #         "#001": Card("#001", "阵营身份", "审判长", {"阵营": "方舟派", "类型": "领袖"}),
    #         # ... 其他身份卡
    #     },
    #     "关键行动": {
    #         "#013": Card("#013", "关键行动", "家园建设", {"类型": "建造", "效果": "建造节点"}),
    #         # ... 其他行动卡
    #     },
    #     # ... 其他卡牌类型
    # }
# ---------- 核心逻辑 ----------
class GameSimulator:
    def __init__(self, player_count=4):
        self.cards = load_cards()#input("请输入卡牌配置CVS文件的路径 "))
        self.state = GameState([Player(f"Player{i + 1}") for i in range(player_count)])
        self.log = []

    def _log_action(self, text):
        """记录行动日志并计算耗时"""
        self.log.append(text)
        time.sleep(len(text) * 0.1)  # 根据字数模拟耗时

    def setup_game(self):
        """初始化游戏"""
        self._log_action("=== 游戏初始化 ===")
        # 分配身份卡逻辑...

    def run_round(self):
        """运行单轮游戏"""
        self.state.round += 1
        self._log_action(f"\n=== 第 {self.state.round} 轮开始 ===")

        # 阶段模拟
        self._building_phase()
        self._trading_phase()
        self._crisis_phase()

    def _building_phase(self):
        """建造阶段逻辑示例"""
        self._log_action("\n--- 建造阶段 ---")
        for p in self.state.players:
            action = random.choice(["建造节点", "使用卡牌", "跳过"])
            self._log_action(f"{p.name} 选择操作：{action}")
    def _trading_phase(self):
        """交易阶段逻辑示例"""
        self._log_action("\n--- 建造阶段 ---")
        for p in self.state.players:
            action = random.choice(["建造节点", "使用卡牌", "跳过"])
            self._log_action(f"{p.name} 选择操作：{action}")
    def _crisis_phase(self):
        """危机阶段逻辑示例"""
        self._log_action("\n--- 建造阶段 ---")
        for p in self.state.players:
            action = random.choice(["建造节点", "使用卡牌", "跳过"])
            self._log_action(f"{p.name} 选择操作：{action}")



# ---------- 示例运行 ----------
if __name__ == "__main__":
    simulator = GameSimulator(player_count=4)
    simulator.setup_game()

    # 模拟3轮游戏
    for _ in range(3):
        simulator.run_round()

    print("\n".join(simulator.log))
    print("\n=== 模拟完成 ===")