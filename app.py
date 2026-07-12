import streamlit as st
import requests
import time

st.set_page_config(page_title="2026世界盃與全球運動運彩娛樂城 (GM控制版)", page_icon="🏆", layout="wide")

# 初始化 session 狀態
if "balance" not in st.session_state:
    st.session_state.balance = 10000
if "bets" not in st.session_state:
    st.session_state.bets = []
if "history" not in st.session_state:
    st.session_state.history = []
if "live_games" not in st.session_state:
    st.session_state.live_games = {}
if "available_sports" not in st.session_state:
    st.session_state.available_sports = []

# 聯賽中文化映射 - 榮譽加入 2026 FIFA 世界盃
LEAGUE_TRANSLATION = {
    "soccer_fifa_world_cup": "🏆 2026 FIFA 世界盃足球賽 (World Cup) 🏆",
    "baseball_mlb": "美國職棒 (MLB) ⚾",
    "basketball_nba": "美國職籃 (NBA) 🏀",
    "baseball_npb": "日本職棒 (NPB) ⚾",
    "soccer_epl": "英格蘭超級聯賽 (EPL) ⚽",
    "soccer_uefa_champs_league": "歐洲冠軍聯賽 (UEFA) ⚽",
    "icehockey_nhl": "北美冰球聯盟 (NHL) 🏒",
    "americanfootball_nfl": "美式足球聯盟 (NFL) 🏈",
    "tennis_atp_us_open": "美國網球公開賽 (ATP) 🎾"
}

st.title("⚽ 2026 美加墨世界盃特開版 — 全球運動運彩系統")
st.markdown("🔥 **時事追蹤**：目前正值 2026 年盛夏，世界盃足球賽火熱開踢中！點擊下方按鈕獲取最新國際盤口。")

# 側邊欄：帳戶資訊
with st.sidebar:
    st.header("⚙️ 帳戶與系統設定")
    API_KEY = st.text_input("輸入 The Odds API Key", value="d2af9efaf974ed4731a3aebdab5a1021", type="password")
    st.markdown("---")
    st.metric(label="💰 目前帳戶可用餘額", value=f"${st.session_state.balance:,} 元")
    
    if st.button("🌐 重新同步全球即時賽事項目", type="primary", use_container_width=True):
        if not API_KEY:
            st.error("請先輸入 API Key！")
        else:
            with st.spinner("正在探測全球體育市場..."):
                url = f"https://api.the-odds-api.com/v4/sports/?apiKey={API_KEY}"
                try:
                    res = requests.get(url, timeout=10)
                    if res.status_code == 200:
                        active_sports = [s for s in res.json() if s.get("active", True)]
                        st.session_state.available_sports = active_sports
                        st.toast(f"✅ 成功載入當前包含「世界盃」在內的 {len(active_sports)} 個熱門項目！")
                    else: st.error("無法取得運動清單。")
                except Exception as e: st.error(f"連線失敗: {str(e)}")

# 建立分頁
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 即時盤口大廳", "📋 購物車/未結注單", "🎯 同步現實開獎", "📈 歷史帳戶對帳單", "👑 莊家GM控制台"])

# ----------------- TAB 1: 即時盤口大廳 -----------------
with tab1:
    main_col, side_slip = st.columns([0.7, 0.3])
    with main_col:
        if not st.session_state.available_sports:
            st.info("👋 歡迎！請先點擊左側邊欄的 **「🌐 重新同步全球即時賽事項目」** 按鈕，獲取 2026 世界盃與全球即時盤口！")
        else:
            sport_options = {s["key"]: LEAGUE_TRANSLATION.get(s["key"], f"⚽ {s['title']}") for s in st.session_state.available_sports}
            
            # 如果世界盃在清單中，我們把它強制排在第一個，方便一進來就下注世足
            sorted_keys = list(sport_options.keys())
            if "soccer_fifa_world_cup" in sorted_keys:
                sorted_keys.remove("soccer_fifa_world_cup")
                sorted_keys.insert(0, "soccer_fifa_world_cup")
                
            selected_sport_key = st.selectbox("選擇即時時事聯賽", sorted_keys, format_func=lambda x: sport_options[x], label_visibility="collapsed")
            
            if st.button("🔄 刷新當前水位", type="primary"):
                with st.spinner("正在向拉斯維加斯盤口中心更新最新水位..."):
                    url = f"https://api.the-odds-api.com/v4/sports/{selected_sport_key}/odds/?apiKey={API_KEY}&regions=us&markets=h2h,spreads,totals&oddsFormat=decimal"
                    try:
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            st.session_state.live_games[selected_sport_key] = response.json()
                            st.toast("✅ 最新世界盃/聯賽水位同步完成！")
                    except: st.error("網路連線超時。")

            current_games = st.session_state.live_games.get(selected_sport_key, [])
            if not current_games and selected_sport_key == "soccer_fifa_world_cup":
                st.warning("⚽ 目前世界盃此時此刻可能正處於兩場比賽中間的空檔，或是今日賽事已封盤。你可以稍後刷新，或先遊玩其他即時熱門賽事！")
                
            for game in current_games[:8]:
                game_id, home, away = game["id"], game["home_team"], game["away_team"]
                h2h = {home: 1.90, away: 1.90, "Draw": 3.25}
                if game.get("bookmakers"):
                    for m in game["bookmakers"][0].get("markets", []):
                        if m["key"] == "h2h":
                            for o in m["outcomes"]: h2h[o["name"]] = o["price"]

                with st.container(border=True):
                    st.markdown(f"#### 🌍 {home} vs {away}")
                    
                    c_h2h_1, c_h2h_2, c_h2h_3 = st.columns(3)
                    with c_h2h_1:
                        if st.button(f"主勝 {h2h.get(home, 1.90)}", key=f"h_{game_id}", use_container_width=True):
                            st.session_state.active_bet = {"id": game_id, "sport": selected_sport_key, "type": "獨贏", "pick": home, "odds": h2h.get(home, 1.90), "desc": f"{home} vs {away}", "condition": 0.0}
                    with c_h2h_2:
                        # 足球賽果靈魂：和局盤
                        draw_p = h2h.get("Draw") or h2h.get("Tie") or 3.25
                        if st.button(f"和局 {draw_p}", key=f"d_{game_id}", use_container_width=True):
                            st.session_state.active_bet = {"id": game_id, "sport": selected_sport_key, "type": "獨贏", "pick": "和局", "odds": draw_p, "desc": f"{home} vs {away}", "condition": 0.0}
                    with c_h2h_3:
                        if st.button(f"客勝 {h2h.get(away, 1.90)}", key=f"a_{game_id}", use_container_width=True):
                            st.session_state.active_bet = {"id": game_id, "sport": selected_sport_key, "type": "獨贏", "pick": away, "odds": h2h.get(away, 1.90), "desc": f"{home} vs {away}", "condition": 0.0}

    with side_slip:
        st.subheader("📝 快速下注單")
        if "active_bet" in st.session_state:
            b = st.session_state.active_bet
            with st.container(border=True):
                st.markdown(f"**{b['desc']}**\n\n預測標的：`{b['pick']}`\n\n即時賠率：<span style='color:#ff4b4b;font-weight:bold;font-size:20px;'>{b['odds']}</span>", unsafe_html=True)
                amount = st.number_input("投注本金 (NTD)", min_value=100, value=100, step=100)
                
                est_return = round(amount * b['odds'])
                st.markdown(f"🎯 預估回報：**${est_return:,} 元**")
                
                if st.button("🔥 確認送出注單", type="primary", use_container_width=True):
                    if st.session_state.balance >= amount:
                        st.session_state.balance -= amount
                        st.session_state.bets.append({
                            "game_id": b["id"], "sport": b["sport"], "type": b["type"],
                            "desc": b["desc"], "pick": b["pick"], "odds": b["odds"],
                            "amount": amount, "condition": b["condition"], "time": time.strftime("%X")
                        })
                        st.success("✅ 注單已成功送進核心系統！")
                        del st.session_state.active_bet
                        st.rerun()
                    else: st.error("餘額不足！")
        else: st.info("請點選左側賠率水位按鈕。")

# ----------------- TAB 2 & 3 & 4 -----------------
with tab2:
    st.subheader("📋 帳戶未結注單")
    for b in st.session_state.bets:
        st.write(f"📌 {b['desc']} ｜ 預測: {b['pick']} ｜ 金額: ${b['amount']}")

with tab3:
    st.subheader("🎯 同步現實開獎 (世界盃賽果同步)")
    if st.button("🚀 接入現實世界比分進行世界盃派彩", type="secondary", use_container_width=True):
        if not st.session_state.bets: st.warning("您目前沒有任何在外馳騁的注單。")
        else:
            with st.spinner("正在向世界盃官方數據庫對接比分..."):
                kept_bets = []
                needed_sports = set([b["sport"] for b in st.session_state.bets])
                scores_data = {}
                for sport in needed_sports:
                    url = f"https://api.the-odds-api.com/v4/sports/{sport}/scores/?apiKey={API_KEY}&daysFrom=2" 
                    try:
                        res = requests.get(url, timeout=10)
                        if res.status_code == 200: scores_data[sport] = res.json()
                    except: pass
                
                for b in st.session_state.bets:
                    sport_scores = scores_data.get(b["sport"], [])
                    match_found = False
                    for game in sport_scores:
                        if game["id"] == b["game_id"] and game["completed"]:
                            match_found = True
                            s = game["scores"]
                            if s and len(s) == 2:
                                home_score = next((int(x["score"]) for x in s if x["name"] == game["home_team"]), 0)
                                away_score = next((int(x["score"]) for x in s if x["name"] == game["away_team"]), 0)
                                result_status = "lose"
                                
                                if b["pick"] in ["和局", "Draw", "Tie"]:
                                    if home_score == away_score: result_status = "win"
                                elif b["pick"] == game["home_team"] and home_score > away_score: result_status = "win"
                                elif b["pick"] == game["away_team"] and away_score > home_score: result_status = "win"
                                
                                payoff = round(b["amount"] * b["odds"]) if result_status == "win" else 0
                                st.session_state.balance += payoff
                                st.session_state.history.append({"desc": b["desc"], "type": b["type"], "pick": b["pick"], "amount": b["amount"], "payoff": payoff, "result": result_status, "score": f"{home_score}:{away_score}"})
                                if result_status == "win": st.success(f"🎉 世界盃狂歡！【{b['desc']}】最終比分 {home_score}:{away_score}。過盤贏得 ${payoff} 元！")
                                else: st.error(f"💀 殘念！【{b['desc']}】最終比分 {home_score}:{away_score}。未過盤。")
                            break
                    if not match_found:
                        st.info(f"⏳ 【{b['desc']}】賽事尚未完賽，注單繼續保留。")
                        kept_bets.append(b)
                st.session_state.bets = kept_bets
                st.rerun()

with tab4:
    st.subheader("📈 歷史帳戶對帳單")
    for h in reversed(st.session_state.history):
        st.write(f"⚖️ {h['desc']} ｜ 賽果: {h['score']} ｜ 損益: `${h['payoff']-h['amount']}` ({h['result']})")

# ----------------- 👑 TAB 5: 莊家 GM 控制台 -----------------
with tab5:
    st.subheader("👑 莊家至高無上神之權限後台 (可手動強開世界盃)")
    new_bal = st.number_input("設定玩家錢包新餘額 (元)", min_value=0, value=int(st.session_state.balance), step=1000)
    if st.button("🪄 瞬間修改餘額", type="primary"):
        st.session_state.balance = new_bal
        st.rerun()
        
    st.write("---")
    st.markdown("### 🎲 暗箱操作欄")
    if not st.session_state.bets: st.info("目前沒有任何未結注單。")
    else:
        for idx, b in enumerate(st.session_state.bets):
            with st.container(border=True):
                st.write(f"**單號 #{idx+1}：{b['desc']}** (預測: {b['pick']}, 金額: ${b['amount']})")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"🟩 強制判定：過盤(贏)", key=f"gm_w_{idx}"):
                        payoff = round(b["amount"] * b["odds"])
                        st.session_state.balance += payoff
                        st.session_state.history.append({"desc": b["desc"], "type": b["type"], "pick": b["pick"], "amount": b["amount"], "payoff": payoff, "result": "win (莊家強開)", "score": "後台控制"})
                        st.session_state.bets.pop(idx)
                        st.rerun()
                with c2:
                    if st.button(f"🟥 強制判定：槓龜(輸)", key=f"gm_l_{idx}"):
                        st.session_state.history.append({"desc": b["desc"], "type": b["type"], "pick": b["pick"], "amount": b["amount"], "payoff": 0, "result": "lose (莊家強開)", "score": "後台控制"})
                        st.session_state.bets.pop(idx)
                        st.rerun()
