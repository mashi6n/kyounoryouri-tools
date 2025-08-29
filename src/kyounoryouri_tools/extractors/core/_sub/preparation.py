from bs4 import Tag

from kyounoryouri_tools.extractors.utils import get_next_sibling
from kyounoryouri_tools.models import Step, TitledStep


def extract_preparation(preprocess_header: Tag) -> list[TitledStep]:
    """
    Extract preparation steps from the page

    Args:
        preprocess_header (Tag): Tag object of preparation header

    Returns:
        list[TitledStep]: list of preparation steps

    """
    pre_steps = []
    s = get_next_sibling(preprocess_header)
    while s is not None:
        s_class = s.get("class")

        if s.name == "div" and s_class is not None and "detail-sub-ttl" in s_class:
            pre_steps.append(TitledStep(title=s.get_text(strip=True), steps=[]))

        elif s.name == "p":
            if len(pre_steps) == 0:
                pre_steps.append(TitledStep(title="", steps=[]))

            step_number_tag = s.find("span")

            if not isinstance(step_number_tag, Tag):
                err = "failed to extract step number"
                raise ValueError(err)

            step_number = int(step_number_tag.get_text(strip=True))
            step_number_tag.decompose()

            desc = s.get_text(strip=True)

            next_s = get_next_sibling(s)
            point = ""
            if next_s is not None and next_s.name == "div":
                next_s_class = next_s.get("class")
                if next_s_class is not None and "detail-sub-point" in next_s_class:
                    next_s.select("p")[0].decompose()
                    point = next_s.get_text(strip=True)
                    s = next_s

            pre_steps[-1].steps.append(Step(step_num=step_number, desc=desc, point=point))

        s = get_next_sibling(s)
    return pre_steps
