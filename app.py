import streamlit as st
import random

st.set_page_config(page_title="⚾ シンプル野球ゲーム")

st.markdown("<h2 style='text-align:center;'>⚾ 野球スコアゲーム</h2>", unsafe_allow_html=True)

# -------------------------
# セッション初期化
# -------------------------
if "inning" not in st.session_state:
    st.session_state.inning = 1
if "top" not in st.session_state:
    st.session_state.top = True
if "scores_top" not in st.session_state:
    st.session_state.scores_top = [None] * 9
if "scores_bottom" not in st.session_state:
    st.session_state.scores_bottom = [None] * 9
if "finished" not in st.session_state:
    st.session_state.finished = False
if "current_inning" not in st.session_state:
    st.session_state.current_inning = 1
if "current_half" not in st.session_state:
    st.session_state.current_half = "top"


# -------------------------
# チーム名入力
# -------------------------
team_top = st.text_input("先攻チーム名（表）", value="チームA")
team_bottom = st.text_input("後攻チーム名（裏）", value="チームB")

st.divider()

# -------------------------
# 現在の回表示
# -------------------------
if not st.session_state.finished:
    half = "表" if st.session_state.top else "裏"
    st.subheader(f"{st.session_state.inning}回 {half}")

# -------------------------
# 次へボタン
# -------------------------
def animate_score():
    box = st.empty()

    # 数字ルーレット（2秒）
    for _ in range(20):  # 0.1 × 20 = 2秒
        box.markdown(
            f"<div style='font-size:36px; font-weight:bold; text-align:center;'>"
            f"{random.randint(0,5)}</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.1)

    # 最終得点（確率調整）
    final_score = random.choices(
        [0,1,2,3,4,5],
        weights=[0.35,0.30,0.18,0.10,0.05,0.02],
        k=1
    )[0]

    box.markdown(
        f"<div style='font-size:36px; font-weight:bold; text-align:center; color:#e63946;'>"
        f"{final_score}</div>",
        unsafe_allow_html=True
    )

    time.sleep(0.5)
    box.empty()

    return final_score
    
if st.button("▶ 次のイニング"):
    inning = st.session_state.current_inning - 1
    half = st.session_state.current_half

    score = animate_score()
    st.session_state.scoreboard[half][inning] = score

    # 表 → 裏 → 次の回
    if half == "top":
        st.session_state.current_half = "bottom"
    else:
        st.session_state.current_half = "top"
        st.session_state.current_inning += 1

# -------------------------
# スコアボード表示
# -------------------------
top_scores = st.session_state.scoreboard["top"]
bottom_scores = st.session_state.scoreboard["bottom"]

top_total = sum(s if isinstance(s, int) else 0 for s in top_scores)
bottom_total = sum(s if isinstance(s, int) else 0 for s in bottom_scores)


# -------------------------
# 勝敗判定
# -------------------------
if st.session_state.finished:
    st.divider()
    if top_total > bottom_total:
        st.success(f"🏆 勝利：{team_top}")
    elif bottom_total > top_total:
        st.success(f"🏆 勝利：{team_bottom}")
    else:
        st.info("🤝 引き分け")
