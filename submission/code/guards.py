"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("chưa xác định được chính sách có hiệu lực")
    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    if order and order["customer_id"] == ctx.ticket["customer_id"] and order.get("parcels"):
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        if parcel["status"] == "DELIVERED" and not parcel.get("delivered_date"):
            ctx.log("tracking_incomplete", parcel_id=parcel["parcel_id"])
            return Verdict.escalate("kiện đã giao nhưng thiếu ngày giao, cần đối soát")
    return Verdict.allow(policy_id=policy["policy_id"])


def _approval_covers(ctx, action, order):
    matches = ctx.tools.lookup_approvals(
        approval_id=action["approval_id"], ticket_id=ctx.ticket["ticket_id"],
        order_id=order["order_id"], customer_id=order["customer_id"], status="valid",
    )
    return any(
        a.get("expires_at") and a["expires_at"] >= ctx.as_of
        and a.get("max_vnd", 0) >= action["amount_vnd"]
        for a in matches
    )


def _refund_gate(ctx, action, order, parcel, policy, delay):
    if ctx.tools.ledger_rows(order_id=order["order_id"], ticket_id=ctx.ticket["ticket_id"]):
        return Verdict.deny("yêu cầu đã có bút toán hoàn")

    entitlement = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    if entitlement <= 0:
        return Verdict.deny("tracking và chính sách không cho phép hoàn")
    if action.get("basis") != "policy" or action.get("payer") != "LOGIX":
        return Verdict.escalate("cần người xác minh căn cứ hoàn và bên chịu tiền")
    if action["amount_vnd"] != entitlement:
        return Verdict.escalate("đề xuất khác số tiền tính từ tracking và chính sách")

    approval_id = action.get("approval_id")
    if approval_id and not _approval_covers(ctx, action, order):
        return Verdict.escalate("phê duyệt không còn hiệu lực hoặc không khớp phạm vi")
    if entitlement > policy["auto_limit_vnd"] and not approval_id:
        return Verdict.escalate("quá hạn mức tự động và chưa có phê duyệt")
    return Verdict.allow()


def _negative_proposal_used_override(events):
    used_ticket_delay = any(
        event["type"] == "model_override" and event.get("field") == "delay_days"
        for event in events
    )
    return used_ticket_delay and any(
        e["type"] == "proposal" and e["amount_vnd"] <= 0 for e in events
    )


def write_gate(ctx, action):
    tool = action.get("tool")
    check_denial = tool == "send_reply" and _negative_proposal_used_override(ctx.events)
    if tool not in ("issue_refund", "file_carrier_fault") and not check_denial:
        return Verdict.allow()

    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    key = "customer_id" if check_denial else "order_id"
    if not order or action.get(key) != order[key] or order["customer_id"] != ctx.ticket["customer_id"]:
        return Verdict.deny("không xác minh được chủ đơn và lệnh ghi")
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    parcel_id = ctx.ticket.get("parcel_id")
    parcels = order["parcels"]
    if not policy or not parcels or (parcel_id and all(p["parcel_id"] != parcel_id for p in parcels)):
        return Verdict.escalate("thiếu chính sách hoặc chứng cứ tracking cho kiện")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    if check_denial:
        if H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause")) > 0:
            ctx.log("reply_review_required", parcel_id=parcel["parcel_id"])
            return Verdict.escalate("từ chối theo ticket trái với quyền lợi ở tracking")
        return Verdict.allow()
    if tool == "issue_refund":
        return _refund_gate(ctx, action, order, parcel, policy, delay)

    if (action.get("parcel_id"), action.get("carrier_id"), action.get("delay_days")) != (
        parcel["parcel_id"], parcel["carrier_id"], delay
    ) or not H.carrier_at_fault(policy, parcel, delay):
        return Verdict.deny("lỗi hãng không khớp kiện hoặc nguyên nhân tracking")

    carrier = parcel["carrier_id"]
    limit = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    count = len(ctx.tools.fault_rows(carrier_id=carrier))
    if limit is not None and count >= limit:
        ctx.log("carrier_fault_review_required", carrier_id=carrier, recorded=count, limit=limit)
        return Verdict.deny("đã chạm trần ghi lỗi tự động của hãng, cần người đối soát")
    return Verdict.allow()
