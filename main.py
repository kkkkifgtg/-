from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                QPushButton, QTextEdit, QHBoxLayout, QLabel,
                                QLineEdit, QMessageBox)
from PySide6.QtCore import Qt, QTimer
import sys
import time
from game_ai import PuzzleAI

class PuzzleGameUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai = PuzzleAI()
        self.current_question = None
        self.start_time = 0
        self.score = 0
        self.setWindowTitle('智能猜谜游戏')
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 游戏信息显示
        self.info_label = QLabel('准备开始游戏...')
        self.score_label = QLabel(f'得分: {self.score}')
        
        # 题目显示
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        
        # 用户输入
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText('输入你的答案')
        self.submit_btn = QPushButton('提交答案')
        
        # 提示按钮
        self.hint_btn = QPushButton('获取提示')
        
        # 布局设置
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.info_label)
        header_layout.addStretch()
        header_layout.addWidget(self.score_label)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.answer_input)
        input_layout.addWidget(self.submit_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.question_label)
        main_layout.addSpacing(20)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.hint_btn)
        main_widget.setLayout(main_layout)
        
        # 连接信号
        self.submit_btn.clicked.connect(self.check_answer)
        self.hint_btn.clicked.connect(self.show_hint)
        
        QTimer.singleShot(1000, self.new_question)

    def new_question(self):
        self.current_question = self.ai.recommend_question()
        if self.current_question:
            self.start_time = time.time()
            self.question_label.setText(self.current_question['text'])
            self.info_label.setText(f'当前难度: {self.current_question["difficulty"]}')
            self.answer_input.clear()
        else:
            QMessageBox.information(self, '提示', '题库已用完！')

    def check_answer(self):
        reaction_time = time.time() - self.start_time
        user_answer = self.answer_input.text().strip()
        
        is_correct = user_answer.lower() == self.current_question['answer'].lower()
        self.ai.update_model(reaction_time, 
                           self.current_question['difficulty'], 
                           is_correct)
        
        if is_correct:
            self.score += 10 * self.current_question['difficulty']
            QMessageBox.information(self, '结果', '回答正确！')
        else:
            QMessageBox.critical(self, '结果', 
                               f'错误！正确答案是：{self.current_question["answer"]}')
        
        self.score_label.setText(f'得分: {self.score}')
        self.new_question()

    def show_hint(self):
        if self.current_question and self.current_question['hints']:
            QMessageBox.information(self, '提示', 
                                  '\n'.join(self.current_question['hints']))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PuzzleGameUI()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())