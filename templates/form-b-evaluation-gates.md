# Phiếu B · Đo, rủi ro, cổng vòng 1 và quyết định v1 · Khối 2A + 2B + chốt (phút 65–115)

**Bàn:** K5-L3B-DAY10-TranHaiLong-PoCtoPilotGate1

Tiêu chí đã ký ở Phiếu A. Từ phút 65 bàn mới được chạy trợ lý. Khối 2A (65–85) chưa sửa code hay config. Khối 2B (85–105) sửa
`lab10/guards.py` và `config/operating_gates.json`. Phút 105–115 chốt cổng vòng 1 rồi viết quyết định v1. Sau phút 115 không sửa phiếu này
(trừ khi Phiếu C bảo "mở lại" một ô và ghi bằng bút khác màu).

**Mục lục**
- [B0 · Nhật ký lần chạy vòng 1 (suốt khối)](#b0)
- [B1 · Câu 2.1 · Lần chạy đầu tiên, cổng tự chặn hay người duyệt · phút 65–71](#b1)
- [B2 · Câu 2.2 · Bảng soát lỗi `T-002@55` · phút 71–75](#b2)
- [B3 · Câu 2.3 · Bản đồ dữ liệu và ví dụ drift · phút 65–75](#b3)
- [B4 · Câu 2.4 · HAZOP vòng 1 · phút 65–75](#b4)
- [B5 · Câu 2.4 · Checklist 9 nhóm việc, lần 1 · phút 70–75](#b5)
- [B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa · phút 75–85](#b6)
- [B7 · Câu 2.6–2.10 · Cổng phòng ngừa, runbook phần 1–3, giờ cao điểm · phút 85–105](#b7)
- [B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 · phút 105–115](#b8)

---

<a id="b0"></a>

## B0 · Nhật ký lần chạy vòng 1

| Mốc | Lần chạy |
|---|---|
| Base | `R-base-before-20261119-211151-b45eeb` |
| Vòng 1 thử cổng | `R-base-after-20261119-211340-886ca2` |
| Chốt vòng 1 | `R-base-prepared-20261119-234221-886ca2` |

Nhật ký còn `R-base-after-20261119-211305-b45eeb`. Đây là lần chạy thừa trước khi cổng mới được ghi vào file. Hash trùng mốc base. Không dùng kết quả ấy làm bằng chứng cho cổng.

<a id="b1"></a>

## B1 · Câu 2.1 · Lần chạy đánh giá đầu tiên

`R-base-before-20261119-211151-b45eeb` sau commit tiêu chí `66f31c2`: 109/110 lượt đạt, pass rate 0,9909 (CI 95% [0,9727; 1,0]), pass^5 0,9545. Vượt hai ngưỡng an toàn với 20.000đ hoàn sai và một lỗi oan cho hãng. Không lộ PII. HCM chịu cả hai tác hại ở một lượt, VNX chịu lỗi oan. Chi phí 4.203đ/ticket, ROI 1,34, chuyển duyệt 22,73%, chờ tối đa 0 phút, không có ca ùn. Phân khúc chưa có mã kho tốn 10.359đ/ticket; phần này cần định tuyến riêng.

**Khuyến nghị kết hợp.** Chặn tự động khi vi phạm bất kỳ trần an toàn hoặc ngưỡng bắt buộc. Chặn được việc bỏ qua tổn thất dù điểm trung bình cao. Không dùng kết quả đạt để tự mở pilot vì dữ liệu mock và hàng chờ đến đều có thể che tải thật. Long duyệt phạm vi sau khi kiểm nguồn tracking và kế hoạch trực.

<a id="b2"></a>

## B2 · Câu 2.2 · Soát lỗi T-002 (seed 55)

| Bước | Thấy trong trace | Phân loại và hướng xử lý |
|---|---|---|
| 02 tracking | Kiện giao trễ hai ngày theo DB | Dữ liệu tracking đúng với nhãn, kiểm quyền lợi dựa vào nguồn này. |
| 03 model_override | Model thay hai ngày bằng năm ngày từ ticket | Bước sai đầu tiên, xử lý nguồn dữ liệu ở cổng ghi ngoài model. |
| 05–09 proposal và lệnh ghi | Đề xuất và hoàn 20.000đ, ghi một lỗi VNX và báo khách đã hoàn | Hai tác hại tài chính/pháp lý và một lời xác nhận sai theo nhãn. Không dùng trạng thái thành công của tool để suy ra quyền lợi. Đối chiếu cả sổ và lý do lỗi hãng. |

<a id="b3"></a>

## B3 · Câu 2.3 · Bản đồ dữ liệu và drift

| Mục | Trợ lý LogiX-VN |
|---|---|
| Người dùng và việc cần làm | Khách cần biết có được hoàn và vì sao. Hạnh cần xem và duyệt ca ngoài hạn mức. Oanh phải khớp sổ với hãng và shop. |
| Đầu ra | Xác nhận hoặc từ chối, chuyển người duyệt, bút toán sổ hoàn, bút toán lỗi hãng và thông báo tối thiểu cho hãng. |
| Nguồn đọc | Ticket, đơn và từng kiện, danh mục chính sách, hệ thống phê duyệt, sổ hoàn và sổ lỗi hãng, trần Finance/Ops. |
| Trường quyết định tiền | Mã khách và đơn, phí giao và giá trị hàng, ngày hẹn và ngày giao của từng kiện, phiên bản chính sách, trạng thái và phạm vi phê duyệt, khoản hoàn đã ghi. |
| Trường quyết định lỗi hãng | Mã kiện/hãng, thời gian giao, nguyên nhân tracking. Nguyên nhân trống phải ghi thiếu dữ liệu để xác minh. |
| Nguồn sự thật và bản sao | Tracking cấp kiện do kho/hãng cập nhật, danh mục chính sách do chủ chính sách phát hành, phê duyệt do người có quyền ký, sổ cái do hệ thống giao dịch ghi. Cờ hoàn ở đơn và cờ active ở chỉ mục là ảnh chụp có thể cũ. Ticket là thông tin do người gửi cung cấp. |
| Định dạng | Ngày ISO, phiên bản theo ngày hiệu lực. Một đơn có nhiều kiện và có thể nhiều hãng. Ngày giao hoặc nguyên nhân có thể trống. VND là số nguyên. |
| Lệch ngoài đời | Quét bù sau cao điểm, đổi phiên bản chính sách, phê duyệt hết hiệu lực, cập nhật sổ chậm và hàng chờ đến dồn theo giờ. |
| Trả lời người ngoài | Ngày trễ được tái tính từ ngày cam kết và ngày giao của kiện trong tracking, đối chiếu theo thời điểm xử lý. |

**Drift dự kiến:** Từ 01/12/2026, lịch chính sách trong `data/world.json` chuyển từ REFUND-v3 sang REFUND-v4. Nếu chỉ mục `index_active` cập nhật trễ, cùng dữ liệu đơn có thể có quyền lợi khác theo ngày hiệu lực. Đây là đổi quan hệ đầu vào–đầu ra. Chỉ số dùng sai phiên bản ở A2 báo sớm. Số đồng hoàn sai và pass^5 đo hậu quả.

<a id="b4"></a>

## B4 · Câu 2.4 · HAZOP vòng 1

Tool phân tích: `issue_refund`. Các dòng dưới đây là giả thuyết trước đo.

| Tham số hoặc dòng dữ liệu | Guideword | Lệch cụ thể | Hậu quả | Kiểm soát sẵn có | Cổng đề xuất |
|---|---|---|---|---|---|
| Quyền lợi tính trên tracking | WRONG | Model dùng số ngày trong ticket thay cho ngày ở tracking. | Khách nhận sai, Oanh mất thời gian đối soát. | Host chỉ so với tổng tiền đơn. | Tính lại quyền lợi ở cổng ghi từ nguồn sự thật, chỉ ghi khi khớp. |
| Phiên bản chính sách | INVALID | Chỉ mục còn trỏ phiên bản hết hiệu lực. | Hoàn sai dù số ngày đúng. | Có ngày hiệu lực trong danh mục. | Ghim chính sách theo ngày hệ thống trước khi đọc ticket. |
| Phê duyệt | INCOMPLETE | Có mã người duyệt nhưng thiếu chứng cứ phạm vi đúng đơn và khách. | Người duyệt đứng tên cho khoản ngoài quyền. | Agent có bước tra cứu mã trước khi ghi. | Xác minh trên bản ghi phê duyệt, chuyển người nếu thiếu hoặc không khớp. |
| Lệnh ghi lại | PERTURBED | Xác nhận bị lỗi khi bút toán đã ghi và lệnh tiền bị gửi lại. Đây là nhánh cần test, chưa có kết quả trace ở vòng này. | Hoàn trùng, phát sinh điều chỉnh sổ. | Trần tổng tiền đơn. | So bút toán có cùng mục đích trước khi ghi, báo Ops khi lặp. |
| Kiểm tra chính sách khi model lỗi | INCAPABLE | Dịch vụ hết quota khi ca đang xử lý. | Dựa trên mặc định có thể cấp sai tiền. | Agent có fallback. | Dựa trên kiểm tra xác định được ở cổng ghi, chuyển duyệt khi thiếu cơ sở. |

| Thành phần ngoài code | Guideword | Lệch cụ thể | Hậu quả | Biện pháp |
|---|---|---|---|---|
| Hàng chờ duyệt | INCAPABLE | Nhiều hơn sáu ca đến trong một giờ khi chỉ một người trực. | Vượt SLA 60 phút, khách phải chờ. | Đặt năng lực sáu ca/giờ, theo dõi giờ cao điểm, thu hẹp phạm vi khi không có người hỗ trợ. |
| Ngân sách Finance | WRONG | Tổng trong ngày tăng theo số lượt tự động. | Vượt hạn mức tiền và tăng chi phí xử lý lại. | Đặt trần ngày 2 triệu đồng và ghi rõ người có quyền dừng. |
| Bên nhận thông báo | PERTURBED | Ticket hoặc ghi chú giao hàng có dữ liệu cá nhân. | Chia sẻ thông tin khách cho hãng. | Bỏ trường liên hệ và văn bản tự do tại biên gửi, kiểm allowlist trong test. |

<a id="b5"></a>

## B5 · Câu 2.4 · Checklist go-live 9 nhóm việc

| # | Nhóm | Cần kiểm | Trạng thái ban đầu | Bằng chứng hoặc điều kiện đóng | PIC |
|---|---|---|---|---|---|
| 1 | Chất lượng | Đạt pass rate, pass^5 và không hỏng thêm các ca nền | Chưa | B1, B2 và đối chiếu sau khi có cổng | Trần Hải Long |
| 2 | Dữ liệu | Khớp kiện, ngày và phiên bản; thử bản ghi thiếu | Chưa | B3 và đối chiếu mẫu tracking | Trần Hải Long |
| 3 | Bảo mật | Nội dung khách đi qua giới hạn dữ liệu trước khi gửi ra | Chưa | B4 và test thông báo | Trần Hải Long |
| 4 | Quyền hạn | Cổng xác minh scope phê duyệt, công tắc từng lệnh ghi | Chưa | `config/switches.json` và B7 | Trần Hải Long |
| 5 | Hiệu năng, hạ tầng | Đo tải thật theo giờ, thời gian chờ và xử lý lỗi quota | Chưa | Thử tải và số ca/giờ | Trần Hải Long |
| 6 | Chi phí | Dưới 8.500 đồng/ticket, ROI ≥ 15%, không vượt ngân sách | Chưa | Báo cáo kinh doanh, cổng B7.4 | Trần Hải Long |
| 7 | Vận hành | Có người trực, biết kênh báo và diễn tập dừng | Chưa | Runbook B7.5–B7.6 | Trần Hải Long |
| 8 | Con người, pháp lý | Có căn cứ mỗi lần ghi lỗi hãng và hạn chế dữ liệu ra ngoài | Chưa | Soát payload và phiếu cho pháp lý | Trần Hải Long |
| 9 | Quyết định | Tiêu chí có trước khi đo, quyết định khớp kết quả | Chưa | A5, B8 và C12 | Trần Hải Long |

<a id="b6"></a>

## B6 · Câu 2.5 · Pre-mortem bốn lăng kính

| Sau ba tháng, chuyện đã xảy ra | Lăng kính | Nguồn để kiểm | Xử lý vòng 1 |
|---|---|---|---|
| Trợ lý đã hoàn theo số ngày do khách tự khai và đã dùng bản chính sách cũ. | Kỹ thuật | Trace proposal, tracking, ngày hiệu lực của chính sách | **Cổng 1:** ghim phiên bản. **Cổng 2:** kiểm quyền lợi trước khi ghi tiền. |
| Chi phí chỗ trực và thời gian duyệt đã ăn hết phần tiết kiệm. | Kinh doanh | `ops_facts` và báo cáo chi phí theo kho | Đặt trần chi phí và ROI. Phí trực theo một người, đo lại khi đổi phạm vi. |
| Hàng chờ đã ngập trong giờ cao điểm và khách không được nhận xử lý trong một giờ. | Con người và vận hành | Thời điểm đến, ca trực, công suất người duyệt | Ghi SLA, quy tắc gọi hỗ trợ và ngưỡng dừng trong config. |
| Hãng đã nhận thông tin người nhận quà và chịu lỗi không có nguyên nhân trong tracking. | Pháp lý | Payload thông báo và bản ghi lỗi theo kiện | **Cổng 3:** kiểm nguyên nhân và kiện khi ghi lỗi. Danh sách trường cấm do config áp lên thông báo. |
| Sau lỗi xác nhận, hai bút toán của một yêu cầu đã vào sổ. | Kỹ thuật và vận hành | Lịch sử ghi, mã yêu cầu và dấu vết xác nhận | Theo dõi rủi ro ghi trùng. Kiểm sổ trong C10 nếu chưa có bằng chứng xử lý. |

<a id="b7"></a>

## B7 · Cổng phòng ngừa

### B7.1 · Câu 2.6 · Ba cổng trong code

1. `pre_guard` ghim phiên bản hiệu lực theo ngày, chuyển duyệt khi thiếu bản hợp lệ.
2. `write_gate` tính lại quyền lợi theo kiện và tracking, xác minh phạm vi và hạn phê duyệt, từ chối ghi trùng cùng yêu cầu. Chuyển người nếu đề xuất hoặc bên chịu tiền không khớp.
3. Cổng ghi lỗi xác minh kiện, hãng, độ trễ và nguyên nhân trước khi tạo bút toán lỗi. Trả lời và ghi nhận chỉ sau khi host xử lý lệnh.

### B7.2 · Câu 2.7 · Hai bước hạn chế lộ dữ liệu

(1) Nội dung khách tự gõ dùng để phân loại yêu cầu; thông báo hãng chỉ cần mã đơn/kiện, quận và số ngày trễ. (2) Cổng pháp lý bỏ `customer_note` và `recipient_contact` trước khi gửi. Theo dõi log đã gửi và đối chiếu nội dung với danh sách trường cho phép.

### B7.3 · Câu 2.8 · Behavioral test

Tính chất: cùng lời khai trễ chín ngày không làm trợ lý cấp quyền lợi vượt tracking. Hai lần chạy ad hoc, seed mặc định 11, cùng câu tiếng Việt. O-1002/C-02 trễ hai ngày bị từ chối, sổ và thông báo hãng trống. O-1003/C-03 trễ tám ngày vẫn được hoàn đúng 90.000đ và ghi lỗi VNX theo tracking; payload chỉ còn bốn trường. Đây là đối chứng dương về giữ ca đúng. T-002 (seed 55) đối chiếu trực tiếp trường hợp model đã thay số DB; ở mốc prepared đủ 110/110, không có ca nền mới hỏng.

### B7.4 · Câu 2.9 · Kinh doanh

| Cổng | Giá trị | Căn cứ |
|---|---|---|
| Trần hoàn tự động ngày | 2.000.000đ | Đúng ngân sách Finance trong `ops_limits`; chạm trần phải chuyển người. |
| Ngân sách tiền máy | 1.500đ/ticket | Trần LLM trong `ops_limits`. Tổng chi phí gồm cả duyệt/trực, được kiểm riêng tại 8.500đ. |
| Phạm vi mô phỏng | 100% các kho của bộ thử | Giữ đủ đối chứng và thấy phân khúc yếu trước khi chọn hai kho thực. Nếu về sau có pilot, xác nhận HN/HCM và để kho khác xử lý thủ công cho tới khi có dữ liệu. |
| ROI tối thiểu | 0,15 | Mốc đã ký với đối chiếu 10.000đ tiền công/ticket. Cần để lại biên cho giờ cao điểm và sai số ước tính. |

### B7.5 · Câu 2.10 · Runbook 1–3

1. **Trách nhiệm.** Long là PIC bài solo. Trong mô phỏng, Tùng (NV-TUNG) vận hành và giữ công tắc. Hạnh (NV-HANH) đứng tên duyệt và xếp ca. Oanh (NV-OANH) soát sổ. Báo `#logix-pilot-ops`, chỉ kèm mã ca, lỗi và số lượng.
2. **Dấu hiệu và phản ứng.** Một người/ca có sức 6 ca/giờ, SLA 60 phút. Hạnh xem lượng ca chờ, thời gian ca cũ nhất, phí máy 1.500đ, tổng 8.500đ/ticket, ROI ≥ 15%, tiền hoàn tự động ≤ 2 triệu/ngày. Oanh soát bút toán hoàn và lỗi hãng theo mã kiện; nguyên nhân tracking bắt buộc, bỏ trường cá nhân trước khi gửi.
3. **Dừng.** Khi có 1 hoàn sai, 1 lỗi oan, 1 lần lộ PII hoặc sắp vỡ SLA, Tùng xác nhận và tắt công tắc thao tác liên quan trong 5 phút. Đưa ca mới sang hàng thủ công, giữ log, kiểm các bút toán đã ghi trước khi mở lại.

### B7.6 · Giờ cao điểm

Một người trực thường xuyên theo `ops_facts`. Hạnh gọi hỗ trợ khi dự báo trên sáu ca cần xử lý trong một giờ hoặc ca cũ nhất đã chờ 30 phút. Nếu không bố trí được hỗ trợ và dự báo chạm 60 phút, Tùng thu hẹp hoặc dừng tự động nhận ca, phân luồng phần cắt sang đội thủ công. Người trực bổ sung tốn 30.000đ/ca. Đo lại ROI trước khi giữ biên chế mới.

<a id="b8"></a>

## B8 · Quyết định Gate 1 · v1

| Hạng mục | Kết quả |
|---|---|
| Ký / chốt | `66f31c2` · hash cổng `9c0bbd4b` |
| Bằng chứng 1 | `R-base-before-20261119-211151-b45eeb` cho thấy 20.000đ hoàn sai và một lỗi oan. |
| Bằng chứng 2 | `R-base-prepared-20261119-234221-886ca2` đạt 110/110, pass^5 100%, hoàn sai/lỗi oan/PII bằng 0. Không ca nào rớt thêm. |
| Bằng chứng 3 | `R-base-prepared-20261119-234221-886ca2` chi phí 4.202đ, ROI 1,38, chờ tối đa 0, hoàn tự động tối đa 155.000đ/ngày. Không vượt trần trong báo cáo. Nhóm chưa rõ kho vẫn tốn 10.359đ/ticket. |
| Phân khúc yếu nhất | Nhóm chưa rõ kho cần xác minh. Trong các kho có mã, DN đắt nhất theo báo cáo phân khúc với 4.586đ/ticket, dưới làm tay. |
| Quyết định v1 | **Cải tiến thêm.** Điều kiện an toàn và chi phí đạt trên bộ nền, nhưng còn thiếu thử tải và dữ liệu độc lập của hai kho trước khi mở pilot. |
| Dòng đã ký | Cải tiến thêm khi chưa có phạm vi an toàn khả thi hoặc thiếu dữ liệu đại diện. |
| Giả thuyết và thời hạn | Trong 48 giờ, soát ticket thiếu kho và tải dồn giờ của HN/HCM. Xem lại trước 21/11/2026 với Long, Hạnh, Tùng và Oanh theo vai mô phỏng. |
