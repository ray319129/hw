from selenium import webdriver # 控制瀏覽器
from selenium.webdriver.common.by import By # 指定搜尋網頁元素
from selenium.webdriver.support.ui import WebDriverWait # 等待網頁元素出現
from selenium.webdriver.support import expected_conditions as EC # 判斷網頁元素是否可被操作


class AdidasBot:
    def __init__(self):
        """建立瀏覽器與等待工具。"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)


    def open_website(self):
        """開啟 Adidas 台灣官網首頁。"""
        self.driver.get("https://www.adidas.com.tw/")


    def enter_keyword(self, keyword):
        """找到搜尋框並輸入關鍵字。"""
        search_box = self.wait.until(
            EC.element_to_be_clickable( # 等待搜尋框可被點擊
                (By.CSS_SELECTOR, "input#ns-search-input") # Adidas 搜尋框的 id
            )
        )
        search_box.clear()
        search_box.send_keys(keyword)


    def click_search(self):
        """點擊搜尋框旁的放大鏡按鈕。"""
        search_button = self.wait.until(
            EC.element_to_be_clickable(
                # Adidas 搜尋按鈕的 CSS 選擇器
                (By.CSS_SELECTOR, "a.ns-search-btn")
            )
        )
        search_button.click()


    def show_results(self, limit=10):
        """等待搜尋結果出現，並在終端機列出商品名稱與價格。"""
        self.wait.until(EC.url_contains("/Search"))
        cards = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.product-card__vertical") # 每個商品卡片
            )
        )
        print(f"\n搜尋結果網址：{self.driver.current_url}")
        print(f"共找到 {len(cards)} 件商品，列出前 {min(limit, len(cards))} 件：")
        for i, card in enumerate(cards[:limit], start=1):
            lines = [line.strip() for line in card.text.split("\n") if line.strip()]
            # 商品名稱在分類（例如「男/女,潮流」）的上一行，價格以 NT$ 開頭
            name = next((lines[j - 1] for j, line in enumerate(lines) if "," in line and j > 0), lines[0] if lines else "")
            prices = [line for line in lines if line.startswith("NT$")]
            print(f"{i}. {name}  {' → '.join(prices)}")


    def close(self):
        """關閉瀏覽器。"""
        self.driver.quit()


def main():
    bot = AdidasBot()

    try:
        bot.open_website()
        input("請先關閉網頁上的廣告視窗，再回終端機按 Enter……")
        keyword = input("請輸入搜尋關鍵字：")
        bot.enter_keyword(keyword)
        bot.click_search()
        bot.show_results()

        input(f"\n確認已搜尋「{keyword}」並顯示結果，按 Enter 關閉……")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
