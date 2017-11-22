from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time
import sys

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def stale_aware_for_action(self, action):
        while(True):
            try:
                action()
                break
            except StaleElementReferenceException:
                continue

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 伊迪丝听说有一个很酷的在线代办事项应用
        # 她去看了这个应用的首页
        self.browser.get(self.server_url)

        # 她注意到网页的标题和头部都包含“TO-DO”这个词
        #assert 'To-Do' in browser.title, "Browser title was" + browser.title

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        

        # 应用邀请她输入一个代办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 她在一个文本框中输入了“Buy peacock feathers”(购买孔雀羽毛)
        # 伊迪丝的爱好是使用假蝇做饵钓鱼
        inputbox.click()
        inputbox.send_keys('Buy peacock feathers' + Keys.ENTER)

        # 她按回车键后，被带到了一个新url
        # 这个页面的代办事项清单中显示了“1: Buy peacock feathers”
        time.sleep(0.5)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        def cherk_for_row_in_list_table():
            self.check_for_row_in_list_table('1:Buy peacock feathers')
        self.stale_aware_for_action(cherk_for_row_in_list_table)

        # 页面中又显示了一个文本框，可以输入其他的代办事项
        # 她输入了“Use peacock feathers to make a fly”使用孔雀羽毛做假蝇
        # 伊迪丝做事情很有条理
        def insert_second_item_to_inputbox():
            inputbox = self.browser.find_element_by_id('id_new_item')
            inputbox.send_keys('Use peacock feathers to make a fly' + Keys.ENTER)
        self.stale_aware_for_action(insert_second_item_to_inputbox)


        # 页面再次更新，她的页面中添加了这两个代办事项
        def check_for_first_item():
            self.check_for_row_in_list_table('1:Buy peacock feathers')
        def check_for_second_item():
            self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
        self.stale_aware_for_action(check_for_first_item)
        self.stale_aware_for_action(check_for_second_item)
        
        # 现在一个叫做佛朗西斯的新用户访问了网站

        ## 我们使用一个新浏览器会话
        ## 确保伊迪丝的信息不会从cookie中泄漏出来
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

        # 佛朗西斯访问首页
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 佛朗西斯输入一个新代办事项，新建一个清单
        # 他不像伊迪丝那样兴趣昂然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 佛朗西斯获得了他的唯一URL
        time.sleep(0.1)
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # 两人都很满意，去睡觉了
    def test_layout_and_styling(self):
        # 伊迪丝访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 他看到输入框完美的居中显示

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # 她新建了一个清单，看到输入框仍完美的居中显示。
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )





















