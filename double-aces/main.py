import random


class Card:
    # 限定Card对象只能绑定suite和face属性
    __slots__ = ('suite', 'face')

    def __init__(self, suite, face):
        # 牌的花色和点数
        self.suite = suite
        self.face = face

    def __repr__(self):
        # 打印牌
        return Card.suites()[self.suite] + Card.faces()[self.face]

    def __lt__(self, other):
        # 牌序
        if self.face == other.face:
            return self.suite < other.suite
        else:
            return self.face < other.face

    @staticmethod
    def suites():
        # 牌的花色集
        return ['♠', '♥', '♣', '♦']

    @staticmethod2

    def faces():
        # 牌的点数集
        return ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class Poker:
    def __init__(self):
        # 扑克牌牌堆和索引
        self.cards = []
        self.index = 0

    def __repr__(self):
        # 打印牌堆
        return f'剩余牌堆：{self.cards[self.index:]}'

    def poker(self):
        # 创建一副标准扑克
        for suite in range(4):
            for face in range(1, 14):
                card = Card(suite, face)
                self.cards.append(card)

    def shuffle(self):
        # 洗牌
        random.shuffle(self.cards)
        self.index = 0

    def deal(self):
        # 发牌
        card = self.cards[self.index]
        self.index += 1
        return card


class Player:
    def __init__(self, name):
        # 玩家的昵称和手牌
        self.name = name
        self.cards = []
        self.cards_num = len(self.cards)

    def __repr__(self):
        # 打印手牌
        return f'{self.name}的手牌：{self.cards}'

    def no_more(self):
        # 过
        pass

    def one_more(self, card):
        # 摸牌
        self.cards.append(card)
        self.cards_num = len(self.cards)
        self.arrange()

    def arrange(self):
        # 手牌排序
        self.cards.sort()


class Check:
    @staticmethod
    def is_double_aces(player):
        # 是否双万
        if player.cards_num == 6:
            i_d_a = True
            for card in player.cards:
                if card.face != 1:
                    i_d_a = False
                    break
            if i_d_a:
                return True
        else:
            return False

    @staticmethod
    def is_tena(player):
        # 是否万立
        if player.cards_num == 6:
            if player.cards[0].face == 1 and player.cards[1].face in (10, 11, 12, 13):
                return True
        else:
            return False

    @staticmethod
    def the_sum(player):
        # 手牌点数和
        t_s = 0
        for card in player.cards:
            may_face = card.face
            if card.face in (11, 12, 13):
                may_face = 10
            if card.face == 1:
                change = int(input(f'{player.name}的手牌为{player.cards}，是否把{card}视为11点：'))
                if change:
                    may_face = 11
            t_s += may_face
        if t_s > 21:
            t_s = 0
        elif t_s >= 16:
            if player.cards_num == 5:
                t_s = 22
        return t_s


def main():
    # 创建玩家
    players = []
    players_num = int(input('请输入玩家人数：'))

    for each_player in range(players_num):
        player = Player(str(input(f'请输入{each_player + 1}号玩家的名字：')))
        players.append(player)

    # 创建扑克牌
    poker1 = Poker()
    poker1.poker()

    while True:
        '''一局游戏'''

        # 洗牌
        poker1.shuffle()
        for one in players:
            one.cards = []

        # 初始手牌
        for _ in range(2):
            for index in range(players_num):
                players[index].one_more(poker1.deal())

        for one in players:
            print(f'{one.name}:{one.cards}')

        while True:
            '''摸牌'''

            cards_nums = [one.cards_num >= 5 for one in players]
            if all(cards_nums):
                break

            for one in players:
                if one.cards_num < 5:
                    get = int(input(f'{one.name}的手牌为{one.cards}，请选择是否摸牌：'))
                    if get:
                        one.one_more(poker1.deal())
                    else:
                        one.no_more()
                        one.cards_num = 6
                    print(f'{one.name}:{one.cards}')

        # 亮牌
        end = []
        for one in players:
            if Check.is_double_aces(one):
                one.t_s = 24
                print(f'{one.name}的牌是:{one.cards}——双万！')
            elif Check.is_tena(one):
                one.t_s = 23
                print(f'{one.name}的牌是:{one.cards}——万立！')
            else:
                one.t_s = Check.the_sum(one)
                if one.t_s == 22:
                    print(f'{one.name}的牌是:{one.cards}——五龙！')
                elif one.t_s == 0:
                    print(f'{one.name}的牌是:{one.cards}，点数大于21——糊了T_T')
                else:
                    print(f'{one.name}的牌是:{one.cards}，点数为{one.t_s}')
            end.append(one.t_s)

        # 结算
        max_num = max(end)
        min_num = min(end)
        if max_num == 24 and min_num == 0:
            max_num = min_num
        for index in range(len(end)):
            if end[index] == max_num:
                print(f'{players[index].name}获胜！')

        if int(input('是否再来一局：')):
            pass
        else:
            break


if __name__ == '__main__':
    main()
