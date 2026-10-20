import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

# --- SETUP DESIGN THEME ---
st.set_page_config(page_title="PhotoHub - Ecosystem", layout="wide")

PRIMARY_COLOR = "#3E2723"  # Dark Brown
SECONDARY_COLOR = "#F4C9D6"  # Pastel Pink
ACCENT_COLOR = "#8D6E63"

# Custom CSS injection for theme branding
st.markdown(f"""
    <style>
    .main {{ background-color: #FAF6F0; }}
    h1, h2, h3 {{ color: {PRIMARY_COLOR} !important; font-family: 'Helvetica Neue', Arial, sans-serif; }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white !important;
        border-radius: 8px;
        border: 1px solid {PRIMARY_COLOR};
        padding: 0.5rem 1rem;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: {SECONDARY_COLOR};
        color: {PRIMARY_COLOR} !important;
        border-color: {PRIMARY_COLOR};
    }}
    .card {{
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid {SECONDARY_COLOR};
        margin-bottom: 15px;
    }}
    .admin-card {{
        background-color: #FFF2F4;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid {SECONDARY_COLOR};
        margin-bottom: 10px;
    }}
    .badge {{
        background-color: {SECONDARY_COLOR};
        color: {PRIMARY_COLOR};
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATABASE (Session State Persistence) ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

    # 1. Partner/Vendor Database
    st.session_state.vendors = [
        {"id": "V1", "name": "Minh An Portfolio", "type": "Photographer", "style": "Nàng thơ", "price": 1500000, "location": "Sài Gòn", "rating": 4.9, "slots": ["08:00", "10:00", "14:00", "16:00"], "bookings_count": 124, "status": "Active", "portfolio": "https://images.unsplash.com/photo-1517841905240-472988babdf9"},
        {"id": "V2", "name": "Linh Chi Studio", "type": "Studio", "style": "Hàn Quốc", "price": 1800000, "location": "Sài Gòn", "rating": 4.8, "slots": ["09:00", "13:00", "15:00"], "bookings_count": 89, "status": "Active", "portfolio": "https://images.unsplash.com/photo-1534528741775-53994a69daeb"},
        {"id": "V3", "name": "Hoàng Long Art", "type": "Photographer", "style": "Vintage", "price": 1200000, "location": "Hà Nội", "rating": 4.7, "slots": ["10:00", "14:00", "18:00"], "bookings_count": 56, "status": "Active", "portfolio": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"},
        {"id": "V4", "name": "MUA Ngọc Trâm", "type": "Makeup Artist", "style": "Nàng thơ", "price": 500000, "location": "Sài Gòn", "rating": 5.0, "slots": ["07:00", "11:00", "13:00"], "bookings_count": 210, "status": "Active", "portfolio": "https://images.unsplash.com/photo-1494790108377-be9c29b29330"}
    ]

    # 2. Bookings Database
    st.session_state.bookings = [
        {"id": "BK101", "customer": "Nguyễn Văn A", "vendor_id": "V1", "vendor_name": "Minh An Portfolio", "concept": "Nàng thơ Sài Gòn", "date": "2023-11-20", "time": "10:00", "price": 1500000, "deposit": 500000, "status": "Completed", "moodboard": "Moodboard_A", "photo_link": "https://drive.google.com/photo-final", "rating": 5, "review": "Ảnh chụp siêu xịn xò đúng gu mình!"},
        {"id": "BK102", "customer": "Trần Thị B", "vendor_id": "V2", "vendor_name": "Linh Chi Studio", "concept": "Couple kiểu Hàn", "date": "2023-11-22", "time": "14:00", "price": 1800000, "deposit": 500000, "status": "In Progress", "moodboard": "Moodboard_B", "photo_link": "", "rating": None, "review": ""}
    ]

    # 3. Photo Feed
    st.session_state.feeds = [
        {"id": 1, "author": "Minh An", "role": "Photographer", "title": "Nàng thơ hoàng hôn sông Sài Gòn", "likes": 245, "img": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1"},
        {"id": 2, "author": "Linh Chi Studio", "role": "Studio", "title": "Retro Vintage Studio Concept", "likes": 189, "img": "https://images.unsplash.com/photo-1519741497674-611481863552"}
    ]

# --- SIDEBAR - SYSTEM PORTAL SELECTION ---
st.sidebar.image("https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=100", width=70)
st.sidebar.markdown(f"<h2 style='text-align: center; color:{PRIMARY_COLOR};'>PhotoHub</h2>", unsafe_allow_html=True)
portal = st.sidebar.radio("Chọn Không gian truy cập:", ["🌐 Khách hàng (Customer)", "📸 Đối tác (Vendor Portal)", "🔑 Quản trị viên (Admin Master)"])

# --- PORTAL 1: CUSTOMER PORTAL ---
if portal == "🌐 Khách hàng (Customer)":
    st.markdown(f"<h1>✨ Khám phá Thế giới Nhiếp ảnh PhotoHub</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎬 Photo Feed & Inspiration", "🤖 AI Concept Match (Tự động hóa)", "📅 Trực tiếp Booking & Tạo Moodboard", "📦 Lịch sử Đơn hàng"])

    with tab1:
        st.subheader("🔥 Xu hướng nổi bật & Cảm hứng mới")
        col_feed1, col_feed2 = st.columns(2)
        for i, feed in enumerate(st.session_state.feeds):
            col = col_feed1 if i % 2 == 0 else col_feed2
            with col:
                st.image(feed["img"], use_container_width=True)
                st.markdown(f"**{feed['title']}** - Đăng bởi <span class='badge'>{feed['author']} ({feed['role']})</span>", unsafe_allow_html=True)
                st.write(f"❤️ {feed['likes']} lượt yêu thích")
                if st.button(f"Yêu thích & Lưu Concept {feed['id']}"):
                    st.success("Đã lưu thành công vào Bộ sưu tập cảm hứng!")

    with tab2:
        st.subheader("🤖 Tìm Concept & Matching thợ chụp bằng AI")
        st.info("Giao thức tích hợp n8n Webhook: Tự động phân tích nhu cầu và gợi ý Studio + Thợ phù hợp thời gian thực.")

        col_ai1, col_ai2 = st.columns([1, 1])
        with col_ai1:
            ai_query = st.text_input("Nhập ý tưởng của bạn (ví dụ: 'tôi muốn chụp kiểu nàng thơ ngoài trời ở Sài Gòn dưới 2 triệu')", "chụp kiểu nàng thơ ngoài trời ở Sài Gòn dưới 2 triệu")
            budget_val = st.slider("Ngân sách tối đa (VNĐ)", 500000, 3000000, 2000000)
            pref_style = st.selectbox("Chọn tone style ưu tiên", ["Nàng thơ", "Vintage", "Hàn Quốc"])

            run_ai = st.button("⚡ Khởi chạy AI & Đồng bộ hóa n8n")

        with col_ai2:
            if run_ai:
                st.write("**[n8n Automation Log]** Webhook Triggered -> Phân tích thực thể...")
                st.write(f"🔍 Đang lọc dữ liệu thợ chụp theo keyword: `{pref_style}` và ngân sách < `{budget_val}`...")

                # Matching logic
                matched_vendors = [v for v in st.session_state.vendors if v["style"] == pref_style and v["price"] <= budget_val and v["status"] == "Active"]

                if matched_vendors:
                    st.success(f"🎯 Tìm thấy {len(matched_vendors)} Đối tác tối ưu nhất cho bạn!")
                    for mv in matched_vendors:
                        st.markdown(f"""
                        <div class='card'>
                            <h4>🏆 {mv['name']} ({mv['type']})</h4>
                            <p><b>Phong cách:</b> {mv['style']} | <b>Địa điểm:</b> {mv['location']}</p>
                            <p><b>Đánh giá:</b> ⭐ {mv['rating']} ({mv['bookings_count']} booking)</p>
                            <p style='color:green; font-weight:bold;'>Giá dịch vụ: {mv['price']:,} VNĐ</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Không tìm thấy kết quả phù hợp hoàn toàn, hệ thống đề xuất các phương án mở rộng!")

    with tab3:
        st.subheader("📅 Đặt lịch dịch vụ & Tạo Moodboard gửi thợ")
        col_b1, col_b2 = st.columns([1, 1])

        with col_b1:
            st.markdown("##### 1. Thiết kế Moodboard ý tưởng")
            mb_name = st.text_input("Tên Moodboard của bạn", "Concept Sweet Dream 2024")
            poses = st.multiselect("Chọn phong thái / Tư thế chụp", ["Đứng nghiêng đón nắng", "Ngồi đọc sách cổ điển", "Cận cảnh cười nhẹ", "Đi dạo tự nhiên"])
            colors = st.color_picker("Tông màu chủ đạo mong muốn", "#F4C9D6")

        with col_b2:
            st.markdown("##### 2. Chọn thợ & Khung giờ trống")
            chosen_v = st.selectbox("Chọn Đối tác muốn đặt", [v["name"] for v in st.session_state.vendors])
            v_detail = next(v for v in st.session_state.vendors if v["name"] == chosen_v)

            chosen_date = st.date_input("Chọn ngày chụp", datetime.now())
            chosen_slot = st.selectbox("Khung giờ còn trống", v_detail["slots"])

            confirm_bk = st.button("🚀 Xác nhận Booking & Chuyển cọc (500,000đ)")

            if confirm_bk:
                # Append new booking
                new_bk = {
                    "id": f"BK{random.randint(103, 999)}",
                    "customer": "Khách hàng Vãng Lai",
                    "vendor_id": v_detail["id"],
                    "vendor_name": v_detail["name"],
                    "concept": mb_name,
                    "date": str(chosen_date),
                    "time": chosen_slot,
                    "price": v_detail["price"],
                    "deposit": 500000,
                    "status": "Pending",
                    "moodboard": f"{mb_name} (Poses: {', '.join(poses)})",
                    "photo_link": "",
                    "rating": None, "review": ""
                }
                st.session_state.bookings.append(new_bk)
                st.success(f"🎉 Booking {new_bk['id']} đã được khởi tạo! Email xác nhận đã gửi đến Đối tác {v_detail['name']}.")

    with tab4:
        st.subheader("📦 Lịch sử đặt lịch của bạn")
        for bk in st.session_state.bookings:
            st.markdown(f"""
            <div class='card'>
                <h4>Đơn hàng {bk['id']} - Trạng thái: <b>{bk['status']}</b></h4>
                <p><b>Đối tác:</b> {bk['vendor_name']} | <b>Thời gian:</b> {bk['date']} ({bk['time']})</p>
                <p><b>Moodboard ý tưởng:</b> {bk['moodboard']}</p>
                <p><b>Tổng giá trị:</b> {bk['price']:,} VNĐ (Đã cọc {bk['deposit']:,} VNĐ)</p>
                {f"<p><b>🔗 Link nhận ảnh:</b> <a href='{bk['photo_link']}'>Tải ảnh tại đây</a></p>" if bk['photo_link'] else "<p><i>⏳ Đang tiến hành photoshoot/retouching...</i></p>"}
            </div>
            """, unsafe_allow_html=True)
            if bk['status'] == "Completed" and not bk['rating']:
                st.text_input("Để lại feedback chân thực cho thợ ảnh:", key=f"rev_{bk['id']}")
                st.slider("Đánh giá số sao:", 1, 5, 5, key=f"star_{bk['id']}")
                if st.button("Gửi Đánh giá", key=f"btn_rev_{bk['id']}"):
                    st.success("Cảm ơn bạn đã đóng góp đánh giá xác thực! Bạn nhận được +10 PhotoPoints!")

# --- PORTAL 2: VENDOR PORTAL ---
elif portal == "📸 Đối tác (Vendor Portal)":
    st.markdown(f"<h1>📸 Studio & Photographer Workspace</h1>", unsafe_allow_html=True)

    # Select which partner acts
    partner_name = st.selectbox("Đăng nhập Tài khoản Đối tác:", [v["name"] for v in st.session_state.vendors])
    partner_data = next(v for v in st.session_state.vendors if v["name"] == partner_name)

    v_tab1, v_tab2, v_tab3 = st.tabs(["📊 Quản lý Lịch trống & Portfolio", "🔔 Tiếp nhận & Phê duyệt Đơn hàng", "📤 Trả Sản phẩm & Hậu kỳ"])

    with v_tab1:
        st.subheader("🗓️ Thiết lập Lịch biểu rảnh rỗi (Time-slot Inventory)")
        all_slots = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
        updated_slots = st.multiselect("Tích chọn các khung giờ bạn có thể nhận khách:", all_slots, default=partner_data["slots"])
        if st.button("Cập nhật Kho lịch trống"):
            partner_data["slots"] = updated_slots
            st.success("Hệ thống AI Matcher đã cập nhật kho lịch trống mới nhất của bạn!")

        st.write("--- ")
        st.subheader("🖼️ Quản lý Album Portfolio (Đầu vào cho AI)")
        st.text_input("Tags Phong cách của bạn (dấu phẩy ngăn cách)", partner_data["style"])
        st.image(partner_data["portfolio"], width=300, caption="Ảnh bìa Album")

    with v_tab2:
        st.subheader("🔔 Quản lý đơn booking chờ xử lý")
        active_bookings = [b for b in st.session_state.bookings if b["vendor_id"] == partner_data["id"]]

        if not active_bookings:
            st.write("Hiện chưa có lịch đặt nào mới.")
        for b in active_bookings:
            st.markdown(f"""
            <div class='card'>
                <h4>Yêu cầu từ: {b['customer']} | Ngày: {b['date']} | Giờ: {b['time']}</h4>
                <p><b>Ý tưởng Moodboard:</b> {b['moodboard']}</p>
                <p><b>Tổng chi phí:</b> {b['price']:,} VNĐ (Tiền cọc an toàn: {b['deposit']:,} VNĐ)</p>
                <p>Trạng thái hiện tại: <span class='badge'>{b['status']}</span></p>
            </div>
            """, unsafe_allow_html=True)

            if b["status"] == "Pending":
                col_a, col_r = st.columns(2)
                if col_a.button("✅ Chấp nhận chụp", key=f"app_{b['id']}"):
                    b["status"] = "In Progress"
                    st.rerun()
                if col_r.button("❌ Từ chối do bận đột xuất", key=f"rej_{b['id']}"):
                    b["status"] = "Cancelled"
                    st.rerun()

    with v_tab3:
        st.subheader("📤 Trả ảnh gốc & Hậu kỳ")
        retouching_bookings = [b for b in st.session_state.bookings if b["vendor_id"] == partner_data["id"] and b["status"] == "In Progress"]
        if not retouching_bookings:
            st.info("Không có đơn hàng nào đang trong quá trình hậu kỳ.")
        for rb in retouching_bookings:
            st.write(f"**Đơn hàng:** {rb['id']} - Khách: {rb['customer']}")
            drive_url = st.text_input("Nhập link Google Drive / Dropbox ảnh hoàn thiện:", "https://drive.google.com/drive/folders/...")
            if st.button("Hoàn tất bàn giao ảnh", key=f"done_{rb['id']}"):
                rb["photo_link"] = drive_url
                rb["status"] = "Completed"
                st.success("Tuyệt vời! Ảnh đã được tự động gửi tới khách hàng và báo cáo doanh thu tới Admin.")
                st.rerun()

# --- PORTAL 3: ADMIN PORTAL ---
elif portal == "🔑 Quản trị viên (Admin Master)":
    st.markdown(f"<h1>🔑 Hệ thống Phân tích & Vận hành PhotoHub</h1>", unsafe_allow_html=True)

    # Key Authentication Gate
    admin_key = st.text_input("Nhập mã Admin mật để truy cập dữ liệu nâng cao:", type="password")
    if admin_key != "photohub2024":
        st.warning("Vui lòng nhập mật mã quản trị chính xác để truy xuất dữ liệu Escrow và mô hình dự báo AI.")
    else:
        st.success("Đăng nhập thành công với vai trò Quản trị viên tối cao!")

        adm1, adm2, adm3 = st.tabs(["📊 Dashboard Tài chính & Vận hành", "🔮 Dự báo AI & Churn Risk", "🛡️ Kiểm duyệt Đối tác & Tranh chấp"])

        with adm1:
            st.subheader("📈 Tổng quan Sàn giao dịch")

            # Calculate financial metrics
            total_bookings = len(st.session_state.bookings)
            escrow_balance = sum(b["deposit"] for b in st.session_state.bookings if b["status"] != "Completed")
            commission_collected = sum(b["price"] * 0.1 for b in st.session_state.bookings if b["status"] == "Completed")

            c1, c2, c3 = st.columns(3)
            c1.metric("Tổng số Booking hệ thống", total_bookings)
            c2.metric("Tiền cọc đang tạm giữ (Escrow)", f"{escrow_balance:,} VNĐ")
            c3.metric("Doanh thu hoa hồng sàn (10%)", f"{commission_collected:,} VNĐ")

            st.write("--- ")
            st.subheader("📂 Toàn bộ danh sách Booking liên kết 3 Bên")
            st.dataframe(pd.DataFrame(st.session_state.bookings))

        with adm2:
            st.subheader("🔮 Phân hệ Dự báo & Phân tích thông minh")

            st.markdown("##### 1. Dự báo Doanh thu & Dòng tiền (Time-series Regression)")
            chart_data = pd.DataFrame(
                np.random.randn(20, 2) * 5000000 + 15000000,
                columns=['Doanh thu dự kiến', 'Dòng tiền cọc ký quỹ']
            )
            st.line_chart(chart_data)

            col_fore1, col_fore2 = st.columns(2)
            with col_fore1:
                st.markdown("""
                <div class='admin-card'>
                    <b>⚠️ Dự báo Rủi ro Churn (Đối tác rời bỏ nền tảng):</b><br>
                    - <i>Minh An Portfolio:</i> <span style='color:green; font-weight:bold;'>Thấp (5%)</span><br>
                    - <i>Hoàng Long Art:</i> <span style='color:orange; font-weight:bold;'>Trung bình (35%)</span> (Do ít hoạt động)
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class='admin-card'>
                    <b>🤖 Tỷ lệ chuyển đổi AI Match (CTR/CVR):</b><br>
                    - Tỷ lệ click từ gợi ý: <b>24.6%</b> (Tăng 2.1% so với tuần trước)
                </div>
                """, unsafe_allow_html=True)

            with col_fore2:
                st.markdown("""
                <div class='admin-card'>
                    <b>🔥 Dự báo Xu hướng Concept mới (Trending):</b><br>
                    - <i>Hàn Quốc Retro:</i> <b>Đột biến (Viral)</b><br>
                    - <i>Street Photography:</i> <b>Phổ thông</b>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class='admin-card'>
                    <b>🚨 Dự báo Nguy cơ chậm SLA bàn giao ảnh:</b><br>
                    - Đơn hàng <i>BK102</i> có nguy cơ trễ hẹn giao ảnh: <span style='color:red; font-weight:bold;'>78%</span>
                </div>
                """, unsafe_allow_html=True)

        with adm3:
            st.subheader("🛡️ Phê duyệt Đối tác KYC & Xử lý khiếu nại")

            st.markdown("##### Danh sách đăng ký mở shop từ Photographer mới")
            st.info("Hệ thống nhận diện tự động hồ sơ: Hợp lệ (98%)")

            col_kyc1, col_kyc2 = st.columns([2, 1])
            with col_kyc1:
                st.write("**Ứng viên:** Nguyễn Văn C - Photographer Tự do (Hà Nội)")
                st.write("**Hồ sơ:** Chuyên môn cưới ngoại cảnh, kinh nghiệm 3 năm.")
            with col_kyc2:
                st.button("Duyệt đối tác (Approve)")