from PyQt5.QtWidgets import QTreeWidgetItem


class FinalExamItem(QTreeWidgetItem):
    def __init__(self, data, final_exam):
        super().__init__(data)
        self.final_exam = final_exam
