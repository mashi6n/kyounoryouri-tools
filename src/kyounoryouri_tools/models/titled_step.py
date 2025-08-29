from pydantic import BaseModel

from .step import Step


class TitledStep(BaseModel):
    """
    TitledStep corresponds to a section of a recipe instruction or preparation.

    Fields:
        title (str): title of the section. section may not have a title.
        steps (list[Step]): steps in the section.
    """

    title: str
    steps: list[Step]

    def __str__(self) -> str:
        s = self.title + "\n"
        for step in self.steps:
            s += f"  {step}\n"
        return s

    def get_list_str_wo_title(
        self, remove_stepref_marker: bool, assign_step_number: bool
    ) -> list[str]:
        step_list = []
        for step in self.steps:
            if assign_step_number:
                if remove_stepref_marker:
                    step_list.append(f"{step.step_num}. {step.desc.replace('__', '')}".strip())
                else:
                    step_list.append(f"{step.step_num}. {step.desc}".strip())
            else:
                if remove_stepref_marker:
                    step_list.append(step.desc.replace("__", "").strip())
                else:
                    step_list.append(step.desc.strip())
        return step_list
