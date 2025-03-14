import json
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier

class PuzzleAI:
    def __init__(self):
        # 初始化玩家能力模型
        self.player_model = SGDClassifier(loss='log_loss')
        # 难度决策树
        self.difficulty_tree = DecisionTreeClassifier()
        # 玩家特征数据
        self.X = []
        self.y = []
        self.load_questions()

    def load_questions(self):
        with open('question_bank.json', encoding='utf-8') as f:
            self.questions = json.load(f)['questions']

    def update_model(self, reaction_time, difficulty, is_correct):
        # 特征：反应时间、难度级别
        features = [reaction_time, difficulty]
        self.X.append(features)
        self.y.append(1 if is_correct else 0)
        # 在线学习更新模型
        if len(self.X) > 10:
            self.player_model.partial_fit(self.X, self.y, classes=[0, 1])

    def select_difficulty(self):
        if len(self.X) < 5:
            return np.random.randint(1, 4)
        # 使用决策树预测合适难度
        return self.difficulty_tree.predict([self.X[-1]])[0]

    def recommend_question(self):
        target_diff = self.select_difficulty()
        candidates = [q for q in self.questions 
                      if q['difficulty'] == target_diff]
        return np.random.choice(candidates) if candidates else None