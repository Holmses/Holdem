import itertools
import pandas as pd
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 10000  # 模拟的次数，用于估算胜率
NB_PLAYER = 6  # 玩家数量
community_card = []  # 公共牌为空

def generate_all_combinations():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['H', 'D', 'C', 'S']  # 红桃（Hearts）、方块（Diamonds）、梅花（Clubs）、黑桃（Spades）

    # 生成一副牌的所有52张牌
    deck = [suit + rank for rank in ranks for suit in suits]

    # 使用itertools生成所有可能的两张手牌组合
    all_combinations = list(itertools.combinations(deck, 2))

    return all_combinations

def calculate_probabilities(all_combinations):
    probabilities = {}

    for hole_cards in all_combinations:
        print(hole_cards)
        hole_card_1 = hole_cards[0]
        hole_card_2 = hole_cards[1]

        # 将手牌转换成pypokerengine需要的格式
        hole_cards_pypoker = gen_cards([hole_card_1, hole_card_2])
        # 估算手牌组合的胜率
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=NB_PLAYER,
            hole_card=hole_cards_pypoker,
            community_card=gen_cards(community_card)
        )

        # 将结果存入字典
        probabilities[hole_cards] = win_rate

    return probabilities

if __name__ == "__main__":
    # 生成所有手牌组合和计算胜率
    all_combinations = generate_all_combinations()
    probabilities = calculate_probabilities(all_combinations)

    # 将数据存储到DataFrame中
    df_data = {
        '手牌组合': [f"{hole_cards[0]}, {hole_cards[1]}" for hole_cards in probabilities.keys()],
        '胜率': [win_rate for win_rate in probabilities.values()]
    }
    df = pd.DataFrame(df_data)

    # 将DataFrame保存到Excel文件
    excel_file = 'hand_combinations_10000_win_rate.xlsx'
    df.to_excel(excel_file, index=False)

    print(f"数据已保存到 {excel_file}")