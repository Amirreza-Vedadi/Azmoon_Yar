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

    def save(self, question):
        self.connect()
        self.cursor1.execute(
            "INSERT INTO questions (question, option1, option2, option3, option4, correct_option, exam_time, is_navigation_enabled) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (question.question, question.option1, question.option2, question.option3,
             question.option4, question.correct_option, question.exam_time, question.navigation_enabled)
        )
        self.db.commit()
        self.disconnect()

    def edit(self, question):
        self.connect()
        self.cursor1.execute(
            """UPDATE questions 
            SET question=%s, option1=%s, option2=%s, option3=%s, option4=%s, 
                correct_option=%s, exam_time=%s, is_navigation_enabled=%s
            WHERE id=%s""",
            [question.question, question.option1, question.option2, question.option3,
             question.option4, question.correct_option, question.exam_time, question.navigation_enabled, question.id]
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
        return questions_list

    def find_one(self, id):
        self.connect()
        self.cursor1.execute("SELECT * FROM questions WHERE id=%s", [id])
        question = self.cursor1.fetchone()
        self.disconnect()
        return question

    def find_by_question(self, question_text):
        self.connect()
        self.cursor1.execute("SELECT * FROM questions WHERE question=%s", [question_text])
        question = self.cursor1.fetchone()
        self.disconnect()
        return question

