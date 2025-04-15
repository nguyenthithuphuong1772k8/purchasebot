import streamlit as st
import pandas as pd
def load_and_process_data(uploaded_file):
    """Hàm đọc và xử lý dữ liệu từ file"""
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()
        column_mapping = {
            'purchasing document': 'code',
            'material': 'material_code',
            'document date': 'doc_date',
            'supplier/supplying plant': 'supplier',
            'short text': 'description',
            'still to be delivered (qty)': 'quantity',
            'delivery date': 'delivery_date'
        }
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        date_cols = [col for col in ['doc_date', 'delivery_date'] if col in df.columns]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
        return df
    except Exception as e:
        st.error(f"⛔ Lỗi khi đọc file: {str(e)}")
        return None
uploaded_file = st.file_uploader("📤 Chọn file dữ liệu", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = load_and_process_data(uploaded_file)
    
    if df is not None:
        if st.checkbox("👀 Hiển thị toàn bộ dữ liệu"):
            st.dataframe(df)
        st.subheader("🔍 Tìm kiếm thông tin")
        search_code = st.text_input("Nhập mã hàng cần tra cứu:")
        
        if search_code:
            try:
                filtered_data = df[df['material_code'].astype(str).str.strip() == search_code.strip()]
                
                if not filtered_data.empty:
                    st.success(f"✅ Tìm thấy {len(filtered_data)} bản ghi cho mã hàng {search_code}")
                    cols_to_show = ['code', 'material_code', 'description', 
                                   'quantity', 'supplier', 'doc_date', 'delivery_date']
                    cols_to_show = [col for col in cols_to_show if col in df.columns]
                    
                    st.dataframe(filtered_data[cols_to_show].reset_index(drop=True))
                    
                    st.subheader("📊 Tổng hợp thông tin")
                    
                    if 'quantity' in df.columns:
                        total_qty = filtered_data['quantity'].sum()
                        st.markdown(f"**Tổng số lượng cần giao:** {total_qty:,.0f}")
                    if 'supplier' in df.columns:
                        suppliers = filtered_data['supplier'].unique()
                        st.markdown("**Nhà cung cấp:**")
                        for sup in suppliers:
                            st.write(f"- {sup}")
                    if 'delivery_date' in df.columns:
                        dates = filtered_data['delivery_date'].unique()
                        st.markdown("**Ngày giao hàng:**")
                        for date in dates:
                            st.write(f"- {date}")
                else:
                    st.warning(f"⚠️ Không tìm thấy thông tin cho mã hàng {search_code}")
            except Exception as e:
                st.error(f"⛔ Lỗi khi tìm kiếm: {str(e)}")
else:
    st.info("ℹ️ Vui lòng upload file dữ liệu để bắt đầu")
