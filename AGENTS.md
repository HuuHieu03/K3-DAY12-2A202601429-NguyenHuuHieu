# AGENTS.md – Quy tắc cho các AI agents trong Lab Day 12 (Cloud Services & Deployment)

---

## 🎯 Mục tiêu chính
1. **Triển khai** một AI agent (FastAPI) lên URL công khai, bảo mật, chi phí hạn chế và không bị downtime khi cập nhật.
2. Tuân thủ **12‑Factor**: tách cấu hình ra môi trường, không chứa secret trong code.
3. Xây dựng **Docker multi‑stage**, chạy dưới user không có quyền root, image ≤ 500 MB.
4. Bảo vệ API bằng **API key**, **sliding‑window rate limit** và **budget guard** (ngân sách tháng).
5. Đảm bảo **health / readiness probes**, **graceful shutdown**, **stateless** để scale ngang.
6. Deploy lên **Railway, Render hoặc Cloud Run** và cung cấp thông tin trong `DEPLOYMENT.md`.
7. Hoàn thành toàn bộ **checkpoint** (CP1‑CP5) và (tuỳ chọn) **bonus CI/CD**.

---

## 📚 Kiến thức cần nắm
- **FastAPI** (v0.110+) – routing, middleware, dependency injection.
- **Docker** – multi‑stage builds, `USER` non‑root, `.dockerignore`.
- **12‑Factor Config** – `pydantic‑settings`, `.env`, không commit secrets.
- **API security** – xác thực bằng header `X‑API‑Key`, kiểm tra khóa trong môi trường.
- **Rate limiting** – sliding‑window, biến `RATE_LIMIT_PER_MINUTE`.
- **Cost guard** – biến `MONTHLY_BUDGET_USD`, kiểm soát chi phí trả lời.
- **Redis** – lưu lịch sử hội thoại, health check, dùng fakeredis nếu không có Docker.
- **Health / readiness** – endpoint `/health` trả về `{ "status": "ok" }`, `/ready` chỉ trả về 200 khi Redis sẵn sàng.
- **Graceful shutdown** – xử lý SIGTERM, đóng kết nối Redis, dừng server cleanly.
- **CI/CD** – GitHub Actions workflow (bonus), badge status trong README.
- **Cloud deployment** – cấu hình `railway.toml` hoặc `render.yaml`, set env vars trên dashboard.

---

## ✅ Các quy tắc (AI‑friendly) – Được viết bằng tiếng Việt
> **Lưu ý:** Các quy tắc này dành cho **agents** (app code) và **developers**. Tuân thủ để nhận điểm đầy đủ.

### 1. Bảo mật & secrets
- **Không bao giờ** commit file `.env` hoặc bất kỳ secret nào (API key, DB credentials) vào repo. `.gitignore` đã có sẵn.
- **Chỉ** lấy giá trị secret từ biến môi trường (`AGENT_API_KEY`, `REDIS_URL`, …). Trong `DEPLOYMENT.md` chỉ ghi **tên** biến, **không** ghi giá trị.
- Khi gọi API, phải truyền `X‑API‑Key: <AGENT_API_KEY>` trong header. Yêu cầu **không có** API key trả về 401.

### 2. Cấu hình 12‑Factor
- Tất cả cấu hình (port, rate limit, budget, log level) được định nghĩa trong `app/config.py` bằng `pydantic‑settings` và đọc từ `.env`.
- Các biến môi trường bắt buộc: `PORT`, `AGENT_API_KEY`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`, `MONTHLY_BUDGET_USD`, `LOG_LEVEL`.
- Mọi giá trị mặc định **không** chứa secret; nếu cần giá trị mặc định, dùng placeholder an toàn.

### 3. API & Rate limiting
- Middleware **rate_limiter** phải kiểm tra `RATE_LIMIT_PER_MINUTE`. Sau khi đạt giới hạn, trả về **429 Too Many Requests**.
- `cost_guard` kiểm tra tổng chi phí tháng (đơn vị USD). Khi vượt `MONTHLY_BUDGET_USD`, trả về **403 Forbidden** với thông báo “budget exceeded”.
- Các endpoint:
  - `POST /ask` – yêu cầu API key, `X‑User‑Id` (định danh người dùng) và body `{"question": "..."}`.
  - `GET /health` – luôn trả về 200 và JSON `{ "status": "ok" }`.
  - `GET /ready` – trả về 200 chỉ khi Redis kết nối thành công.

### 4. Docker & CI/CD
- Dockerfile **phải** là multi‑stage, giảm kích thước ≤ 500 MB, sử dụng `USER appuser` (không root).
- `.dockerignore` phải bao gồm `.env`, `__pycache__`, `tests/`, `*.pyc`, `*.pyo`.
- `docker‑compose.yml` phải định nghĩa service `app` và `redis` (nếu có). Đánh dấu `★` ở các file cần chỉnh sửa.
- **Bonus**: nếu có workflow CI/CD, phải đặt file `.github/workflows/ci.yml`, badge passing trong README.

### 5. Logging & Monitoring
- Log phải ở định dạng **JSON**, mức độ `INFO` hoặc `DEBUG` thông qua biến `LOG_LEVEL`.
- Mỗi request ghi `request_id`, `user_id`, `latency`, `status`, và **audit** (có hay không vi phạm guardrails).
- Khi phát hiện vi phạm (rate‑limit, budget, missing API key), log mức `WARNING` và trả về thông báo lỗi rõ ràng.

### 6. Scaling & Reliability
- Service **stateless** – không lưu state trên disk, chỉ trong Redis.
- `lifecycle.py` phải lắng nghe SIGTERM, đóng kết nối Redis, rồi dừng FastAPI gracefully.
- Các probe (`/health`, `/ready`) được khai báo trong Docker/Kubernetes config để auto‑restart nếu cần.

### 7. Kiểm thử & Đánh giá
- Mỗi checkpoint (CP1‑CP5) có **test** tương ứng trong thư mục `tests/`. Đảm bảo **tất cả** test pass trước khi nộp.
- `exercises.md` phải có 10 câu trả lời tự viết, không sao chép.
- `DEPLOYMENT.md` phải được **điền đầy đủ** thông tin thực tế sau khi deploy thành công (URL, platform, ngày, biến môi trường đã set).
- Khi chạy `python grade.py`, điểm tối đa 100 + bonus ≤ 10. Nếu repo tên không đúng, trừ 5 điểm.

### 8. Đặt tên Repository
- Định dạng: `DAY12-<MãHV>-<HọTên>` (không dấu, không khoảng trắng). Sai tên **trừ 5 điểm**.

---

## 📌 Lưu ý chung
- **Không** bao giờ ghi giá trị secret vào bất kỳ file nào trong repo (đặc biệt `DEPLOYMENT.md`).
- Khi gặp lỗi không giải quyết được trong 10 phút, **gọi Lab Coach** và tiếp tục các block còn lại.
- Mọi thay đổi phải **commit** thường xuyên để chứng minh quá trình làm việc.
- Các file có dấu `★` ở `README.md` là **bắt buộc** phải chỉnh sửa hoặc tạo mới.

---

*Đây là file `AGENTS.md` tổng hợp các quy tắc AI‑friendly mà agents và người phát triển cần tuân theo trong Lab Day 12.*
