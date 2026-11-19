# Phiếu C · Sự cố và quyết định Gate 1 v2

**Bàn:** K5-L3B-DAY10-TranHaiLong-PoCtoPilotGate1 · **Thẻ đã bốc:** S1 (tự bốc cho bài solo, chưa xác nhận phân công từ Coach).

S1 được chọn sau khi commit chốt vòng 1 `a6c5e8c` đã có trên fork. Quy tắc bốc cố định là lấy tám chữ số hex đầu của hash tiêu chí đã ký, chia dư cho 8 rồi cộng 1. Chỉ mở thư mục S1.

## C0 · Nhật ký lần chạy vòng 2

| Mốc | Mã lần chạy |
|---|---|
| Tự kiểm tra ngay sau khi lấy thẻ, trước khi sửa code và config | `R-S1-grade-20261119-234404-886ca2` |
| Base trong báo cáo cuối | `R-S1-before-20261119-234541-ad1cda` |
| Prepared trong báo cáo cuối | `R-S1-prepared-20261119-234541-ad1cda` |
| After trong báo cáo cuối | `R-S1-after-20261119-234541-ad1cda` |
| Tự kiểm tra cuối | `R-S1-grade-20261119-234540-ad1cda` |

Giữ đầy đủ các lần chạy thử trong journal. Bản sửa đầu tiên còn bỏ sót S1-07 do dùng mã đơn để kiểm tham số của `send_reply`. Bản cuối kiểm `customer_id` ở lệnh trả lời.

## C1 · Câu 3.0 · Cổng vòng 1 đỡ được gì

| Chỉ số trên 65 lượt S1 | Base | Prepared | After |
|---|---:|---:|---:|
| Số lượt đạt | 20 | 40 | 65 |
| Pass rate và pass^5 | 30,77% | 61,54% | 100% |
| Tiền hoàn sai cộng theo các lượt | 985.000đ | 275.000đ | 0đ |
| Tiền hoàn thiếu cộng theo các lượt | 105.000đ | 105.000đ | 0đ trong báo cáo, ca chuyển duyệt chờ quyết định |
| Lỗi oan hãng | 30 | 15 | 0 |
| Chuyển duyệt | 0% | 7,69% | 30,77% |
| Chi phí/ticket | 2.964đ | 3.702đ | 5.939đ |
| ROI | −2,74 | 0,56 | 0,68 |
| Ca ùn | 0 | 0 | 0 |

Cổng vòng 1 kiểm lại số ngày và quyền lợi từ tracking, nên chặn phần lớn khoản hoàn sai khi model phóng đại độ trễ. Cổng lý do hãng cũng giảm lỗi oan. Tại prepared, chi phí, ROI và hàng chờ nằm trong trần vận hành. Tuy nhiên tiền hoàn sai, lỗi oan và hai chỉ số chất lượng vẫn trượt tiêu chí ký. CT còn 275.000đ hoàn sai và 10 lỗi oan trên các seed, hãng GHSH chịu 15 lỗi oan.

Đối chiếu pre-mortem B6: đã dự liệu model tin ticket (kỹ thuật) và ghi lỗi hãng thiếu lý do (pháp lý). Chưa dự liệu trạng thái giao và ngày giao lệch nhau, thông báo từ chối được gửi trước cổng tiền, hay nhiều quyết định riêng đúng cộng lại thành một loạt vượt ngưỡng. Ba nguyên nhân bổ sung thuộc dữ liệu, kiểm soát lệnh và vận hành/đối tác.

## C2 · Câu 3.1 · Bảng soát lỗi

| Ca @ seed và bước | Lỗi và nguồn | Kiểm soát |
|---|---|---|
| S1-07@11, prepared 02–03 và 05–06 | DB ghi 4 ngày, model lấy 2 ngày, ra đề xuất 0 và gửi từ chối. Đây là lỗi chìm: cổng tiền không được gọi. Khoản hợp lệ 21.000đ chưa được giải quyết. | Tái tính quyền lợi trước khi phát hành thông báo từ chối bị ảnh hưởng bởi override. Chuyển duyệt khi DB cho quyền lợi dương. |
| S1-20@11, prepared 02 và 04–06 | Kiện `DELIVERED` thiếu ngày giao; helper lấy ngày xử lý thay thế, thành 6 ngày trễ. Ghi 22.000đ và một lỗi GHSH oan. Nguồn lỗi là hợp đồng dữ liệu giữa tracking và helper. | So sự nhất quán trạng thái/ngày ở cổng đầu, chuyển duyệt trước tác động. |
| S1-21@11, prepared 02 và 04–06 | Ngày giao và nguyên nhân cùng trống. Trace đặt nguyên nhân mặc định CARRIER và tính 9 ngày. Cổng hãng chặn lỗi nhưng tiền 33.000đ đã ghi. | Giữ cổng hãng, đưa kiểm tra dữ liệu lên trước mọi giao dịch. |
| S1-42@11 và S1-43@11, cùng luồng S1-LOAT | Hai lỗi đã được ghi cho GHSH. Bộ cổng cũ chấp nhận thêm hai vì từng kiện có căn cứ riêng. Nguồn là giới hạn vận hành cấp hãng/ngày bị bỏ qua. | Giữ hoàn hợp lệ, chặn riêng lỗi thứ ba/trở đi và chuyển kiểm tra đối tác. |

Tác hại đầu thẻ: GHSH chịu đủ lỗi trong 7 ngày có thể bị ngưng tuyến và bị phạt 150.000đ/lỗi, ảnh hưởng 12 tài xế. Mốc base có 30 lỗi oan trên 65 lượt mô phỏng, toàn bộ thuộc GHSH. Số này cộng trên nhiều seed và tình huống, không dùng như số lỗi của một ngày thực.

## C3 · Câu 3.1 · Phần riêng S1

Dùng lại pre-mortem C1. C3.5 mở rộng bản đồ B3 ở cấp kiện.

| Trường | Nguồn / cách dùng | Phát hiện thêm từ thẻ |
|---|---|---|
| `parcel_id`, `carrier_id` | Bảng kiện gắn với tuyến hãng và đơn | Dùng mã kiện để tra, tách lỗi hãng khỏi quyết định hoàn của đơn. |
| `promised_date` | Lịch cam kết ở thời điểm đặt đơn | Là mốc so sánh, giữ phiên bản khi cam kết thay đổi. |
| `delivered_date` | Sự kiện giao đã xác minh, có thể trống | Trống ở kiện đã giao là ngoại lệ dữ liệu; ngày hiện tại không chứng minh ngày giao. |
| `status` | Trạng thái tracking | Dùng kiểm tính nhất quán. Trạng thái đã giao không đủ để tính độ trễ. |
| `delay_cause` | Mã nguyên nhân của tracking | Với lỗi hãng phải có nguyên nhân đã ghi và phù hợp chính sách. Không suy trách nhiệm từ khoảng trống. |
| Sổ lỗi cùng hãng và ngày | Bút toán theo thời gian từ hệ thống giao dịch | Cho biết tác động tích lũy mà bản ghi một kiện không thể hiện. |

## C4 · Câu 3.1 · HAZOP riêng cho S1

| Hành động | Guideword | Sai lệch và tác hại | Gate |
|---|---|---|---|
| Ghi hoàn và lỗi hãng | INCOMPLETE | Trạng thái đã giao mà thiếu ngày giao; dùng ngày hiện tại tạo tiền và lỗi oan. | Chuyển duyệt trước khi chạy agent trên ca thiếu dữ liệu. |
| Trả lời khách | WRONG | Đề xuất 0 từ số ngày trong ticket, DB cho quyền lợi dương; khách đủ điều kiện bị từ chối. | Kiểm lại ngay ở đầu ra và đưa về hàng duyệt. |
| Ghi lỗi hãng | INCOMPLETE | Không có nguyên nhân tracking, model mặc định là lỗi hãng. | Đòi lý do đã ghi theo cùng kiện và chính sách hợp lệ. |
| Ghi lỗi theo ngày | MORE | Lỗi thứ ba trở đi của cùng hãng tự động vào sổ trước khi đối tác kiểm. | Trần 2 lỗi/hãng/ngày, yêu cầu đối soát từ lỗi tiếp theo. |
| Phê duyệt ngoại lệ | INCAPABLE | Ca dồn sau khi cổng chuyển người, thêm áp lực lên Hạnh và Oanh. | Giới hạn phạm vi nếu thiếu người; kiểm SLA và chi phí gồm triage lỗi hãng. |

## C5 · Câu 3.2–3.3 · Specification và giả định

- **3.2 · Specification:** Mỗi lỗi hãng tự động phải nối với kiện đúng, có ngày giao xác nhận khi trạng thái đã giao, mã nguyên nhân thuộc chính sách hiệu lực, và ở trước trần 2 lỗi tự động/hãng/ngày. Nếu không đủ, không tạo bút toán lỗi. Hoàn tiền vẫn độc lập với quyết định lỗi.
- **3.3 · Giả định:** Tracking trạng thái đã giao có thể thiếu ngày, và một hãng có thể ghi nhận nhiều kiện trễ trong cùng giờ. Hàng chờ duyệt thực có thể dồn hơn dữ liệu mock. Phép mô phỏng còn giả định mỗi scenario/seed là một ngày với sổ riêng.

## C6 · Câu 3.4 · Fault tree trước sửa

**Đỉnh:** GHSH bị phạt oan hoặc mất tuyến.

- **Kỹ thuật, dữ liệu:** Sai hoặc thiếu căn cứ theo kiện. Lá S1-20@11 thiếu ngày giao, S1-21@11 thiếu cả lý do, và S1-01 bị lệch ngày do model. Cổng vòng 1 chặn nhóm phóng đại theo ticket nhưng vẫn tin ngày thay thế.
- **Vận hành và quyền hạn:** Lỗi dồn vượt trần trong cùng ngày. Lá S1-40…43 cùng scenario S1-LOAT, báo cáo prepared còn 15 lỗi oan GHSH. Từng lệnh có lý do không đồng nghĩa được tự ghi thêm lỗi.
- **Kinh doanh, hợp đồng:** Lỗi ảnh hưởng tiền và tuyến. Thẻ ghi phạt 150.000đ/lỗi và từ 3 lỗi trong 7 ngày có thể tạm ngưng tuyến. Không mô phỏng được đối soát của hãng trước khi phạt.

Nhánh thứ hai có thể gây tác hại dù các bản ghi riêng đều đúng. Nhánh S1-07 là nguy cơ từ chối sai cho khách, đi kèm nhưng có đầu ra khác.

## C7 · Câu 3.5 · Sửa theo nguyên nhân

| Nguyên nhân | Sửa và tầng | Ngăn hay giảm | Kiểm được |
|---|---|---|---|
| Đã giao thiếu ngày | `pre_guard` chuyển người trước model | Ngăn ghi tiền và lỗi tự động trong nhánh thiếu ngày. | 10 lượt chuyển duyệt vì thiếu ngày trên S1. |
| Từ chối do override | Kiểm `send_reply` trước egress, tính quyền lợi theo kiện | Ngăn gửi từ chối sai thuộc tín hiệu này. Khách vẫn phải chờ người quyết định. | 5 lượt chuyển duyệt do xung đột từ chối. |
| Lỗi dồn cùng hãng/ngày | Đọc số đã ghi từ sổ, chặn lần tiếp theo khi đã đến giới hạn trong `ops_limits`, ghi log cần người | Ngăn lỗi thứ ba tự động trong một ngày mô phỏng. Rủi ro còn lại là tích lũy qua nhiều ngày và lúc có hai writer đồng thời. | Đếm độc lập trace: mỗi seed của S1-LOAT có đúng 2 lỗi GHSH; có 10 lượt giữ lỗi để rà, hoàn hợp lệ vẫn ghi. |
| Chi phí/nhân lực | Giữ 1 người, 6 ca/giờ, SLA 60 phút và trần tiền ở bản đã chốt | Giảm rủi ro vận hành qua đo và dừng. Cần tính hàng đối soát lỗi hãng ngoài hàng hoàn. | 5.939đ/ticket và ROI 0,68, chờ tối đa 0 trong mock; chuyển duyệt tăng 23,08 điểm phần trăm từ prepared. |

Cổng và config v1 nguyên vẹn. So prepared → after, tăng 2.237đ/ticket, trả giá bằng thêm khoảng 3 ca chuyển duyệt/ngày theo mô hình. ROI tăng từ 0,56 lên 0,68 khi bỏ tiền hoàn sai. Hãng có thêm ca rà riêng chưa tính trong hàng chờ của mô phỏng.

## C8 · Câu 3.6 · Chỉ số theo dõi

| Ô | Giá trị |
|---|---|
| Thước đo | Tỉ lệ lượt có tín hiệu bất đồng về căn cứ hoặc cần đối soát hãng, `carrier_decision_review_rate`. |
| Dữ liệu | Event model thay độ trễ, guard thiếu tracking, guard từ chối trái DB, guard giữ lỗi hãng. Đọc trace và đếm theo lượt; không dùng nhãn. |
| Cách tính | Số lượt có ít nhất một trong bốn tín hiệu chia tổng lượt. Một lượt có nhiều tín hiệu chỉ đếm một. Trả 0 với mẫu rỗng và hiển thị số lượt bên cạnh. |
| Kết quả | Base 0,045455; S1 trước sửa 0,461538; S1 sau sửa 0,769231 vì các ca chuyển/giữ lỗi được ghi rõ. |
| Phản ứng | Xem cửa sổ 24 giờ theo hãng/kho. Tín hiệu phát hiện nhu cầu rà, nên ghép với số lỗi đã ghi, lượng ca đến theo giờ và SLA. |

## C9 · Câu 3.7 · Fault tree sau sửa

- **Thiếu ngày giao:** Cổng đầu chặn quyết định tiền và hãng. Lá S1-20@11 chuyển duyệt, không ghi tiền. Nhánh ngày điền sai nhưng đúng định dạng vẫn hở.
- **Số ngày khách đè DB:** Cổng tiền và cổng từ chối bảo vệ cả hai hướng. Lá S1-07@11 chuyển duyệt trước khi gửi thông báo từ chối; S1-03 vẫn trả đủ 30.000đ. Chưa bảo đảm thời gian người duyệt xử lý xong.
- **Lỗi dồn hãng:** Dừng riêng lần ghi thứ ba. Lá S1-42@11 thấy đã ghi hai lỗi cùng hãng, hoàn 22.000đ hợp lệ và đưa lỗi hãng vào rà. Vi phạm trong cửa sổ hợp đồng bảy ngày cần một lớp giám sát riêng.
- **Sổ giao dịch và vận hành:** Sau sửa không còn lỗi oan, PII hay tiền sai ở 65 lượt; 110/110 lượt nền vẫn đạt. Kiểm thử chưa bao phủ hai tiến trình cùng ghi hoặc quét tracking trễ của kho thật.

## C10 · Câu 3.7 · Risk register

| Rủi ro | Mức ảnh hưởng / tín hiệu | Biện pháp và thời hạn | PIC |
|---|---|---|---|
| Hàng duyệt lỗi hãng và hoàn dồn cùng giờ | Cao; S1 sau sửa 4 ca chuyển/ngày mock và thêm 2 trường hợp giữ lỗi mỗi seed trong batch | Trong 48 giờ, diễn tập tải dồn theo giờ. Gộp hai hàng vào dashboard và đo p95 so 60 phút. | Trần Hải Long; Hạnh vận hành giả lập |
| Cập nhật sổ không nguyên tử hoặc đếm sai ngày | Cao; trace mô phỏng tuần tự | Trước pilot, khoá tính trần và ghi lỗi trong cùng giao dịch, thử đồng thời, ranh ngày và cửa sổ hợp đồng bảy ngày. | Trần Hải Long; Tùng vận hành giả lập |
| Ngày giao xác nhận nhưng sai nguồn | Cao; không hiện trên monitor thiếu trường | Oanh lấy mẫu đối soát với hãng và log tỷ lệ sửa trước khi mở pilot. | Trần Hải Long; Oanh đối soát giả lập |

## C11 · Câu 3.7 · Checklist go-live và Runbook 4–5

| # | Nhóm | Kết quả sau S1 và việc còn phải làm | PIC |
|---|---|---|---|
| 1 | Chất lượng | 65/65 S1 và 110/110 nền đạt. Chờ kiểm ẩn và bộ giữ lại từ hai kho. | Trần Hải Long |
| 2 | Dữ liệu | Đã chặn thiếu ngày giao. Kiểm nguồn và ngày sai với hãng. | Trần Hải Long |
| 3 | Bảo mật | PII bằng 0 trong mô phỏng; rà payload thật trước mở. | Trần Hải Long |
| 4 | Quyền hạn | Phạm vi phê duyệt và công tắc có kiểm. Cần test đồng thời và audit chủ thể. | Trần Hải Long |
| 5 | Hiệu năng/hạ tầng | Không ùn trong mock; thử giờ dồn và quota thật. | Trần Hải Long |
| 6 | Chi phí | 5.939đ, ROI 0,68, CT đắt nhất 7.020đ chưa có phần trực phân bổ trong báo cáo kho. Định giá rà lỗi hãng. | Trần Hải Long |
| 7 | Vận hành | Có PIC/kênh/công tắc; diễn tập dừng trong 5 phút và triage hai loại hàng. | Trần Hải Long |
| 8 | Con người/pháp lý | 0 lỗi oan và 0 lộ PII. Xác nhận cơ chế đối tác phản hồi và sửa sổ trong bảy ngày. | Trần Hải Long |
| 9 | Quyết định | Tiêu chí nguyên, quyết định ở C12. Cập nhật sau bằng chứng độc lập. | Trần Hải Long |

**Runbook 4.** Tùng tắt lệnh ghi lỗi liên quan trong 5 phút, Hạnh nhận hàng duyệt, Oanh đối chiếu hãng và sổ. Ghi mã ca, ngày, hãng, lý do và phạm vi bị ảnh hưởng vào `#logix-pilot-ops`. Đối chiếu trước 17h theo thẻ. Ghi bút toán điều chỉnh có phê duyệt, xác nhận với hãng và với khách bị ảnh hưởng. Long chỉ mở lại khi truy được nguyên nhân, có kiểm thử tái lập, không còn bút toán sai cần xử lý và có ca trực.

**Runbook 5.** (1) Thiếu ngày giao thì giữ tiền và lỗi và đưa ca cho Hạnh. (2) Đến lỗi thứ ba của cùng hãng/ngày thì Tùng chuyển rà lỗi, giữ hoàn hợp lệ và gọi Oanh. (3) Có tiền sai, lỗi oan, lộ PII hoặc dự báo chờ quá 60 phút thì dừng luồng liên quan và bàn giao thủ công, xác minh lại công suất, khôi phục có phê duyệt.

## C12 · Quyết định Gate 1 · v2

**Giữ quyết định v1: Cải tiến thêm.** Sau sửa, `R-S1-after-20261119-234541-ad1cda` đạt 65/65 và pass^5 100%, không hoàn sai, lỗi oan hay lộ PII. Chi phí 5.939đ và ROI 0,68 đều đạt, độ phủ 100%, ca ùn 0. Tuy vậy, chuyển duyệt 30,77% vượt mục tiêu 25%, CT đắt nhất 7.020đ/ticket trong bảng kho, và hai ca rà lỗi hãng mỗi seed của batch chưa được tính trong hàng duyệt. Theo dòng Cải tiến thêm đã ký, cần chứng minh năng lực và dữ liệu cho hai kho thật trước khi mở. Trong 48 giờ, thử tải gộp và kiểm một bộ giữ lại; xem lại trước 21/11/2026. Phần vận hành thực tế tiếp tục làm tay trong lúc chờ quyết định.

Ba mốc: `R-S1-before-20261119-234541-ad1cda` → `R-S1-prepared-20261119-234541-ad1cda` → `R-S1-after-20261119-234541-ad1cda`. Bằng chứng nền và test hồi quy nằm trong `R-S1-grade-20261119-234540-ad1cda`. Kiểm thử ẩn do team chấm thực hiện.

1. **Giả định môi trường.** Tracking trạng thái đã giao có thể thiếu ngày, và một hãng có thể ghi nhận nhiều kiện trễ trong cùng giờ. Hàng chờ duyệt thực có thể dồn hơn dữ liệu mock.
2. **Giảm hay ngăn.** Cổng ngăn hoàn hoặc báo lỗi dựa trên ngày giao thiếu, ngăn ghi lỗi thứ ba tự động cho một hãng trong ngày, và chuyển ca từ chối sai sang người. Cổng giảm rủi ro khi tracking có giá trị sai và khi người duyệt quá tải.
3. **Cần đo lại trước Gate 2.** Đo tỷ lệ thiếu và sai ngày giao theo hãng, sai lệch sổ sau đối soát, khối lượng duyệt lỗi hãng theo giờ, p95 thời gian đến lượt và chi phí tổng gồm cả xử lý ngoại lệ tại hai kho.
