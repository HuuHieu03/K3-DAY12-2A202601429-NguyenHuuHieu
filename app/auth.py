"""CP3 — Xác thực bằng API key.

Public URL = ai cũng gọi được. Không có lớp này, hóa đơn LLM của bạn do
người lạ quyết định.
"""

from __future__ import annotations

import secrets

from fastapi import Header, HTTPException, status

from .config import get_settings

ANONYMOUS_USER = "anonymous"


def verify_api_key(
    x_api_key: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None),
) -> str:
    """Kiểm tra header ``X-API-Key``; trả về user_id nếu hợp lệ.

    TODO (CP3):
      1. Lấy khóa đúng từ ``get_settings().agent_api_key``.
      2. Nếu ``x_api_key`` là None hoặc không khớp → raise
         ``HTTPException(status_code=401, detail="invalid or missing API key")``.
      3. So sánh bằng ``secrets.compare_digest(a, b)``, **không dùng** ``==``.
         Toán tử ``==`` dừng ngay tại ký tự đầu khác nhau, nên thời gian trả
         lời rò rỉ thông tin về khóa (timing attack). ``compare_digest`` luôn
         chạy hết chuỗi.
      4. Hợp lệ → trả về ``x_user_id`` nếu client có gửi, ngược lại trả
         ``ANONYMOUS_USER``. user_id này là đơn vị để rate limit và tính chi phí.

    Gợi ý: dùng ``status.HTTP_401_UNAUTHORIZED`` cho dễ đọc.
    """
def verify_api_key(
    x_api_key: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None),
) -> str:
    """Kiểm tra header ``X-API-Key`` và trả về ``user_id``.

    - Lấy ký khóa thực tế từ ``get_settings().agent_api_key``.
    - Nếu header ``X-API-Key`` không tồn tại hoặc không khớp → raise 401.
    - So sánh bằng ``secrets.compare_digest`` để tránh timing attack.
    - Trả về ``x_user_id`` nếu client cung cấp, ngược lại trả ``ANONYMOUS_USER``.
    """
    settings = get_settings()
    expected_key = settings.agent_api_key
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing API key",
        )
    # Constant‑time comparison
    if not secrets.compare_digest(x_api_key, expected_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing API key",
        )
    # Nếu client cung cấp user_id, sử dụng nó, nếu không dùng anonymous
    return x_user_id or ANONYMOUS_USER
