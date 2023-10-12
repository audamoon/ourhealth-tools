import re


class ProfileID:
    """
    List of account ids
    """
    DEFAULT = ""
    FIRST = "Profile 1"
    SECOND = "Profile 2"
    THIRD = "Profile 3"
    FORTH = "Profile 4"

    def get_ids() -> list:
        """
        Return all names of ProfileID class
        """
        all_ids = []
        all_attr = ProfileID.__dict__.keys()

        for attr in all_attr:
            if re.match(r'([A-Z]{3,})',attr):
                all_ids.append(attr)

        return all_ids
    