#通用账号\IP封禁对抗

#1. 请求头模拟与轮换
import random
import requests

user_agents = [
    "Mozilla/5.0 XXXXXXX",
    "Mozilla/5.0 XXXXXX",
    "Mozilla/5.0 XXXXXX"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.XXX.com/"
}

#2. 请求频率控制
import time
from random import uniform

def controlled_request(url):
    time.sleep(uniform(1, 3))  # 随机延迟1-3秒
    response = requests.get(url, headers=headers)
    return response


#3. 代理IP池实现
import random

proxy_pool = [
    "http://user:pass@XXX:port",
    "http://user:pass@XXX:port",
    # 多准备高质量代理
]

def get_with_proxy(url):
    proxy = {"https": random.choice(proxy_pool)}
    try:
        return requests.get(url, proxies=proxy, timeout=10)
    except:
        return None  # 实现自动重试机制

#4. 混合代理策略
def smart_request(url, max_retry=3):
    for _ in range(max_retry):
        # 按比例使用不同代理类型
        if random.random() < 0.7:  # 70%几率用数据中心IP
            proxy = datacenter_proxies.get_random()
        else:  # 30%几率用住宅IP
            proxy = residential_proxies.get_random()
        
        try:
            return requests.get(url, proxies=proxy)
        except:
            continue
    raise Exception("All proxies failed")


#5. 多账号轮换系统
accounts = [
    {"user": "user1", "token": "token1"},
    {"user": "user2", "token": "token2"}
]

current_account = 0

def get_active_account():
    global current_account
    account = accounts[current_account]
    current_account = (current_account + 1) % len(accounts)
    return account

#6. 账号行为模拟
def simulate_human_behavior(driver):
    # 随机鼠标移动
    action = webdriver.ActionChains(driver)
    action.move_by_offset(random.randint(5, 15), random.randint(5, 15))
    action.perform()
    
    # 随机滚动
    scroll_px = random.randint(200, 800)
    driver.execute_script(f"window.scrollBy(0, {scroll_px})")
    time.sleep(uniform(0.5, 1.5))


#7. 浏览器指纹管理
from selenium.webdriver import ChromeOptions

options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# 修改WebDriver属性
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        """
    }
)

#8. TLS指纹绕过
# 使用curl_cffi库绕过TLS指纹检测
from curl_cffi import requests as c_requests

response = c_requests.get(
    "https://target.com",
    impersonate="chrome110"  # 模拟Chrome指纹
)


#9. 自动验证码处理
# 使用2Captcha服务
import requests

def solve_recaptcha(site_key, page_url):
    api_key = "YOUR_2CAPTCHA_KEY"
    res = requests.post(
        f"http://2captcha.com/in.php?key={api_key}",
        data={
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": page_url
        }
    )
    if res.text.startswith("OK"):
        captcha_id = res.text.split("|")[1]
        for _ in range(20):  # 最多尝试20次
            time.sleep(5)
            result = requests.get(
                f"http://2captcha.com/res.php?key={api_key}"
                f"&action=get&id={captcha_id}"
            )
            if result.text == "CAPCHA_NOT_READY":
                continue
            return result.text.split("|")[1]
    return None

#10. 请求模式随机化
def random_request_sequence(urls):
    random.shuffle(urls)  # 随机打乱请求顺序
    for url in urls:
        wait_time = random.expovariate(1/2)  # 指数分布延迟
        time.sleep(max(1, min(wait_time, 5)))  # 限制在1-5秒之间
        make_request(url)

#11. 流量特征混淆
def add_noise_to_headers(base_headers):
    noise_headers = {
        "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Accept-Encoding": "gzip, deflate, br"
    }
    return {**base_headers, **noise_headers}


#12. 封禁检测机制
def is_blocked(response):
    blocked_signals = [
        response.status_code in [403, 429],
        "captcha" in response.text.lower(),
        "access denied" in response.text.lower(),
        len(response.content) < 500  # 异常小的响应
    ]
    return any(blocked_signals)

def safe_request(url):
    response = requests.get(url)
    if is_blocked(response):
        handle_block_case()  # 触发封禁处理流程
    return response

#13. 自适应调节系统
class AdaptiveCrawler:
    def __init__(self):
        self.request_interval = 3  # 初始间隔
        self.failure_count = 0
    
    def adjust_speed(self, success):
        if success:
            self.failure_count = max(0, self.failure_count-1)
            # 成功时缓慢加速
            self.request_interval = max(1, self.request_interval*0.9)
        else:
            self.failure_count += 1
            # 失败时指数退避
            self.request_interval = min(60, self.request_interval*(1.5**self.failure_count))
