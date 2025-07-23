import os
import pickle

from app.schemas import Evaluation, EvaluationUpdate

def get_evaluation_crud():
    return evaluation_crud

class CRUDEvaluation:
    def __init__(self, evaluation_file_path: str = "evaluation_history.pkl"):
        self.evaluation_history: list[Evaluation] = []
        self.read_evaluation_history_from_file(evaluation_file_path)
        self.evaluation_file_path = evaluation_file_path

    def read_evaluation_history_from_file(self, file_path: str = None) -> None:
        if file_path is None:
            file_path = self.evaluation_file_path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.evaluation_history = pickle.load(file)
        return

    def write_evaluation_history_to_file(self, file_path: str = None) -> None:
        if file_path is None:
            file_path = self.evaluation_file_path
        with open(file_path, "wb") as f:
            pickle.dump(self.evaluation_history, f)
        return

    def get_evaluation_history(self) -> list[Evaluation] | None:
        return self.evaluation_history

    def append_evaluation_history(self, evaluation: Evaluation) -> None:
        self.evaluation_history.append(evaluation)
        self.write_evaluation_history_to_file()
        return

    def update_evaluation(self, index: int, update_data: EvaluationUpdate) -> None:
        if 0 <= index < len(self.evaluation_history):
            evaluation = self.evaluation_history[index]
            update_dict = update_data.dict(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(evaluation, key, value)
            self.write_evaluation_history_to_file()
        return

    def delete_evaluation(self, index: int) -> None:
        if 0 <= index < len(self.evaluation_history):
            del self.evaluation_history[index]
            self.write_evaluation_history_to_file()
        return

evaluation_crud = CRUDEvaluation()