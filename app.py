import streamlit as st
import random

# 必須先安裝 streamlit-sortable： pip install streamlit-sortable
from streamlit_sortable import sortable

# --- 1. 頁面佈局與流暢 UI 樣式設定 ---
st.set_page_config(page_title="顏色罐子猜謎遊戲", page_icon="🧪", layout="wide")

# 使用 CSS 強化顏色罐子的 3D 視覺質感與流暢動畫
st.markdown("""
    <style>
    .jar-wrapper {
        display: inline-block;
        margin: 5px;
        text-align: center;
    }
    .color-jar {
        width: 70px;
        height: 100px;
        border-radius: 15px 15px 25px 25px;
        box-shadow: inset 0 5px 10px rgba(255,255,255,0.6), 
                    inset 0 -10px 20px rgba(0,0,0,0.3),
                    0 6px 12px rgba(0,0,0,0.15);
        border: 2px solid #ffffff;
        position: relative;
        cursor: grab;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .color-jar:active { cursor: grabbing; transform: scale(1.05); }
    .jar-lid {
        width: 44px;
        height: 12px;
        background: #d1d5db;
        border-radius: 6px;
        margin: 0 auto -2px auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .box-hidden {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: #94a3b8;
        border: 3px dashed #334155;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: inset 0 4px 10px rgba(0,0,0,0.5);
    }
    .history-card {
        background-color: #f8fafc;
        border-left: 5px solid #6366f1;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .mini-jar {
        display: inline-block;
        width: 20px;
        height: 30px;
        border-radius: 4px;
        margin-right: 4px;
        border: 1px solid #cbd5e1;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 顏色庫定義 (支援到 10 種鮮明不重複顏色)
COLOR_MAP = {
    "翡翠綠": "#10B981", "天青藍": "#3B82F6", "極光紫": "#8B5CF6", 
    "烈焰紅": "#EF4444", "活力橙": "#F97316", "璀璨黃": "#F59E0B",
    "櫻花粉": "#EC4899", "深海藍": "#1E3A8A", "薄荷綠": "#A7F3D0", "巧克力": "#78350F"
}
COLOR_LIST = list(COLOR_MAP.keys())

# --- 3. 初始化遊戲狀態 (Session State) ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:st.session_state.difficulty], st.session_state.difficulty)
    st.session_state.player_sequence = COLOR_LIST[:st.session_state.difficulty]
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# 重置遊戲函數
def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:difficulty_num], difficulty_num)
    st.session_state.player_sequence = COLOR_LIST[:difficulty_num]
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 4. UI 畫面渲染 ---
st.title("🧪 3D 顏色罐子猜謎遊戲")
st.caption("透過極致順暢的拖曳排序，用最少的回合找出神秘箱子裡的正確顏色順序吧！")

# 側邊欄：控制面板
with st.sidebar:
    st.header("⚙️ 遊戲設定")
    new_diff = st.slider("選擇遊戲難度 (罐子數量)", min_value=3, max_value=10, value=st.session_state.difficulty)
    
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    if st.button("🔄 重新開啟新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 💡 玩法說明")
    st.markdown("1. 在右側 **「玩家操作區」** 直接**拖曳**卡片或罐子來調整左右順序。\n"
                "2. 調整完畢後，點擊下方 **「確定檢查」** 提交答案。\n"
                "3. 系統會提示有幾個罐子**「顏色與位置完全正確」**。\n"
                "4. 點擊 **「揭曉神祕箱」** 可直接偷看正確答案。")

# 主畫面分欄：左邊遊戲操作，右邊歷史紀錄
col_main, col_hist = st.columns([7, 3])

with col_main:
    # 區塊 A：神秘箱子 (隱藏答案區)
    st.subheader("📦 神秘箱子 (隱藏答案)")
    if st.session_state.show_answer or st.session_state.game_over:
        # 揭曉答案
        cols = st.columns(st.session_state.difficulty)
        for i, color_name in enumerate(st.session_state.secret_sequence):
            with cols[i]:
                color_code = COLOR_MAP[color_name]
                st.markdown(f'''
                    <div class="jar-wrapper">
                        <div class="jar-lid"></div>
                        <div class="color-jar" style="background: linear-gradient(to top, {color_code} 80%, rgba(255,255,255,0.3) 100%);"></div>
                        <p style="margin-top:5px; font-weight:bold; font-size:14px;">{color_name}</p>
                    </div>
                ''', unsafe_allow_html=True)
        if st.session_state.game_over:
            st.success(f"🎉 恭喜闖關成功！共花費了 {len(st.session_state.history)} 個回合！")
    else:
        # 箱子關閉狀態
        st.markdown(f'<div class="box-hidden">🔒 裡面藏著 {st.session_state.difficulty} 個顏色的神祕順序</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("---")

    # 區塊 B：玩家操作區（可拖曳）
    st.subheader("🖐️ 玩家操作區 (請上下/左右拖曳進行排序)")
    
    # 建立適合 sortable 組件的資料結構 (包含 HTML 渲染)
    items_to_sort = []
    for color_name in st.session_state.player_sequence:
        color_code = COLOR_MAP[color_name]
        html_content = f'''
            <div style="display:inline-flex; align-items:center; background:#1e293b; padding:10px 20px; border-radius:10px; margin:2px; border:1px solid #475569; width:100%;">
                <div style="width:24px; height:34px; border-radius:6px; background:{color_code}; margin-right:15px; box-shadow:0 2px 4px rgba(0,0,0,0.3);"></div>
                <span style="color:white; font-weight:bold; font-size:16px;">{color_name}</span>
            </div>
        '''
        items_to_sort.append({"id": color_name, "content": html_content})

    # 執行拖曳元件 (這裡回傳排序後的 id 清單)
    sorted_labels = sortable(items_to_sort, direction="vertical")
    
    if sorted_labels:
        st.session_state.player_sequence = sorted_labels

    st.write("")
    
    # 動作按鈕列
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("確定檢查！確認目前順序", type="primary", use_container_width=True, disabled=st.session_state.game_over):
            # 計算完全正確的數量 (位置與顏色皆同)
            correct_count = sum(1 for p, s in zip(st.session_state.player_sequence, st.session_state.secret_sequence) if p == s)
            
            # 紀錄至歷史
            st.session_state.history.append({
                "round": len(st.session_state.history) + 1,
                "sequence": list(st.session_state.player_sequence),
                "correct": correct_count
            })
            
            # 判斷是否全對
            if correct_count == st.session_state.difficulty:
                st.session_state.game_over = True
            st.rerun()

    with btn_col2:
        if st.button("👁️ 揭曉神祕箱答案", type="secondary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()

with col_hist:
    # 區塊 C：右側歷史紀錄看板
    st.subheader("📊 歷史嘗試紀錄")
    if not st.session_state.history:
        st.info("尚無回合紀錄，調整好上方順序後按下確定吧！")
    else:
        # 由新到舊排序顯示
        for record in reversed(st.session_state.history):
            jar_htmls = ""
            for name in record["sequence"]:
                code = COLOR_MAP[name]
                jar_htmls += f'<div class="mini-jar" style="background-color: {code};" title="{name}"></div>'
                
            st.markdown(f'''
                <div class="history-card">
                    <div style="display:flex; justify-content:between; font-weight:bold; margin-bottom:5px;">
                        <span style="color:#1e3a8a;">第 {record["round"]} 回合</span>
                        <span style="margin-left:auto; color:#b45309;">🎯 {record["correct"]} 個正確</span>
                    </div>
                    <div>{jar_htmls}</div>
                </div>
            ''', unsafe_allow_html=True)
