from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStyingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # lc访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(2560, 1440)

        # 他看到输入框完美的居中显示
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            1280,
            delta=10
        )

        # 他新建了一个清单，看到输入框完美的居中显示
        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            1280,
            delta=10
        )
