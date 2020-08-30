from selenium import webdriver
import unittest


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
        self.fail("finish the test")

        # 应用邀请他输入一个代办事项

        # 他在文本框输入了"learn django-TDD"

        # 然后他按回车键后，页面更新了
        # 待办事项表格中显示了"1：learn django-TDD"

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了"complete water-sword project"

        # 页面再次更新，他的清单中显示了这两个待办事项

        # lc想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 他访问这个URL，发现他的待办事项还在
        # 他很满意，他继续学习去了

        browser.quit()


if __name__ == "__main__":
    unittest.main()
