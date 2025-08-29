from pydantic import BaseModel


class Step(BaseModel):
    """
    Step correspods to a single step in a recipe instruction or preparation.

    Fields:
        step_num (int): step number.
        desc (str): description of the step.
        point (str): tip, hint, or note for the step.
    """

    step_num: int
    desc: str
    point: str

    def __str__(self) -> str:
        if self.point == "":
            return f"{self.step_num}: {self.desc}"
        return f"{self.step_num}: {self.desc}  [[!{self.point}]]"
