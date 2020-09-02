from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # lc 听说有一个很酷的在线代办事项应用
        # 他去看了这个应用的首页
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table("1:Learn django-TDD")

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了"Complete water-sword project"
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Complete water-sword project")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面再次更新，他的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table("2:Complete water-sword project")
        self.wait_for_row_in_list_table("1:Learn django-TDD")

        # 他很满意，他继续学习去了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # lc新建了一个待办事项清单
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Learn django-TDD")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:Learn django-TDD")

        # 他注意到清单有唯一的url
        lc_list_url = self.browser.current_url
        self.assertRegex(lc_list_url, "lists/.+")

        # 现在一个名叫lemon的新用户访问了网站
        # 我们使用了一个新浏览器会话
        # 确保lc的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # lemon 访问首页
        # 页面中是看不到lc的待办清单的
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name("body").text
        self.assertNotIn("Learn django-TDD", page_text)
        self.assertNotIn("water-sword project", page_text)

        # lemon输入了一个新的待办事项，新建一个清单
        # 他不像lc那样好学
        input_box.send_keys("play computer")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:play computer")

        # lemon获得了他的唯一的url
        lemon_list_url = self.browser.current_url
        self.assertRegex(lemon_list_url, "lists/.+")
        self.assertNotEqual(lemon_list_url, lc_list_url)

        # 这个页面还是没有lc的清单
        page_text = self.browser.page_text = self.browser.find_elements_by_tag_name("body").text
        self.assertNotIn("Learn django-TDD", page_text)
        self.assertIn("play computer", page_text)

        # 他们俩都很满意，然后lc又去学习去了
