import streamlit as st
import random

st.set_page_config(
    page_title="⚾ シンプル野球ゲーム",
    layout="wide"   # ← これが重要
)


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
if "ready" not in st.session_state:
    st.session_state.ready = False

# -------------------------
# チーム名入力
# -------------------------
if not st.session_state.ready:
    st.subheader("チーム名を入力してください")

    team_top = st.text_input("先攻チーム名（表）", value="チームA")
    team_bottom = st.text_input("後攻チーム名（裏）", value="チームB")

    if st.button("▶ ゲーム開始"):
        st.session_state.team_top = team_top
        st.session_state.team_bottom = team_bottom
        st.session_state.ready = True
        st.rerun()

    st.stop()  # ← ここで以降の表示を止める
    
team_top = st.session_state.team_top
team_bottom = st.session_state.team_bottom


# -------------------------
# 現在の回表示
# -------------------------
col1, col2 = st.columns([3, 2])

with col1:
    if not st.session_state.finished:
        half = "表" if st.session_state.top else "裏"
        st.subheader(f"{st.session_state.inning}回 {half}")

with col2:
    if not st.session_state.finished:
        if st.button("▶ 次の結果を表示"):

            score = random.choices(
                [0, 1, 2, 3, 4, 5],
                weights=[0.65, 0.14, 0.10, 0.07, 0.03, 0.01],
                k=1
            )[0]

if st.session_state.top:
    # 表の攻撃
    st.session_state.scores_top[st.session_state.inning - 1] = scores
    st.session_state.top = False

    # ★ 9回表終了時の特別判定
    if st.session_state.inning == 9:
        top_total = sum(s for s in st.session_state.scores_top if s is not None)
        bottom_total = sum(s for s in st.session_state.scores_bottom if isinstance(s, int))

        if bottom_total > top_total:
            # 後攻の勝利確定 → 9回裏なし
            st.session_state.scores_bottom[8] = "X"
            st.session_state.finished = True
            st.rerun()

else:
    # 裏の攻撃
    st.session_state.scores_bottom[st.session_state.inning - 1] = scores
    st.session_state.top = True
    st.session_state.inning += 1



# -------------------------
# スコアボード表示
# -------------------------
st.markdown("### スコアボード")

html = "<table style='width:100%; border-collapse:collapse; text-align:center;'>"
html += "<tr><th></th>" + "".join(f"<th>{i}</th>" for i in range(1,10)) + "<th>R</th></tr>"

top_total = sum(s for s in st.session_state.scores_top if s is not None)
bottom_total = sum(s for s in st.session_state.scores_bottom if s is not None)

html += f"<tr><td>{team_top}</td>"
for s in st.session_state.scores_top:
    html += f"<td>{'' if s is None else s}</td>"
html += f"<td><b>{top_total}</b></td></tr>"

html += f"<tr><td>{team_bottom}</td>"
for s in st.session_state.scores_bottom:
    html += f"<td>{'' if s is None else s}</td>"
html += f"<td><b>{bottom_total}</b></td></tr>"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)

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
