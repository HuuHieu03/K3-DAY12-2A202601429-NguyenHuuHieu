# my_workspace

## Mục đích
`my_workspace` là hệ thống chuẩn hóa để quản lý tài liệu, kế hoạch, tiến độ, nhật ký và tóm tắt thảo luận theo cách thân thiện cho cả Con người và AI Agent.

## Cấu trúc thư mục
- `plans/`: kế hoạch thực thi theo từng phiên bản.
- `progress/`: theo dõi trạng thái công việc và tiến độ.
- `logs/`: nhật ký thực hiện, lỗi và cách khắc phục.
- `history/`: lưu tóm tắt các cuộc trò chuyện và thảo luận.
- `docs/`: tài liệu cần thiết trong quá trình review PR và làm việc chung.

## Quy tắc đặt tên file
Áp dụng cho tất cả file Markdown không phải `README.md` và không phải `TEMPLATE_*.md`:
- Chỉ dùng chữ thường, dấu gạch dưới `_`.
- Tên file theo mẫu: `vX.Y.Z_<YYYY-MM-DD>_<topic>_<type>.md`.
- Ví dụ: `v1.0.0_2026-08-10_api_gateway_plan.md`.

## YAML Frontmatter bắt buộc
Mỗi file Markdown chuẩn hóa phải có frontmatter ở đầu file:
```yaml
---
version: "1.0.0"
date: "YYYY-MM-DD"
type: "plan | progress | log"
status: "DRAFT | PLANNED | IN_PROGRESS | COMPLETED | CANCELLED"
author: "Tên người tạo hoặc AI Agent"
target_component: "Tên thành phần / Module"
tags: ["tag1", "tag2"]
summary: "Tóm tắt ngắn gọn 1-2 câu về nội dung file."
---
```

## Quy trình làm việc 4 bước cho AI Agent
1. Đọc `README.md` để nắm quy chuẩn.
2. Đọc file `plans/` liên quan để hiểu mục tiêu và phạm vi.
3. Cập nhật file `progress/` để phản ánh trạng thái mới nhất.
4. Ghi lại phát hiện, lỗi và cách sửa vào `logs/`.

## Cách dùng `docs/`
- Lưu tài liệu phục vụ review PR, checklist, ghi chú kỹ thuật, và các tài liệu hỗ trợ ra quyết định.
- Ưu tiên nội dung ngắn gọn, dễ quét nhanh, và có thể tái sử dụng cho các phiên sau.
- Nếu tài liệu là một file Markdown chuẩn hóa, vẫn tuân thủ quy tắc tên file và frontmatter như các thư mục khác.

## Nguyên tắc vận hành
- Mỗi thay đổi lớn nên có một file kế hoạch riêng.
- Chỉ cập nhật progress khi có trạng thái thực tế mới.
- Log phải ghi rõ root cause, cách sửa, và kết quả nghiệm thu.
- History chỉ lưu bản tóm tắt ngắn gọn của phiên làm việc.
