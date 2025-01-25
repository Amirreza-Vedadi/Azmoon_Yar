from model.entity.questions import Questions
from model.da.questions_da import QuestionsDA
import re

class QuestionsController:
    def is_valid_exam_time(self, exam_time):
        return re.fullmatch(r'\d+', exam_time)

    def save(self, question, option1, option2, option3, option4, correct_option, exam_time, navigation_enabled):
        if not question or not option1 or not correct_option or not exam_time:
            return {"status": "error", "message": "لطفاً تمام فیلدهای ضروری را پر کنید"}

        if not self.is_valid_exam_time(exam_time):
            return {"status": "error", "message": "زمان امتحان باید یک عدد مثبت باشد"}

        q_da = QuestionsDA()
        existing_question = q_da.find_by_question(question)
        if existing_question:
            return {"status": "error", "message": "این سوال قبلاً ثبت شده است"}

        try:
            question_obj = Questions(None, question, option1, option2, option3, option4, correct_option, exam_time,
                                     navigation_enabled)
            q_da.save(question_obj)
            return {"status": "success", "message": "سوال با موفقیت ذخیره شد"}
        except Exception as e:
            return {"status": "error", "message": f"خطا در ذخیره سوال: {str(e)}"}

    def edit(self, id, question, option1, option2, option3, option4, correct_option, exam_time, navigation_enabled):
        if not self.is_valid_exam_time(exam_time):
            return {"status": "error", "message": "زمان امتحان باید عدد باشد"}

        if not str(id).isdigit():
            return {"status": "error", "message": "ID باید عدد باشد"}

        try:
            question_obj = Questions(id, question, option1, option2, option3, option4, correct_option, exam_time,
                                     navigation_enabled)
            q_da = QuestionsDA()
            q_da.edit(question_obj)
            return {"status": "success", "message": "سوال با موفقیت ویرایش شد"}
        except Exception as e:
            return {"status": "error", "message": f"خطا در ویرایش سوال: {str(e)}"}

    def remove(self, id):
        if not str(id).isdigit():
            return {"status": "error", "message": "ID باید عدد باشد"}

        try:
            q_da = QuestionsDA()
            q_da.remove(id)
            return {"status": "success", "message": "سوال با موفقیت حذف شد"}
        except Exception as e:
            return {"status": "error", "message": f"خطا در حذف سوال: {str(e)}"}

    def search(self, id):
        if not str(id).isdigit():
            return {"status": "error", "message": "ID باید عدد باشد"}

        q_da = QuestionsDA()
        question = q_da.find_one(id)
        if question:
            return question
        return {"status": "error", "message": "سوال پیدا نشد"}

    def find_all(self):
        q_da = QuestionsDA()
        return q_da.find_all()
