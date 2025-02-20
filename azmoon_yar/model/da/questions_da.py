import mysql.connector
from model.entity.questions import Questions

class QuestionsDA:
    def connect(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Av3032941??",
            database="azmoon_yar"
        )
        self.cursor1 = self.db.cursor()

    def disconnect(self):
        self.cursor1.close()
        self.db.close()

    def get_option_number(self, correct_option):
        """تبدیل مقدار متنی یا عددی گزینه صحیح به عدد"""
        if isinstance(correct_option, int):
            return correct_option
        try:
            return int(correct_option)
        except ValueError:
            options_map = {"گزینه ۱": 1, "گزینه ۲": 2, "گزینه ۳": 3, "گزینه ۴": 4}
            return options_map.get(correct_option, 1)

    def save(self, question):
        self.connect()

        correct_option_number = self.get_option_number(question.correct_option)

        self.cursor1.execute(
            "INSERT INTO questions (question, option1, option2, option3, option4, correct_option, exam_time, is_navigation_enabled) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (question.question, question.option1, question.option2, question.option3,
             question.option4, correct_option_number, question.exam_time, question.navigation_enabled)
        )
        self.db.commit()
        self.disconnect()

    def edit(self, question):
        self.connect()
        correct_option_number = self.get_option_number(question.correct_option)
        self.cursor1.execute(
            """UPDATE questions 
            SET question=%s, option1=%s, option2=%s, option3=%s, option4=%s, 
                correct_option=%s, exam_time=%s, is_navigation_enabled=%s
            WHERE id=%s""",
            [question.question, question.option1, question.option2, question.option3,
             question.option4, correct_option_number, question.exam_time, question.navigation_enabled, question.id]
        )
        self.db.commit()
        self.disconnect()

    def reorder_ids(self):
        self.connect()
        try:
            self.cursor1.execute("SET @count = 0")
            self.cursor1.execute("UPDATE questions SET id = @count := @count + 1")
            self.cursor1.execute("ALTER TABLE questions AUTO_INCREMENT = 1")
            self.db.commit()
        except Exception as e:
            print(f"Error in reorder_ids: {e}")
            self.db.rollback()
        finally:
            self.disconnect()

    def remove(self, id):
        self.connect()
        self.cursor1.execute("DELETE FROM questions WHERE id=%s", [id])
        self.db.commit()
        self.disconnect()
        self.reorder_ids()

    def find_all(self):
        self.connect()
        self.cursor1.execute("SELECT * FROM questions")
        questions_list = self.cursor1.fetchall()
        self.disconnect()
        updated_questions = []
        for question in questions_list:
            try:
                correct_option_value = int(question[6])
            except (ValueError, TypeError):
                correct_option_value = question[6]
            updated_question = list(question)
            updated_question[6] = correct_option_value
            updated_questions.append(updated_question)
        return updated_questions

    def find_one(self, id):
        self.connect()
        self.cursor1.execute("SELECT * FROM questions WHERE id=%s", [id])
        question = self.cursor1.fetchone()
        self.disconnect()
        if question:
            try:
                correct_option_value = int(question[6])
            except (ValueError, TypeError):
                correct_option_value = question[6]
            question = list(question)
            question[6] = correct_option_value
        return question

    def find_by_question(self, question_text):
        self.connect()
        self.cursor1.execute("SELECT * FROM questions WHERE question=%s", [question_text])
        question = self.cursor1.fetchone()
        self.disconnect()
        return question
