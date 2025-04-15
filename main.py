import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📁 Ứng dụng Tra cứu PO", layout="wide")
st.title("📁 Ứng dụng đọc nhiều file Excel/CSV có lưu tạm bộ nhớ")

uploaded_files = st.file_uploader("📤 Tải lên nhiều file dữ liệu", type=["xlsx", "csv"], accept_multiple_files=True)

if uploaded_files:
    st.session_state["saved_files"] = [
        {"name": f.name, "data": f.read()} for f in uploaded_files
    ]
    st.success("✅ Đã lưu các file vào bộ nhớ tạm.")

def process_file(file_bytes, file_name):
    try:
        if file_name.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            df = pd.read_csv(io.BytesIO(file_bytes))

        df.columns = df.columns.str.strip().str.lower()
        column_mapping = {
            'purchasing document': 'purchasing_document',
            'material': 'material_code',
            'document date': 'doc_date',
            'supplier/supplying plant': 'supplier',
            'short text': 'description',
            'still to be delivered (qty)': 'quantity',
            'delivery date': 'delivery_date'
        }
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})

        for col in ['doc_date', 'delivery_date']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

        return df
    except Exception as e:
        st.error(f"⛔ Lỗi khi đọc file {file_name}: {str(e)}")
        return None

if "saved_files" in st.session_state:
    file_names = [f["name"] for f in st.session_state["saved_files"]]
    selected_file = st.selectbox("📄 Chọn file để xem nội dung", file_names)

    for f in st.session_state["saved_files"]:
        if f["name"] == selected_file:
            df = process_file(f["data"], f["name"])
            if df is not None:
                st.subheader(f"🧾 Nội dung file: `{selected_file}`")
                st.dataframe(df, use_container_width=True)

                st.subheader("🔍 Tìm kiếm theo mã hàng")
                search_code = st.text_input("Nhập mã hàng:")
                if search_code:
                    filtered = df[df['material_code'].astype(str).str.strip() == search_code.strip()]
                    if not filtered.empty:
                        st.success(f"✅ Tìm thấy {len(filtered)} kết quả")
                        st.dataframe(filtered)
                    else:
                        st.warning("⚠️ Không tìm thấy mã hàng trong file này.")

if st.button("🧹 Xoá toàn bộ file đã lưu"):
    st.session_state.pop("saved_files", None)
    st.success("✅ Đã xoá toàn bộ file khỏi bộ nhớ.")
