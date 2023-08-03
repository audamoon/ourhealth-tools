xpath = "/parent::li/ul/li"
if xpath == "":
        xpath = f"//img[@alt='Раскрыть список']"
else:
    xpath = xpath + f"/img[@alt='Раскрыть список']"

print(xpath)