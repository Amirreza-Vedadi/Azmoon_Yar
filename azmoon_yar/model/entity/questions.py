class Questions:
    def __init__(self, id, question, option1, option2, option3, option4, correct_option, exam_time, navigation_enabled=0):
        self.id = id
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.correct_option = correct_option
        self.exam_time = exam_time
        self.navigation_enabled = navigation_enabled
