from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # lc 听说有一个很酷的在线代办事项应用
        # 他去看了这个应用的首页
        self.browser.get("http://localhost:8000")

        # 他注意到了网页的标题和头部都包含"To-Do"这个词
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # 应用邀请他输入一个代办事项
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            "Enter a to-do item"
        )

        # 他在文本框输入了"Learn django-TDD"
        input_box.send_keys("Learn django-TDD")

        # 然后他按回车键后，页面更新了
        # 待办事项表格中显示了"1:Learn django-TDD"
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了"Complete water-sword project"
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Complete water-sword project")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面再次更新，他的清单中显示了这两个待办事项
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn("1:Learn django-TDD", [row.text for row in rows])
        self.assertIn("2:Complete water-sword project", [row.text for row in rows])

        # lc想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能
        self.fail("finish the test")

        # 他访问这个URL，发现他的待办事项还在
        # 他很满意，他继续学习去了

        browser.quit()


if __name__ == "__main__":
    unittest.main()
