import streamlit as st
import random
from streamlit_sortables import sort_items

# --- 1. 全域 iPhone 玻璃風格核心設定 ---
st.set_page_config(page_title="iOS 顏色罐子謎題", page_icon="🧪", layout="wide", initial_sidebar_state="collapsed")

# 核心 CSS：將第三方元件的突兀字卡「完全隱形化」，只留下我們自訂的 3D 玻璃罐子
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
        width: 16px;
        height: 24px;
        border-radius: 5px;
        margin-right: 5px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.2), 0 2px 6px rgba(0,0,0,0.3);
    }

    /* 🪄 核心魔改：把 `streamlit_sortables` 原本醜陋的預設外殼徹底抹除 */
    ul[data-testid="stSortablesList"] {
        display: flex !important;
        flex-direction: row !important; /* 橫向排列 */
        justify-content: space-between !important;
        gap: 16px !important;
        padding: 15px 0 !important;
        background: transparent !important;
    }
    
    li[data-testid="stSortablesItem"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
        
        /* 🔥 關鍵：將第三方元件內建的背景色、邊框、陰影全部拔除變透明，不干擾視線 */
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        
        cursor: grab !important;
        transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* 當玩家正在拖曳某個罐子時的 iPhone 縮放物理動態反饋 */
    li[data-testid="stSortablesItem"]:active {
        cursor: grabbing !important;
        transform: scale(1.08) !important; /* 拖曳時罐子微微放大，極具觸控感 */
    }

    /* 🎨 自訂 3D 霓虹水晶玻璃罐子本體樣式 */
    .custom-jar {
        text-align: center;
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 16px 8px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        transition: border-color 0.2s ease;
    }
    .custom-jar:hover {
        border-color: rgba(255, 255, 255, 0.3);
    }

    /* Apple 膠囊按鈕基底 */
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
st.title("🧪 顏色罐子謎題")
st.write("")

# 側邊欄設定
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
    st.markdown("1. 在 **「玩家操作區」** 直接用滑鼠或手指**左右拖曳罐子**調整順序。\n"
                "2. 調整完畢後，點擊下方 **「確定檢查！」** 提交答案。\n"
                "3. 右側歷史紀錄會即時且完美精準地同步。")

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
                        <div style="width: 46%; height: 10px; background: rgba(255,255,255,0.4); border-radius: 5px; margin: 0 auto -2px auto; max-width: 32px;"></div>
                        <div style="width: 85%; height: 95px; border-radius: 18px; box-shadow: inset 0 4px 8px rgba(255,255,255,0.4), 0 8px 20px rgba(0,0,0,0.4); border: 1.5px solid rgba(255,255,255,0.7); background: linear-gradient(to top, {color_code} 85%, rgba(255,255,255,0.15) 100%); margin: 0 auto; max-width: 55px;"></div>
                        <p style="margin-top:8px; font-weight:600; font-size:12px; color:#e2e8f0; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">{color_name}</p>
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
    st.caption("按住下方的罐子卡片，直接左右拖曳來調整你心目中的正確順序：")
    st.write("")
    
    # 巧妙設計：雖然組件只收純字串，但 Streamlit 的 Markdown 渲染器非常強大，
    # 我們可以直接把完整的「3D 霓虹毛玻璃罐子 HTML 代碼」當作字串丟進 `sort_items`！
    # 這樣組件在渲染時，就會完美呈現出漂亮的罐子，同時完全保留手勢拖曳功能！
    visual_jar_items = []
    for name in st.session_state.player_sequence:
        color_code = COLOR_MAP[name]
        jar_html_string = f'''
        <div class="custom-jar">
            <div style="width: 46%; height: 8px; background: rgba(255,255,255,0.4); border-radius: 4px; margin: 0 auto -2px auto; max-width: 28px;"></div>
            <div style="width: 80%; height: 85px; border-radius: 16px; box-shadow: inset 0 4px 10px rgba(255,255,255,0.5), 0 8px 20px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.6); background: linear-gradient(to top, {color_code} 85%, rgba(255,255,255,0.15) 100%); margin: 0 auto; max-width: 50px;"></div>
            <p style="margin-top:8px; font-weight:700; font-size:13px; color:#cbd5e1; margin-bottom:0; text-shadow: 0 2px 4px rgba(0,0,0,0.5); letter-spacing:-0.2px;">{name}</p>
            <span style="display:none;">[COLOR_ID:{name}]</span>
        </div>
        '''
        visual_jar_items.append(jar_html_string)
    
    # 調用官方專利拖曳排序器 (使用唯一 key 防止回合殘留快取)
    sort_key = f"ios_sortable_engine_{len(st.session_state.history)}"
    sorted_res = sort_items(visual_jar_items, direction="horizontal", key=sort_key)
    
    # 【Bug 終結核心點】：從拖曳後的 HTML 字串中，精準解析出玩家最新排列的顏色順序並存回 Python 狀態
    if sorted_res:
        new_order = []
        for html_item in sorted_res:
            if "[COLOR_ID:" in html_item:
                color_name = html_item.split("[COLOR_ID:")[1].split("]")[0]
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
            
            # 100% 精準計算完全正確的數量
            correct_count = sum(1 for p, s in zip(current_order, st.session_state.secret_sequence) if p == s)
            
            # 寫入歷史紀錄
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
            jar_htmls = ""
            for name in record["sequence"]:
                code = COLOR_MAP.get(name, "#ffffff")
                jar_htmls += f'<div class="mini-jar-ios" style="background-color: {code};" title="{name}"></div>'
                
            st.markdown(f'''
                <div class="ios-history-widget">
                    <div style="font-weight:600; font-size:12px; margin-bottom:6px; display:flex; justify-content:space-between; color:#94a3b8;">
                        <span>第 {record["round"]} 回合</span>
                        <span style="color:#007aff;">🎯 {record["correct"]} 對</span>
                    </div>
                    <div style="display:flex; flex-wrap:nowrap; overflow:hidden;">{jar_htmls}</div>
                </div>
            ''', unsafe_allow_html=True)
