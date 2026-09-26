# POM Design

## 1. Mục đích

Page Object Model (POM) được sử dụng để tách biệt:

- Chi tiết giao diện và locator.
- Hành vi/thao tác trên trang.
- Logic điều phối test.
- Keyword trong Keyword Library.

Mỗi trang hoặc thành phần UI chính được biểu diễn bởi một Page Object riêng.

Ví dụ:

```text
pages/
├── base_page.py
├── login_page.py
├── home_page.py
├── search_page.py
├── product_page.py
└── cart_page.py
```

---

## 2. Nguyên tắc POM

### 2.1 Mỗi Page Object đại diện cho một trang/chức năng UI

Ví dụ:

```text
LoginPage
HomePage
ProductPage
CartPage
```

### 2.2 Locator thuộc Page Object

Locator không được đặt trong:

- Excel.
- Keyword Library.
- Keyword Executor.

### 2.3 Page Object nhận WebDriver từ bên ngoài

Page Object không tự khởi tạo browser.

Thiết kế:

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
```

WebDriver được khởi tạo bởi Core/DriverManager và được truyền vào Page Object.

---

## 3. BasePage

`BasePage` chứa các thao tác UI dùng chung cho nhiều Page Object.

File:

```text
pages/base_page.py
```

Các nhóm chức năng chính:

| Method | Mục đích |
|---|---|
| `click()` | Click element |
| `enter_text()` | Nhập text |
| `clear()` | Xóa nội dung |
| `get_text()` | Lấy text |
| `is_visible()` | Kiểm tra element hiển thị |
| `wait_for_element()` | Chờ element sẵn sàng |
| `get_current_url()` | Lấy URL hiện tại |

BasePage không chứa locator của một trang cụ thể.

---

## 4. Locator Convention

Locator được khai báo tập trung trong Page Object bằng dictionary `LOCATORS`.

Mỗi entry có dạng:

```python
"element_name": (By.<STRATEGY>, "<value>")
```

Ví dụ:

```python
LOCATORS = {
    "username_field": (By.ID, "username"),
    "password_field": (By.ID, "password"),
    "login_button": (By.CSS_SELECTOR, "button[type='submit']"),
}
```

Cấu trúc:

```text
element_name
      ↓
(By strategy, locator value)
```

Ví dụ:

```text
username_field
      ↓
(By.ID, "username")
```

---

## 5. Quy tắc đặt tên element

Tên element phải mô tả ý nghĩa nghiệp vụ/UI.

### Nên dùng

```text
username_field
password_field
login_button
error_message
search_box
product_title
add_to_cart_button
```

### Không nên dùng

```text
xpath_01
id_username
button_1
element_2
css_selector_login
```

Mục tiêu là khi locator thay đổi, tên logical element và test case vẫn có thể giữ nguyên.

---

## 6. LoginPage

File:

```text
pages/login_page.py
```

Cấu trúc:

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    LOCATORS = {
        "username_field": (By.ID, "username"),
        "password_field": (By.ID, "password"),
        "login_button": (By.CSS_SELECTOR, "button[type='submit']"),
        "error_message": (By.CSS_SELECTOR, ".error-message"),
    }

    def __init__(self, driver):
        super().__init__(driver)
```

Các locator này chỉ là ví dụ thiết kế; locator thực tế phụ thuộc website được kiểm thử.

---

## 7. BasePage và Page Object

Quan hệ:

```text
BasePage
   ↑
   │ inherits
   │
LoginPage
HomePage
ProductPage
CartPage
```

BasePage cung cấp thao tác dùng chung.

Page Object cung cấp:

- Locator của trang.
- Các hành vi đặc thù của trang nếu cần.

---

## 8. Không để locator trong Keyword

Không thiết kế:

```python
def click_login(driver):
    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()
```

trong Keyword Library.

Thay vào đó:

```text
CLICK
  ↓
LoginPage.login_button
  ↓
POM
  ↓
LOCATORS["login_button"]
  ↓
Selenium
```

Keyword chỉ biết logical target.

---

## 9. Target Convention

Target có format:

```text
<PageObject>.<element>
```

Ví dụ:

```text
LoginPage.username_field
LoginPage.password_field
LoginPage.login_button
LoginPage.error_message
```

Target được dùng trong Excel:

| Keyword | Target | Data | Expected |
|---|---|---|---|
| `ENTER_TEXT` | `LoginPage.username_field` | `admin` | |
| `ENTER_TEXT` | `LoginPage.password_field` | `123456` | |
| `CLICK` | `LoginPage.login_button` | | |
| `VERIFY_ERROR` | `LoginPage.error_message` | | `Invalid username or password` |

---

## 10. Target Resolution

Framework cần phân tách:

```text
Page Name
Element Name
```

Ví dụ:

```text
LoginPage.username_field
│        │
│        └── element name
└─────────── page object
```

Sau đó:

```text
LoginPage
    ↓
LoginPage.LOCATORS
    ↓
"username_field"
    ↓
(By.ID, "username")
```

---

## 11. Locator Access

Một cách triển khai thống nhất là BasePage cung cấp helper để lấy element theo logical key.

Khái niệm:

```python
def find(self, locator):
    return self.driver.find_element(*locator)
```

Sau đó Page Object/Keyword Layer sử dụng locator đã được Page Object quản lý.

Framework không đưa locator kỹ thuật ra Excel.

---

## 12. WebDriverWait

POM/BasePage chịu trách nhiệm xử lý đồng bộ hóa UI.

Không sử dụng:

```python
time.sleep(5)
```

làm cơ chế chờ chính.

Thay vào đó sử dụng explicit wait:

```text
WebDriverWait
    ↓
element condition
    ↓
element ready
    ↓
interaction
```

Các helper có thể bao gồm:

```text
wait_for_element()
wait_for_element_visible()
wait_for_element_clickable()
```

Điều này giúp giảm vấn đề timing/flaky test.

---

## 13. Page Object không quản lý Test Flow

Page Object không quyết định:

```text
Step 1
Step 2
Step 3
```

và không đọc Excel.

Page Object chỉ cung cấp UI abstraction.

Luồng điều phối nằm ở:

```text
TestExecutor
KeywordExecutor
```

---

## 14. Quan hệ giữa các layer

```text
┌──────────────────────────────┐
│         Excel / Test Data    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Keyword Executor       │
└──────────────┬───────────────┘
               │
               │ Keyword + Target
               ▼
┌──────────────────────────────┐
│        Keyword Library       │
└──────────────┬───────────────┘
               │
               │ gọi hành vi POM
               ▼
┌──────────────────────────────┐
│          Page Object         │
│     Locator + UI behavior    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       BasePage / Wait        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Selenium WebDriver      │
└──────────────────────────────┘
```

---

## 15. Driver Injection

WebDriver được tạo ở Core/DriverManager.

Page Object nhận driver:

```text
DriverManager
      ↓
WebDriver
      ↓
Test/Execution Layer
      ↓
LoginPage(driver)
```

Page Object không tự gọi:

```text
webdriver.Chrome()
```

và không tự quyết định browser.

Điều này giúp POM độc lập với cơ chế khởi tạo driver.

---

## 16. Locator Maintenance

Khi UI thay đổi:

Ví dụ trước:

```python
"username_field": (By.ID, "username")
```

Sau:

```python
"username_field": (By.NAME, "username")
```

Test case vẫn có thể giữ:

```text
LoginPage.username_field
```

và Keyword vẫn giữ:

```text
ENTER_TEXT
```

Chỉ thay đổi locator tại Page Object.

Luồng:

```text
Excel không đổi
    ↓
Keyword không đổi
    ↓
Target không đổi
    ↓
POM locator thay đổi
```

---

## 17. Phân trách nhiệm

| Thành phần | Trách nhiệm |
|---|---|
| Excel | Mô tả test step |
| Keyword Library | Mô tả/thực thi hành động |
| Keyword Executor | Điều phối keyword |
| Page Object | Quản lý UI abstraction |
| `LOCATORS` | Quản lý locator |
| BasePage | Cung cấp UI operation chung |
| DriverManager | Khởi tạo/quản lý WebDriver |
| Selenium | Thực thi thao tác trên browser |

---

## 18. Quy tắc không được vi phạm

### Rule 1

Không ghi XPath/CSS/ID trong Excel.

### Rule 2

Không ghi locator trực tiếp trong Keyword.

### Rule 3

Không để Page Object tự khởi tạo WebDriver.

### Rule 4

Không để Page Object đọc Excel.

### Rule 5

Không dùng `time.sleep()` làm cơ chế synchronization chính.

### Rule 6

Mỗi Page Object quản lý locator của chính trang đó.

### Rule 7

Target phải ổn định và có ý nghĩa:

```text
PageName.elementName
```

---

## 19. Cấu trúc thư mục POM

```text
pages/
├── base_page.py
├── login_page.py
├── home_page.py
├── search_page.py
├── product_page.py
└── cart_page.py
```

Trong đó:

```text
base_page.py
    → thao tác dùng chung

login_page.py
    → locator + behavior của Login

home_page.py
    → locator + behavior của Home

product_page.py
    → locator + behavior của Product
```

---

## 20. Tiêu chí hoàn thành POM Design

POM design được xem là hoàn tất khi:

- Có `BasePage`.
- Có quy ước Page Object.
- Có quy ước `LOCATORS`.
- Có quy ước Target.
- Page Object nhận WebDriver qua constructor.
- Locator không xuất hiện trong Excel.
- Keyword không chứa locator.
- Có cơ chế explicit wait tại BasePage/POM.
- Có thể thay đổi locator mà không cần sửa test step Excel.
