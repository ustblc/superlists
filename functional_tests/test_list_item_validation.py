from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # lc访问首页，不小心提交了一个空的待办事项
        # 输入框没有输入内容，他就按下了回车键
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # 首页刷新了，显示一个错误信息
        # 提示待办事项不能为空
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You can't have an empty list item",
            )
        )

        # 他输入了一些文字，然后再次提交，这次没问题了
        self.browser.find_element_by_id("id_new_item").send_keys("Learn TDD")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Learn TDD")

        # 他有点调皮，又提交了一个空的待办事项
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        # 在清单页面他看到了一个类似的错误信息
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You can't have an empty list item",
            )
        )

        # 输入问题之后就没问题了
        self.browser.find_element_by_id("id_new_item").send_keys("Refactoring code")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Learn TDD")
        self.wait_for_row_in_list_table("2: Refactoring code")
