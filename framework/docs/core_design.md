# Core Module Design

## 1. Mục đích

Core modules là các module điều phối quá trình thực thi test của framework.

Core chịu trách nhiệm:
- Quản lý WebDriver
- Đọc và điều phối testcase
- Thực thi keyword
- Quản lý context của một testcase
- Kết nối Keyword Library với Page Object Model
- Điều phối luồng thực thi từ testcase đến trình duyệt

Core không chứa locator cụ thể của từng trang web.
Locator và thao tác trên từng trang được quản lý bởi Page Object Model.

---

## 2. Các Core Modules

Framework gồm các core modules chính:

    Driver Manager `core/driver_manager.py`-> Khởi tạo, quản lý và đóng WebDriver 

    Test Executor `core/test_executor.py` -> Điều phối quá trình thực thi, chạy từng step test case

    Keyword Executor `core/keyword_executor.py` Nhận keyword và thực thi keyword tương ứng

    Test Context `core/test_context.py` -> Lưu trữ driver, testcase ID, status, data,... trong quá trình test

---

## 3. Driver Manager

### File

`core/driver_manager.py`

### Mục đích

Driver Manager chịu trách nhiệm quản lý Selenium WebDriver.

### Chức năng

- Khởi tạo browser
- Cấu hình browser
- Trả về WebDriver hiện tại
- Đóng browser
- Quản lý vòng đời của WebDriver

### Input

- Browser name
- Các cấu hình browser nếu có

### Output

- Một Selenium WebDriver instance

Test Executor
    ↓
Driver Manager
    ↓
Selenium WebDriver
    ↓
Browser


## 4. Test Executor

### File

`core/test_excutor.py`

### Mục đích

Là module điều phối quá trình thực thi test case.

### Chức năng

- Nhận test case từ dữ liệu đầu vào
- Duyệt từng test step
- Gửi step tới Keyword Executor
- Truyền keyword, target, data và expected value
- Xử lý kết quả thực thi

### Input

- Một test case gồm nhiều step:

Step 1:
Keyword = OPEN_BROWSER

Step 2:
Keyword = NAVIGATE
Data = https://example.com

Step 3:
Keyword = ENTER_TEXT
Target = LoginPage.username
Data = admin

Step 4:
Keyword = CLICK
Target = LoginPage.login_button

### Output

- Kết quả thực thi test case: PASS/FAIL

## 5. Keyword Executor

### File

`core/keyword_executor.py`

### Mục đích

Keyword Executor chịu trách nhiệm nhận một keyword từ test case và tìm cách thực thi keyword đó.

### Chức năng

- Nhận tên keyword
- Nhận target
- Nhận test data
- Nhận expected value
- Tìm keyword tương ứng trong Keyword Library
- Gọi keyword để thực thi
- Trả về kết quả thực thi

### Input

- Keyword
- Target
- Data
- Expected

Ví dụ:
Keyword = ENTER_TEXT
Target = LoginPage.username
Data = admin

### Output

Kết quả thực thi: PASS/FAIL

### Quan hệ
Test Executor
    ↓
Keyword Executor
    ↓
Keyword Registry
    ↓
Keyword Library
    ↓
POM
    ↓
Selenium WebDriver

## 6. Test Context

### File

`core/test_context.py`

### Mục đích

Lưu trữ thông tin và trạng thái trong quá trình thực thi một test case.

### Có thể lưu trữ

- WebDriver instance
- Test case ID
- Test data
- Current page
- Execution status
- Các dữ liệu cần chia sẻ giữa các keyword

Ví dụ
TestContext:

test_case_id = TC_LOGIN_01
browser = Chrome
driver = WebDriver instance
status = RUNNING

### Quan hệ

Test Executor
    ↓
Test Context
    ↑
Keyword Executor

## 7. Quan hệ giữa các Core modules

### Luồng xử lý chính:

Test Case
    ↓
Test Executor
    ↓
Keyword Executor
    ↓
Keyword Registry
    ↓
Keyword Library
    ↓
POM
    ↓
Selenium WebDriver
    ↓
Web Application

### Test Context được sử dụng trong quá trình thực thi

              Test Context
             ↗            ↖
Test Executor              Keyword Executor
      ↓                          ↓
      └──────── Execution ───────┘

  