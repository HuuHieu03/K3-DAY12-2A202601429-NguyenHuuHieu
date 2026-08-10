# Phiếu Phản Ánh — K3 Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay dòng `> *Câu trả lời của bạn*` bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Nguyen Huu Hieu  Mã học viên: 2A202601429

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Việc "chết sớm" giúp ngăn chặn nguy cơ đẩy code lên môi trường production (như cloud) mà quên cấu hình bảo mật. Nếu để mặc định là "changeme", ứng dụng vẫn chạy bình thường và hacker có thể sử dụng chính key mặc định này để vượt qua lớp xác thực, dẫn đến hậu quả lộ lọt dữ liệu hoặc phát sinh chi phí khổng lồ.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> `{"message": "Request processed", "request_id": "req-123", "user_id": "sv-test", "latency": 0.15, "status": 200}`
> Hai việc làm được với log JSON: 1) Có thể đẩy trực tiếp vào các hệ thống quản lý log (như ELK stack, Datadog) để dễ dàng query và trích xuất theo từng thuộc tính (như `user_id` hay `status`). 2) Dễ dàng thiết lập cảnh báo (alert) tự động khi trường `latency` quá cao hoặc `status` báo lỗi 500, điều mà chuỗi print dạng văn bản thô không thể tự động phân tích được.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | ~1.1 GB |
| Multi-stage | ~150 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Phần chênh lệch bao gồm các trình biên dịch hệ thống (như `gcc`, `build-essential`), cache của package manager (`apt-get`), và các file mã nguồn/build tạm thời của thư viện Python. Bằng cách dùng multi-stage, chúng ta chỉ chép sang stage cuối những file đã biên dịch xong (`site-packages`) và các file code thật sự cần để chạy app.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Lệnh `RUN pip install` và các lệnh cài đặt phía trên nó sẽ được Docker dùng lại từ cache, chỉ lệnh `COPY . .` và các layer từ đó trở xuống (CMD, USER) mới bị chạy lại. Nếu đặt `COPY . .` lên trước, mỗi lần sửa bất kỳ file code nào (như `main.py`), cache của `COPY` sẽ bị vô hiệu, kéo theo lệnh `RUN pip install` cũng phải cặm cụi chạy lại từ đầu dù không có thư viện nào mới, làm tăng đáng kể thời gian build.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Chuỗi sự kiện: Kẻ tấn công lợi dụng lỗ hổng trong code (VD: RCE - Remote Code Execution) để chạy được lệnh bash trong container. Do container chạy quyền root, hacker có toàn quyền root bên trong, từ đó có thể chỉnh sửa các file nhạy cảm và tìm cách thoát ra ngoài chiếm quyền máy chủ gốc (host) thông qua cơ chế mount volume hoặc qua các lỗ hổng của nhân hệ điều hành (kernel). Lệnh `USER appuser` cắt đứt chuỗi này: kẻ gian dù chọc được vào bash cũng chỉ có quyền của user thường, không thể cài cắm phần mềm hay phá hoại hệ thống.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Một người dùng có thể gửi tới 20 request trong vòng 2 giây liên tiếp. Cách thực hiện: họ gửi liên tục 10 request vào lúc 00:59 giây, hệ thống cấp phép. Ngay lúc đó giây chuyển sang 00:00 (hệ thống reset lại lượt đếm), và họ lập tức gửi thêm 10 request nữa vào lúc 00:00. Sliding window giải quyết triệt để lỗ hổng này bằng cách luôn tính số request trong đúng khoảng 60 giây lùi về trước tính từ thời điểm hiện tại.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limit kiểm soát **số lượng** request trong một thời gian ngắn (chống spam/DDoS), trong khi cost guard kiểm soát **tổng chi phí** tích lũy dài hạn trong tháng (tránh "cháy túi" trả tiền API). 
> - Tình huống Rate limit qua nhưng Cost guard chặn: Người dùng mỗi ngày chỉ hỏi chậm rãi 5 câu (hoàn toàn thỏa mãn giới hạn phút) nhưng sau 20 ngày tổng tiền Token sử dụng vượt quá ngân sách 10 USD (cost guard chặn).
> - Tình huống Rate guard qua nhưng Rate limit chặn: Vào ngày mùng 1 đầu tháng, tiền budget đang dồi dào, nhưng có người dùng cho bot gửi 20 request trong 1 giây để cào dữ liệu nhanh (bị rate limit chặn ngay).

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> 1. Redis đột ngột mất kết nối. 
> 2. Liveness probe (kiểm tra `/health` nay đã bị gộp) không gọi được Redis nên trả về báo lỗi. 
> 3. Nền tảng quản lý (như K8s) cho rằng cả 3 container đã bị chết lâm sàng, bắt đầu kill (giết) các container đó và khởi động lại. 
> 4. Các container mới được bật lên lại tiếp tục bị kill vì Redis vẫn chưa có mạng (CrashLoopBackOff), toàn bộ hệ thống sập hẳn. 
> Nếu tách riêng: `/ready` thất bại thì bộ định tuyến chỉ ngừng gửi request mới vào các container đó, còn `/health` vẫn xanh giúp giữ container sống đứng đợi Redis phục hồi.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> `history_length` sẽ tăng không đều đặn, bị nhảy cóc hoặc quay về 1. Nguyên nhân là các request mới có thể được Load Balancer điều hướng phân tán ngẫu nhiên đến bất kỳ container nào trong số 3 container đó. Mỗi container lưu một biến cục bộ dict riêng nên không chia sẻ lịch sử trò chuyện. Việc dùng Redis (database tập trung bên ngoài) giúp ứng dụng trở thành stateless: mọi container đều đọc/ghi vào một chỗ, đảm bảo `history_length` luôn tăng đều đặn chính xác.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Mình gặp lỗi `sh: 1: uvicorn: not found` khi deploy service lên nền tảng Render. Mình phát hiện lỗi này nhờ đọc log console trực tiếp trên dashboard của Render và thấy nó báo lỗi thoát code 127 khi chạy CMD. Mình phân tích và hiểu nguyên nhân là do Dockerfile đang sử dụng kĩ thuật Multi-stage build nhưng ở bước 2 đã vô ý không copy các file binary thực thi (như uvicorn) nằm ở `/usr/local/bin` từ thư mục build. Mình đã khắc phục bằng cách thêm câu lệnh `COPY --from=builder /usr/local/bin /usr/local/bin` vào stage runtime của Dockerfile.
