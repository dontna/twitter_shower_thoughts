import selenium.webdriver
import time
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TwitterBoi:
    def __init__(self, post=True):
        self.bot = selenium.webdriver.Firefox(executable_path='geckodriver path here')
        self.login_to_twitter()
        if post:
            self.post_tweet()
        else:
            self.bot_like_posts('showerthoughts')
        self.bot_finished()

    def login_to_twitter(self):
        self.bot.get('https://twitter.com/login')

        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="session[username_or_email]"]')))

        userfield = self.bot.find_element(By.XPATH, '//input[@name="session[username_or_email]"]')
        passfield = self.bot.find_element(By.XPATH, '//input[@name="session[password]"]')

        userfield.send_keys("username here")
        passfield.send_keys("password here")
        time.sleep(0.3)
        passfield.send_keys(Keys.RETURN)

        try:
            WebDriverWait(self.bot, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div')))
        except:
            userfield = self.bot.find_element(By.XPATH, '//input[@name="session[username_or_email]"]')
            passfield = self.bot.find_element(By.XPATH, '//input[@name="session[password]"]')
            userfield.send_keys("username here")
            passfield.send_keys("password here")
            time.sleep(0.3)
            passfield.send_keys(Keys.RETURN)    
            WebDriverWait(self.bot, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div')))

    def post_tweet(self):
        quote_to_post = self.get_shower_thought()

        self.bot.switch_to.window(self.bot.window_handles[0])

        tweet_box = self.bot.find_element(By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div')
        tweet_box.send_keys(quote_to_post)
        
        tweet_button = self.bot.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]').click()

    def get_shower_thought(self):
        time.sleep(1)
        self.bot.execute_script('window.open()')
        self.bot.switch_to.window(self.bot.window_handles[-1])
        self.bot.get('https://www.reddit.com/r/Showerthoughts/top/')

        WebDriverWait(self.bot,10).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), \'Showerthoughts\')]')))

        top_post = self.bot.execute_script('return document.querySelector(\'div div a div h3\').textContent')
        return top_post

    def bot_like_posts(self, hashtag):
        self.bot.get(f'https://twitter.com/search?q=%23{hashtag}&src=typeahead_click&f=live')

        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.r-1ljd8xs > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > section:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > article:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2)')))
        print("Found posts, moving on.")
        time.sleep(2)

        for _ in range(3):
            print(f"{_} iteration")
            time.sleep(5)
            posts = self.bot.find_elements(By.CSS_SELECTOR, 'div[data-testid="like"] div div div')
            print(f"found {len(posts)} posts.")
            if not len(posts) < 5:
                try:
                    print("trying to like the posts.")
                    self.bot.execute_script('document.querySelectorAll(\'div[data-testid="like"] div div div\').forEach((x) => x.click())')
                except:
                    print("Already liked these posts")
            else:
                print("no posts found")
            self.bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)

    def bot_finished(self):
        print("Finished, now exiting.")
        self.bot.quit()

if __name__ == '__main__':
    bot = TwitterBoi()