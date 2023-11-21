from selenium.webdriver.common.by import By
import re
# turbo-setup-menu__top

"top", "main"


class WMTableManager:
    def __init__(self, driver) -> None:
        self.driver = driver

    def collect_menu(self, type,  project, origin_link):
        """
        type can be "top" or "main"
        """
        self.driver.get(origin_link)
        self.__collect_menu_inputs(type, project)

    def __collect_menu_inputs(self, type, project):
        inputs_xpath = f"//div[@class='turbo-setup-menu__{type}']//input"
        result_file_path = f"tables/menu_structure_{type}_{project}.txt"

        inputs = self.driver.find_elements(By.XPATH, inputs_xpath)
        for input in inputs:
            value = input.get_attribute("value")
            with open(result_file_path, "a", encoding="UTF-8") as table_file:
                table_file.write(value + '\n')

    def input_values_in_menus(self, type, project, site):
        inputs_xpath = f"//div[@class='turbo-setup-menu__{type}']//input"
        result_file_path = f"tables/menu_structure_{type}_{project}.txt"

        with open(result_file_path, "r", encoding="UTF-8") as table_file:
            values = table_file.readlines()

        inputs = self.driver.find_elements(By.XPATH, inputs_xpath)

        for i in range(len(values)):
            input_value = values[i]
            if (re.match(r'https:\/\/.+[.][a-z]+', values[i])):
                site_uri = re.sub(
                    r'https:\/\/.+[.][a-z]+', "", values[i])
                input_value = f"{site}{site_uri}"

    def create_table_level(self):
        


    def create_table_old(self):
        self.sm.driver.get(
            "https://webmaster.yandex.ru/site/https:abakan.neoplus-clinic.ru:443/turbo/settings/menu/")

        add_lvl_1_btn = self.sm.driver.find_element(
            By.XPATH, "//button[@class='button button_size_s button_menu-level_1 button_theme_normal sun-table__turbo-setup-menu-add i-bem']")

        for i in range(3):
            add_lvl_1_btn.click()

        for n in range(3):

            amount_of_lvl_2 = [8, 15, 5]
            amount_of_lvl_3 = [[1, 11], [2], []]
            numbers_lvl_3 = [[1, 2], [2], []]
            lvl_1 = self.sm.driver.find_element(
                By.XPATH, f"//tr[@class='sun-table__row sun-table__row_menu-level_1'][{n+1}]")
            lvl_1.find_element(By.XPATH, f"./td[2]/span").click()
            add_lvl_2_btn = lvl_1.find_element(
                By.XPATH, ".//button[@class='button button_size_s button_menu-level_2 button_theme_normal sun-table__turbo-setup-menu-add i-bem']")

            for j in range(amount_of_lvl_2[n]-1):
                add_lvl_2_btn.click()

            expand_lvl_3_btns = lvl_1.find_elements(
                By.XPATH, f".//span[@class='link link_pseudo_yes link_theme_normal link_menu-level_2 sun-table__turbo-setup-submenu-add i-bem']")

            for el in numbers_lvl_3[n]:
                if len(numbers_lvl_3) == 0:
                    break
                expand_lvl_3_btns[el].click()

            add_lvl_3_btns = lvl_1.find_elements(
                By.XPATH, ".//button[@class='button button_size_s button_menu-level_3 button_theme_normal sun-table__turbo-setup-menu-add i-bem']")

            for k in range(len(numbers_lvl_3[n])):
                print(f"n = {n}, k = {k}")
                for lvl3_num in range(amount_of_lvl_3[n][k]-1):
                    add_lvl_3_btns[k].click()


    # def input_values_to_table(self, row_id, names, domens):
    #     inputs = self.sm.driver.find_elements(By.XPATH, "//div[@class='turbo-setup-menu__main']//input")
    #     #ссылки четные, имена - нечетные
    #     city_link = self.gs.read_cell(f"B{row_id}")

    #     links = []
    #     for domen in domens:
    #         links.append(city_link + domen[0])
    #     for i in range (len(inputs)//2):
    #         #all numbers reversed
    #         input_even_number = 2 * i + 1
    #         inputs[input_even_number].click()
    #         inputs[input_even_number].clear()
    #         inputs[input_even_number].send_keys(links[i])
    #         input_odd_number = 2 * i
    #         inputs[input_odd_number].click()
    #         inputs[input_odd_number].clear()
    #         inputs[input_odd_number].send_keys(names[i])

    #     save_btn = self.sm.driver.find_element(By.XPATH, "button button_size_m button_theme_action button_align_left form__submit form__submit_align_left i-bem")
    #     save_btn.click()

    