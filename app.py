import streamlit as st
import pandas as pd

# 1. 繁體中文黑金風格 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #d4af37; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    div[data-testid="stSidebar"] { background-color: #1a1a1a; }
    .stButton>button { width: 100%; background-color: #d4af37; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 2026 全球頂級運彩交易中心")

# 2. 中文化多樣賽事系統
st.sidebar.header("賽事導覽")
sport_type = st.sidebar.selectbox("選擇賽事項目", ["世界盃足球", "MLB 美國職棒", "NBA 籃球", "熱門電競"])
st.subheader(f"當前盤口：{sport_type}")

# 模擬賠率資料 (中文化)
odds_data = {"比賽隊伍": ["地主強隊", "客場挑戰者"], "即時賠率": [1.95, 1.85]}
df = pd.DataFrame(odds_data)
st.table(df)

# 3. 中文化自動損益結算邏輯
if 'balance' not in st.session_state: st.session_state.balance = 50000

st.write(f"### 您的帳戶餘額: ${st.session_state.balance:,.2f}")
bet_amount = st.number_input("請輸入投注金額 (USD)", min_value=100, step=100)

if st.button("確認下注"):
    if bet_amount <= st.session_state.balance:
        st.session_state.balance -= bet_amount
        st.success(f"下注成功！已扣除 ${bet_amount}。剩餘額度: ${st.session_state.balance:,.2f}")
    else:
        st.error("餘額不足，請重新輸入金額。")