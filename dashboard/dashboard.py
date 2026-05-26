import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="E-Commerce Insights & RFM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style kustom dashboard
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }
    
    .metric-title {
        font-size: 14px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #3b82f6;
    }
    
    .recommendation-card {
        background-color: #1e293b;
        border-left: 5px solid #10b981;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Koordinat negara bagian di Brazil
STATE_COORDS = {
    'AC': {'lat': -9.702555, 'lon': -68.451852},
    'AL': {'lat': -9.599729, 'lon': -36.052017},
    'AM': {'lat': -3.349336, 'lon': -60.537430},
    'AP': {'lat': 0.086025, 'lon': -51.234304},
    'BA': {'lat': -13.049361, 'lon': -39.560649},
    'CE': {'lat': -4.363151, 'lon': -39.004140},
    'DF': {'lat': -15.810885, 'lon': -47.969630},
    'ES': {'lat': -20.105145, 'lon': -40.503183},
    'GO': {'lat': -16.577645, 'lon': -49.334195},
    'MA': {'lat': -3.798997, 'lon': -44.818627},
    'MG': {'lat': -19.864647, 'lon': -44.421615},
    'MS': {'lat': -20.765006, 'lon': -54.532140},
    'MT': {'lat': -14.156482, 'lon': -55.708956},
    'PA': {'lat': -2.631213, 'lon': -49.485862},
    'PB': {'lat': -7.088298, 'lon': -35.821678},
    'PE': {'lat': -8.179098, 'lon': -35.758866},
    'PI': {'lat': -5.754989, 'lon': -42.509541},
    'PR': {'lat': -24.793607, 'lon': -50.879662},
    'RJ': {'lat': -22.743477, 'lon': -43.155540},
    'RN': {'lat': -5.856702, 'lon': -35.990079},
    'RO': {'lat': -10.341289, 'lon': -62.720579},
    'RR': {'lat': 2.717100, 'lon': -60.672866},
    'RS': {'lat': -29.679191, 'lon': -52.032652},
    'SC': {'lat': -27.222486, 'lon': -49.617937},
    'SE': {'lat': -10.866199, 'lon': -37.181169},
    'SP': {'lat': -23.155308, 'lon': -47.084074},
    'TO': {'lat': -9.503700, 'lon': -48.348661}
}

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "main_data.csv")
    df = pd.read_csv(path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    return df

df = load_data()

# Filter di Sidebar
st.sidebar.markdown("<h2 style='text-align: center; color: #3b82f6;'>⚙️ Filters</h2>", unsafe_allow_html=True)

min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Select Purchase Date Range:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

all_categories = sorted(df['product_category_name_english'].unique())
selected_categories = st.sidebar.multiselect(
    "Select Product Categories:",
    options=all_categories,
    default=[]
)

# Terapkan filter
filtered_df = df[
    (df['order_purchase_timestamp'] >= start_datetime) &
    (df['order_purchase_timestamp'] <= end_datetime)
]

if selected_categories:
    filtered_df = filtered_df[filtered_df['product_category_name_english'].isin(selected_categories)]

# Header dashboard
st.markdown("<h1 style='text-align: center; color: #3b82f6; font-weight: 700; margin-bottom: 30px;'>📊 E-Commerce Public Dataset Analysis</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 16px; margin-top: -20px;'>Analisis Kinerja Penjualan, RFM Pelanggan, dan Efisiensi Logistik (Periode: {start_date} s/d {end_date})</p>", unsafe_allow_html=True)

# Grid ringkasan metrik (KPI)
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['price'].sum()
total_orders = filtered_df['order_id'].nunique()
total_customers = filtered_df['customer_unique_id'].nunique()
avg_delivery = filtered_df['delivery_time'].mean() if len(filtered_df) > 0 else 0

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value">${total_revenue:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Orders</div>
            <div class="metric-value">{total_orders:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Active Customers</div>
            <div class="metric-value">{total_customers:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Delivery Time</div>
            <div class="metric-value">{avg_delivery:.2f} Days</div>
        </div>
    """, unsafe_allow_html=True)

# Tab navigasi
tab1, tab2, tab3 = st.tabs(["👥 RFM Customer Segmentation", "📍 Geospatial & Logistics", "📋 Strategic Action Items"])

with tab1:
    st.markdown("### Analisis Segmentasi Pelanggan (RFM)")
    
    if len(filtered_df) > 0:
        ref_date = filtered_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
        
        rfm_df = filtered_df.groupby('customer_unique_id').agg({
            'order_purchase_timestamp': lambda x: (ref_date - x.max()).days,
            'order_id': 'nunique',
            'price': 'sum'
        }).rename(columns={
            'order_purchase_timestamp': 'recency',
            'order_id': 'frequency',
            'price': 'monetary'
        }).reset_index()

        # Hitung skor RFM
        try:
            rfm_df['R_score'] = pd.qcut(rfm_df['recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
        except ValueError:
            rfm_df['R_score'] = pd.cut(rfm_df['recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
            
        rfm_df['F_score'] = rfm_df['frequency'].apply(lambda x: 1 if x == 1 else (3 if x == 2 else 5))
        
        try:
            rfm_df['M_score'] = pd.qcut(rfm_df['monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
        except ValueError:
            rfm_df['M_score'] = pd.cut(rfm_df['monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
            
        rfm_df['RFM_sum'] = rfm_df['R_score'] + rfm_df['F_score'] + rfm_df['M_score']

        def segment_rfm(row):
            score = row['RFM_sum']
            if score >= 11:
                return 'Champions'
            elif score >= 9:
                return 'Loyal Customers'
            elif score >= 7:
                return 'Promising'
            elif score >= 5:
                return 'At Risk / Need Attention'
            else:
                return 'Hibernating / Lost'

        rfm_df['segment'] = rfm_df.apply(segment_rfm, axis=1)

        rfm_agg = rfm_df.groupby('segment').agg({
            'customer_unique_id': 'count',
            'monetary': 'sum'
        }).rename(columns={'customer_unique_id': 'customer_count', 'monetary': 'total_revenue'}).reset_index()

        # Plot segmentasi
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig_cust = px.bar(
                rfm_agg,
                x='segment',
                y='customer_count',
                title='Distribution of Customers by RFM Segment',
                labels={'customer_count': 'Number of Customers', 'segment': 'RFM Segment'},
                color_discrete_sequence=['#3b82f6']
            )
            fig_cust.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#f8fafc')
            st.plotly_chart(fig_cust, use_container_width=True)
            
        with chart_col2:
            # Highlight Champions dan Loyal Customers, sisa segmen diberi warna netral abu-abu
            rfm_agg['color'] = rfm_agg['segment'].apply(lambda x: '#ef4444' if x == 'Champions' else ('#3b82f6' if x == 'Loyal Customers' else '#64748b'))
            fig_rev = px.bar(
                rfm_agg,
                x='segment',
                y='total_revenue',
                title='Total Revenue Contribution by RFM Segment',
                labels={'total_revenue': 'Total Revenue ($)', 'segment': 'RFM Segment'},
                color='color',
                color_discrete_map='identity'
            )
            fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#f8fafc', showlegend=False)
            st.plotly_chart(fig_rev, use_container_width=True)

        total_cust = rfm_df['customer_unique_id'].nunique()
        champs = rfm_agg[rfm_agg['segment'] == 'Champions']
        champs_count = champs['customer_count'].values[0] if len(champs) > 0 else 0
        champs_rev = champs['total_revenue'].values[0] if len(champs) > 0 else 0
        champs_rev_pct = (champs_rev / total_revenue) * 100 if total_revenue > 0 else 0
        
        st.info(f"💡 **Insight Segmentasi:** Kelompok **Champions** menyumbang sebesar **${champs_rev:,.2f}** ({champs_rev_pct:.1f}% dari pendapatan terfilter) meskipun hanya merepresentasikan **{champs_count:,}** pelanggan ({ (champs_count/total_cust)*100:.1f}% dari basis pelanggan).")
    else:
        st.warning("No data matches the selected filters.")

with tab2:
    st.markdown("### Analisis Geospasial & Kinerja Logistik")
    
    if len(filtered_df) > 0:
        state_stats = filtered_df.groupby('customer_state').agg({
            'delivery_time': 'mean',
            'order_id': 'count',
            'price': 'sum'
        }).rename(columns={'order_id': 'order_count', 'price': 'total_revenue'}).reset_index()

        geo_col1, geo_col2 = st.columns([3, 2])
        
        with geo_col1:
            st.markdown("#### Sebaran Volume Transaksi Pelanggan (Peta)")
            map_data = []
            for _, row in state_stats.iterrows():
                state = row['customer_state']
                if state in STATE_COORDS:
                    map_data.append({
                        'state': state,
                        'latitude': STATE_COORDS[state]['lat'],
                        'longitude': STATE_COORDS[state]['lon'],
                        'orders': row['order_count'],
                        'revenue': row['total_revenue'],
                        'delivery_time': row['delivery_time']
                    })
            map_df = pd.DataFrame(map_data)
            
            if not map_df.empty:
                st.map(map_df, latitude='latitude', longitude='longitude', size='orders', color='#3b82f6')
                st.caption("Ukuran lingkaran merepresentasikan jumlah volume pesanan (order volume) di negara bagian tersebut.")
            else:
                st.warning("No coordinates found for map mapping.")
                
        with geo_col2:
            st.markdown("#### 5 Negara Bagian dengan Waktu Pengiriman Terlama")
            slowest_5 = state_stats.sort_values(by='delivery_time', ascending=False).head(5)
            
            fig_slow = px.bar(
                slowest_5,
                x='delivery_time',
                y='customer_state',
                orientation='h',
                title='Top 5 Slowest States (Average Days)',
                labels={'delivery_time': 'Delivery Time (Days)', 'customer_state': 'State'},
                color_discrete_sequence=['#ef4444']
            )
            fig_slow.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#f8fafc')
            st.plotly_chart(fig_slow, use_container_width=True)
            
            st.warning(f"⚠️ **Keterlambatan Ekstrim:** Negara bagian **{slowest_5.iloc[0]['customer_state']}** memiliki waktu pengiriman rata-rata terlama mencapai **{slowest_5.iloc[0]['delivery_time']:.1f} hari**.")
    else:
        st.warning("No data matches the selected filters.")

with tab3:
    st.markdown("### Kesimpulan & Rekomendasi Bisnis Strategis")
    
    st.markdown("""
        <div class="recommendation-card">
            <h4>🎯 1. Strategi Segmentasi & Pemasaran Pelanggan (Q1)</h4>
            <ul>
                <li><b>Segmen Champions & Loyal Customers:</b> Berikan akses eksklusif untuk peluncuran produk baru, penawaran khusus tanpa minimal order, dan loyalty rewards. Retensi pelanggan di kedua segmen ini terbukti memberikan kontribusi pendapatan terbesar.</li>
                <li><b>Segmen Promising:</b> Dorong pembelian berikutnya dengan kampanye bundle atau bonus point rewards jika melakukan checkout kedua dalam rentang waktu singkat.</li>
                <li><b>Segmen At Risk / Need Attention:</b> Lakukan kampanye email re-engagement dengan memberikan kupon diskon "win-back" (misal: diskon 15%) untuk menarik mereka kembali berbelanja sebelum tergolong lost.</li>
            </ul>
        </div>
        
        <div class="recommendation-card" style="border-left-color: #ef4444;">
            <h4>🚚 2. Strategi Logistik & Pengiriman Wilayah Lambat (Q2)</h4>
            <ul>
                <li><b>Evaluasi Mitra Logistik:</b> Negara bagian di kawasan Utara/Timur Laut (seperti RR, AM, AP, PA) mencatat waktu pengiriman rata-rata sangat tinggi (>23 hari). Perlu dilakukan evaluasi service level agreement (SLA) vendor pengiriman di wilayah tersebut.</li>
                <li><b>Fulfillment Center Regional:</b> Mendirikan pusat distribusi regional (hub) di kota utama wilayah Utara untuk memangkas jarak pengiriman bagi barang-barang dengan kategori terpopuler.</li>
                <li><b>Integrasi Pilihan Pengiriman Lebih Cepat:</b> Sediakan opsi pengiriman kargo udara dengan biaya premium untuk pelanggan di kawasan luar pulau Jawa/Southeast yang membutuhkan barang segera.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Footer halaman
st.markdown("<hr style='border-color: #1e293b;'><p style='text-align: center; color: #64748b; font-size: 12px;'>Submission Analisis Data</p>", unsafe_allow_html=True)
