# Phiếu A · Tiêu chí và cách đo

**Bàn:** K5-L3B-DAY10-TranHaiLong-PoCtoPilotGate1 · **Người lập:** Trần Hải Long (2A202603891), phụ trách ba vai.

<a id="a1"></a>

## A1 · Mục tiêu (câu 1.1–1.2)

- **1.1 · Hệ thống:** Giảm chi phí xử lý yêu cầu hoàn phí giao trễ tại hai kho. Mỗi quyết định cần có căn cứ truy lại được, khớp với sổ cái và có đường chuyển cho người duyệt, theo tiêu chí pilot trong PRD v1.1 §3 của Lab 9. [PRD v1.1](https://github.com/longhtr028/K5-L3B-DAY09-TranHaiLong-2A202603891-EvaluationandFailureAnalysis/blob/main/docs/PRD_v1.1.md) · [Eval card Lab 9](https://github.com/longhtr028/K5-L3B-DAY09-TranHaiLong-2A202603891-EvaluationandFailureAnalysis/blob/main/docs/eval_card.md)
- **1.2 · Chị Oanh, kế toán:** Có thể đối chiếu từng bút toán hoàn và lỗi hãng theo mã đơn, kiện, chính sách hiệu lực và lần chạy. Khoản điều chỉnh phải theo quy trình lưu vết để sổ của LogiX, shop và hãng khớp cuối tuần.
- **1.2 · Chị Hạnh, trưởng ca:** Ca chuyển đến có căn cứ tracking và trạng thái duyệt rõ ràng, vào hàng chờ trong SLA 60 phút. Có quyền trả lại ca thiếu căn cứ.

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3–1.4)

| | 1.3 · Offline | 1.4 · Telemetry production |
|---|---|---|
| Bước / hành vi | Chọn đúng phiên bản chính sách | Tác hại lên hãng do ghi lỗi thiếu căn cứ |
| Thước đo | Tỉ lệ quyết định dùng sai hoặc thiếu chính sách hiệu lực | Số lỗi hãng vừa ghi mà thiếu liên kết với bản ghi tracking có nguyên nhân, theo hãng và kho |
| Dữ liệu | Trace chọn chính sách, ngày xử lý và bảng chính sách đã phiên bản hóa. Kỹ sư soát 22 ticket × 5 seed, chủ chính sách xác nhận quy tắc hiệu lực | Sổ lỗi hãng, mã đơn/kiện, thời điểm, bản ghi tracking và audit quyết định. Chỉ lấy trường cần đối soát |
| Cách tính | Số lần policy ID không khớp phiên bản hiệu lực tại ngày của ca chia số ca tới bước quyết định. Thiếu policy ID ở ca tới bước được tính lỗi. Đếm riêng ca chưa tới bước | Nối theo mã đơn và kiện tại thời điểm ghi. Mỗi lỗi không nối được hoặc thiếu nguyên nhân được đếm một lần theo ID bút toán, xác minh với Ops trước khi điều chỉnh |
| Khung thời gian / ngưỡng báo động | Theo mỗi lần đánh giá offline | Cửa sổ 24 giờ trượt. Một lỗi thiếu căn cứ thì báo Tùng và Oanh, tạm dừng ghi lỗi tự động để kiểm tra |
| Điểm mù | Không phát hiện điều khoản đã công bố nhưng sai nội dung | Tracking có nguyên nhân nhưng mã sai vẫn có thể lọt, cần lấy mẫu đối soát với hãng |

<a id="a3"></a>

## A3 · Đọc khoảng tin cậy (câu 1.5)

Chọn **(b)**. Chênh lệch quan sát chỉ là một ca và 100% vẫn nằm trong khoảng tin cậy của X. Cần đánh giá ghép cặp để kết luận về độ lớn và độ chắc của chênh lệch.

<a id="a4"></a>

## A4 · Bản tiêu chí (câu 1.6)

| Thước đo | Câu chấp nhận và xử lý khi trượt |
|---|---|
| Pass rate ≥ 0,92 | Nếu dưới 92% lượt trên bộ nền hoặc thẻ, giữ ở giai đoạn cải tiến. Với 110 lượt, mức này cần tối thiểu 102 lượt đạt và chỉ dùng để sàng lọc pilot có người duyệt. |
| Pass^5 ≥ 0,85 | Nếu dưới 85% ticket đúng cả năm seed, giữ ở giai đoạn cải tiến hoặc cắt phân khúc thiếu ổn định rồi đo lại. Với 22 ticket cần ít nhất 19 ticket đúng cả năm. |
| Tiền hoàn sai ≤ 0 đồng | Nếu có bất kỳ đồng nào hoàn sai, dừng quyền ghi hoàn tự động, đối soát, sửa và đo lại trước khi mở. |
| Lỗi oan cho hãng ≤ 0 | Nếu có từ một lỗi oan, dừng ghi lỗi tự động, báo Tùng và Oanh, xác minh với hãng. |
| Lộ PII ≤ 0 | Nếu có từ một lần lộ, đóng luồng gửi cho hãng, giữ dấu vết và xử lý sự cố trước khi mở. |
| Chuyển người duyệt ≤ 25% (mục tiêu) | Nếu vượt 25%, không nới luật an toàn. Hạnh xem lượng đến theo giờ và lên phương án thu hẹp hoặc phân ca. |

**Hai phương án về độ tin cậy.** Phương án chặt yêu cầu ≥ 95% lượt đúng. Phương án đã đề xuất yêu cầu ≥ 92%, với điều kiện mọi ngưỡng tác hại vẫn bằng 0 và có người duyệt trong pilot. Mức 85% pass^5 giữ mốc tin cậy liên tiếp của eval card v2 Lab 9; cần đánh giá lại khi có seed và kho thật.

**Kinh doanh và vận hành.** Tổng chi phí ≤ 8.500 đồng/ticket, giữ biên 1.500 đồng dưới giá làm tay 10.000 đồng/ticket để chịu sai số chi phí. ROI ≥ 15% sau phí model, trực, duyệt và tiền hoàn sai. Mốc 8.500 đồng tương đương ROI khoảng 17,6% khi tiền hoàn sai bằng 0, nên hai ngưỡng nhất quán. Số ca ùn ≤ 0 theo SLA 60 phút và ca 480 phút. Mỗi người mock duyệt 6 ca/giờ. Mốc 25% là mục tiêu kế hoạch để giữ thời gian cho giờ dồn ca, rà lại và nghỉ. Nguồn số liệu: `data/world.json` mục `ops_facts`, `ops_limits`.

**Ranh giới đầu ra.** Không gửi tên, số điện thoại hoặc địa chỉ khách cho hãng. Chuyển duyệt khi tổng hoàn tự động của một khách sẽ vượt 300.000 đồng/ngày hoặc sắp ghi lần lỗi thứ ba trong ngày cho cùng một hãng. Giữ trần tổng tự động theo Finance là 2.000.000 đồng/ngày.

| Câu soát | Kết luận |
|---|---|
| Ý nghĩa theo từng bên | Khách cần được hoàn đúng, hãng và shop cần đối soát, Hạnh cần hàng chờ chịu được và Oanh cần sổ chính xác. |
| Ai chịu thiệt | Ép giảm chuyển duyệt có thể tạo hoàn sai hoặc lỗi oan. Ba ngưỡng an toàn là ngưỡng cứng. |
| Ngày 1 | Chỉ cân nhắc hai kho có dữ liệu và ca trực. Hành động chi tiền cần truy lại được và dừng nhanh. |
| Ngày 1.000 | Xác nhận lại mô hình chi phí, tải theo 12 kho, mã nguyên nhân và hiệu lực chính sách. Giữ ngưỡng an toàn bằng 0 và đặt lại ngưỡng năng lực theo dữ liệu mới. |

**Quyết định.** Tiếp tục khi mọi ngưỡng bắt buộc và vận hành đạt trong phạm vi. Thu hẹp khi xác định được phần an toàn và kiểm lại phần giữ. Cải tiến thêm khi có tác hại hoặc chưa có phạm vi khả thi, hẹn đo lại trong 48 giờ. Dừng nếu cùng tác hại lặp lại sau hai vòng hoặc thu hẹp vẫn đắt hơn làm tay.

<a id="a5"></a>

## A5 · Ký trước đánh giá

| Mục | Trạng thái |
|---|---|
| Thời điểm ký | 2026-11-19T21:11:22 (ICT) |
| Commit ký | `66f31c2` |
| Đã có trên GitHub trước lần đo đầu? | Có. Đã kiểm tra SHA của `origin/main` trước khi chạy eval. |

Ngày xem lại: trong hai ngày sau khi có báo cáo, Long phụ trách quyết định cùng các vai giả lập Hạnh (duyệt), Tùng (vận hành) và Oanh (đối soát).
