import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 全域 iPhone 玻璃風格核心設定 ---
st.set_page_config(page_title="iOS 顏色方塊謎題", page_icon="🟪", layout="wide", initial_sidebar_state="collapsed")

# 核心 CSS：抹除所有干擾字卡，並優化橫向排版
st.markdown("""
    <style>
    /* 仿 iOS 流光壁紙背景 */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #1a1b35 40%, #2c1b4d 70%, #111827 100%) !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        color: #f1f5f9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", sans-serif !important;
    }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }
    
    h1 {
        font-weight: 800 !important;
        font-size: 2.6rem !important;
        letter-spacing: -1px !important;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* iPhone 核心玻璃面板 */
    .ios-panel {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 24px !important;
        padding: 24px !important;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 24px;
    }
    
    /* 🔒 神秘箱子 */
    .box-hidden-ios {
        background: rgba(0, 0, 0, 0.35);
        border: 1.5px dashed rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 50px 20px;
        text-align: center;
        font-size: 18px;
        font-weight: 500;
        color: #94a3b8;
        box-shadow: inset 0 4px 20px rgba(0,0,0,0.6);
    }
    
    /* 📊 歷史紀錄卡片 */
    .ios-history-widget {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        padding: 14px !important;
        border-radius: 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15) !important;
    }
    
    .mini-jar-ios {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 6px;
        margin-right: 6px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.2), 0 2px 6px rgba(0,0,0,0.3);
    }

    /* 魔改拖曳組件外殼：完全透明不遮擋 */
    ul[data-testid="stSortablesList"] {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 16px !important;
        padding: 15px 0 !important;
        background: transparent !important;
    }
    
    li[data-testid="stSortablesItem"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        cursor: grab !important;
        transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    li[data-testid="stSortablesItem"]:active {
        cursor: grabbing !important;
        transform: scale(1.08) !important; /* 拖曳時輕微放大 */
    }

    /* 🎨 Apple 經典 3D 霓虹水晶方塊 */
    .custom-color-block {
        width: 100%;
        aspect-ratio: 1 / 1; /* 保持絕對正方形 */
        border-radius: 22px;
        box-shadow: inset 0 6px 12px rgba(255,255,255,0.4), 0 10px 24px rgba(0,0,0,0.4);
        border: 1.5px solid rgba(255, 255, 255, 0.5);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .custom-color-block:hover {
        border-color: rgba(255, 255, 255, 0.8);
    }

    /* Apple 膠囊按鈕 */
    .stButton>button {
        border-radius: 16px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #007aff 0%, #0056b3 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,122,255,0.3) !important;
    }
    .stButton>button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #f1f5f9 !important;
    }
    
    /* 側邊欄抽屜 */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 顏色庫定義 (10 種高飽和度 iOS 霓虹色彩)
COLOR_MAP = {
    "翡翠綠": "#34c759", "天青藍": "#007aff", "極光紫": "#af52de", 
    "烈焰紅": "#ff3b30", "活力橙": "#ff9500", "璀璨黃": "#ffcc00",
    "櫻花粉": "#ff2d55", "深海藍": "#5856d6", "薄荷綠": "#64d2ff", "巧克力": "#a2845e"
}
COLOR_LIST = list(COLOR_MAP.keys())

# --- 3. 初始化遊戲狀態 ---
if "secret_sequence" not in st.session_state:
    st.session_state.difficulty = 4
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:st.session_state.difficulty], st.session_state.difficulty)
    st.session_state.player_sequence = list(COLOR_LIST[:st.session_state.difficulty])
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

def reset_game(difficulty_num):
    st.session_state.difficulty = difficulty_num
    st.session_state.secret_sequence = random.sample(COLOR_LIST[:difficulty_num], difficulty_num)
    st.session_state.player_sequence = list(COLOR_LIST[:difficulty_num])
    st.session_state.history = []
    st.session_state.show_answer = False
    st.session_state.game_over = False

# --- 4. UI 畫面渲染 ---
st.title("🧪 顏色方塊謎題")
st.write("")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 遊戲設定")
    new_diff = st.slider("選擇遊戲難度 (方塊數量)", min_value=3, max_value=10, value=st.session_state.difficulty)
    
    if new_diff != st.session_state.difficulty:
        reset_game(new_diff)
        st.rerun()
        
    if st.button("🔄 重新開啟新局", use_container_width=True):
        reset_game(st.session_state.difficulty)
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 💡 玩法說明")
    st.markdown("1. 在 **「玩家操作區」** 直接拖曳**彩色方塊**調整左右順序。\n"
                "2. 沒有任何文字提示，完全依賴你的視覺記憶！\n"
                "3. 調整完畢後，點擊下方 **「確定檢查！」** 提交答案。")

# 主畫面排版
col_main, col_hist = st.columns([78, 22])

with col_main:
    # 區塊 A：神秘箱子區
    st.markdown('<div class="ios-panel">', unsafe_allow_html=True)
    st.subheader("📦 神秘箱子")
    
    if st.session_state.show_answer or st.session_state.game_over:
        cols = st.columns(st.session_state.difficulty)
        for i, color_name in enumerate(st.session_state.secret_sequence):
            with cols[i]:
                color_code = COLOR_MAP[color_name]
                st.markdown(f'''
                    <div style="text-align: center; width:100%;">
                        <div class="custom-color-block" style="background: linear-gradient(to top, {color_code} 85%, rgba(255,255,255,0.2) 100%);"></div>
                    </div>
                ''', unsafe_allow_html=True)
        if st.session_state.game_over:
            st.success(f"🎉 恭喜闖關成功！共花費了 {len(st.session_state.history)} 個回合！")
    else:
        st.markdown(f'<div class="box-hidden-ios">🔒 箱內藏有 {st.session_state.difficulty} 個顏色的隱藏順序</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 區塊 B：玩家操作區
    st.markdown('<div class="ios-panel">', unsafe_allow_html=True)
    st.subheader("🖐️ 玩家操作區")
    st.caption("直接左右拖曳下方的彩色方塊來調整順序：")
    st.write("")
    
    # 核心設計：只生成純顏色 3D 方塊，不顯示任何文字，並偷偷附帶色標碼供後端辨識
    visual_block_items = []
    for name in st.session_state.player_sequence:
        color_code = COLOR_MAP[name]
        block_html_string = f'''
        <div style="text-align: center; width: 100%;">
            <div class="custom-color-block" style="background: linear-gradient(to top, {color_code} 85%, rgba(255,255,255,0.2) 100%);"></div>
            <span style="display:none;">[BLOCK_ID:{name}]</span>
        </div>
        '''
        visual_block_items.append(block_html_string)
    
    # 橫向拖曳引擎
    sort_key = f"ios_block_engine_{len(st.session_state.history)}"
    sorted_res = sort_items(visual_block_items, direction="horizontal", key=sort_key)
    
    # 後端讀取拖曳後的新順序
    if sorted_res:
        new_order = []
        for html_item in sorted_res:
            if "[BLOCK_ID:" in html_item:
                color_name = html_item.split("[BLOCK_ID:")[1].split("]")[0]
                new_order.append(color_name)
        if len(new_order) == st.session_state.difficulty:
            st.session_state.player_sequence = new_order

    st.write("")
    st.write("")
    
    # iOS 操作主按鈕列
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("確定檢查！", type="primary", use_container_width=True, disabled=st.session_state.game_over):
            current_order = list(st.session_state.player_sequence)
            correct_count = sum(1 for p, s in zip(current_order, st.session_state.secret_sequence) if p == s)
            
            st.session_state.history.append({
                "round": len(st.session_state.history) + 1,
                "sequence": current_order,
                "correct": correct_count
            })
            
            if correct_count == st.session_state.difficulty:
                st.session_state.game_over = True
            st.rerun()

    with btn_col2:
        if st.button("揭曉神秘箱答案", type="secondary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_hist:
    # 右側 iOS 歷史紀錄面板
    st.subheader("📊 歷史紀錄")
    if not st.session_state.history:
        st.info("暫無紀錄")
    else:
        for record in reversed(st.session_state.history):
            block_htmls = ""
            for name in record["sequence"]:
                code = COLOR_MAP.get(name, "#ffffff")
                block_htmls += f'<div class="mini-jar-ios" style="background-color: {code};"></div>'
                
            st.markdown(f'''
                <div class="ios-history-widget">
                    <div style="font-weight:600; font-size:12px; margin-bottom:6px; display:flex; justify-content:space-between; color:#94a3b8;">
                        <span>第 {record["round"]} 回合</span>
                        <span style="color:#007aff;">🎯 {record["correct"]} 對</span>
                    </div>
                    <div style="display:flex; flex-wrap:nowrap; overflow:hidden;">{block_htmls}</div>
                </div>
            ''', unsafe_allow_html=True)
