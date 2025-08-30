from pathlib import Path
import xmltodict

from kyounoryouri_tools.models import Urlset


def get_urlset(xml_source: Path) -> Urlset | None:
    """
    Get urlset from xml file

    Args:
        xml_source (Path | str): path or url to xml file

    Returns:
        Urlset | None: urlset, None if xml_source is invalid

    """
    if not xml_source.exists():
        print(f"{xml_source} does not exist.")
        return Urlset(url=[])

    xmldict = xmltodict.parse(xml_source.read_text())
    urlset_dict = xmldict["urlset"]

    return Urlset.model_validate(urlset_dict)
