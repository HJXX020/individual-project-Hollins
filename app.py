# -*- coding: utf-8 -*-
"""好邻舍 Hollins · 单文件精简版（可直接粘贴到 Streamlit 新建的 app.py）"""
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="好邻舍 Hollins · 家门口的交易场", page_icon="邻", layout="wide")

CSS = """
<style>
.block-container{max-width:1100px;padding-top:6rem}
.hero{background:linear-gradient(120deg,#E8F3EC,#F4F8F2);border:1px solid #D8E7DC;
      border-radius:16px;padding:24px 28px;margin-bottom:16px}
.hero-title{font-size:28px;font-weight:700;color:#1F4D38;margin:0 0 6px}
.hero-sub{font-size:16px;color:#456153;margin:0}
.tag{display:inline-block;background:#fff;border:1px solid #C9DFD0;color:#2F7D5B;
     border-radius:99px;padding:3px 12px;font-size:13px;margin:10px 8px 0 0}
.card{background:#fff;border:1px solid #E2E9E3;border-radius:12px;padding:14px 18px;margin-bottom:10px}
.card-title{font-size:17px;font-weight:650;color:#20372B;margin:0 0 4px}
.meta{font-size:13px;color:#6B7A70;margin:0}
.badge{display:inline-block;font-size:12px;border-radius:6px;padding:2px 8px;margin-left:6px;
       background:#E7F5EC;color:#2F7D5B}
.badge-o{background:#FFF0DE;color:#B96A18}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

DIST = {"春和景明花园": 0, "锦绣家园": 1.2, "望江里社区": 2.1, "梧桐里小区": 2.8, "城东新村": 4.6}


def now():
    return datetime.now().isoformat(timespec="seconds")


def ago(days):
    return (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")


def when(s):
    m = max(0, int((datetime.now() - datetime.fromisoformat(s)).total_seconds() // 60))
    return "刚刚" if m < 1 else f"{m}分钟前" if m < 60 else f"{m//60}小时前" if m < 1440 else f"{m//1440}天前"


def seed():
    return {
        "consent": False, "community": "春和景明花园", "relations": 12,
        "users": [
            dict(id="u1", name="林阿姨", community="春和景明花园", credit=96, phone="138****2210", joined=ago(120), active=now()),
            dict(id="u2", name="陈舟", community="春和景明花园", credit=88, phone="139****6631", joined=ago(86), active=ago(1)),
            dict(id="u3", name="苏禾", community="锦绣家园", credit=92, phone="137****1088", joined=ago(64), active=ago(2)),
            dict(id="u4", name="王叔", community="春和景明花园", credit=79, phone="135****7742", joined=ago(210), active=ago(9)),
        ],
        "items": [
            dict(id="i1", owner="u1", title="手电钻一套", desc="家用闲置，成色好", deposit=50, status="可借", borrower=None, created=ago(0.3)),
            dict(id="i2", owner="u2", title="儿童绘本 20 册", desc="3-6 岁适读，可分批借", deposit=0, status="可借", borrower=None, created=ago(1)),
            dict(id="i3", owner="u3", title="露营天幕", desc="已清洗晾干，周末可约", deposit=200, status="借出中", borrower="u1", created=ago(5)),
        ],
        "helps": [
            dict(id="h1", publisher="u1", title="今天下午帮忙代收快递", kind="代收快递", reward="当面致谢", status="待接单", taker=None, created=ago(0.2)),
            dict(id="h2", publisher="u2", title="周三晚上求代遛小狗", kind="临时遛狗", reward="20 元", status="进行中", taker="u4", created=ago(1)),
            dict(id="h3", publisher="u4", title="出差三天帮忙浇花", kind="浇花照看", reward="技能互换", status="待接单", taker=None, created=ago(0.6)),
        ],
    }


if "data" not in st.session_state:
    st.session_state.data = seed()
d = st.session_state.data
U = {u["id"]: u for u in d["users"]}


def me(uid):
    return U.get(uid, d["users"][0])


def near(community):
    here = d["community"]
    return community == here or (DIST.get(community, 99) <= 3 and abs(DIST.get(community, 99) - DIST.get(here, 0)) <= 3)


def add_credit(uid, n):
    me(uid)["credit"] += n


if not d["consent"]:
    st.markdown('<div class="hero"><div class="hero-title">好邻舍 Hollins</div>'
                '<div class="hero-sub">家门口的交易场 · 1公里互助网</div>'
                '<span class="tag">同小区认证</span><span class="tag">当面借还</span></div>', unsafe_allow_html=True)
    st.subheader("隐私说明")
    st.write("仅收集手机号（注册）与小区（匹配邻居）；认证材料不公开展示；信息仅对同小区及 3 公里内认证用户可见；可随时注销账号。本演示数据只存在当前会话中。")
    with st.form("agree"):
        ok = st.checkbox("我已阅读并同意上述说明")
        if st.form_submit_button("同意并进入社区", type="primary") and ok:
            d["consent"] = True
            st.rerun()
    st.stop()

with st.sidebar:
    st.markdown("### 好邻舍 Hollins")
    community = st.selectbox("我的小区（地理围栏）", list(DIST), index=list(DIST).index(d["community"]))
    d["community"] = community
    uid = st.session_state.get("uid") or d["users"][0]["id"]
    st.session_state["uid"] = uid
    ids = [u["id"] for u in d["users"]]
    uid = st.selectbox("演示身份", ids, index=ids.index(uid),
                       format_func=lambda x: f'{U[x]["name"]} · 信用 {U[x]["credit"]}')
    st.session_state["uid"] = uid
    me(uid)["active"] = now()
    st.caption(f'{me(uid)["name"]} · 信用 {me(uid)["credit"]} · 已实名/住户')
    st.divider()
    nav = st.radio("功能", ["首页", "闲置借用", "邻里互助", "我的邻居卡"])

if nav == "首页":
    st.markdown('<div class="hero"><div class="hero-title">你好，邻居</div>'
                '<div class="hero-sub">不用刷群消息，家门口的闲置、互助和公告都在这里。</div>'
                '<span class="tag">同小区认证</span><span class="tag">当面交易</span></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("周边邻居", len([u for u in d["users"] if near(u["community"])]))
    c2.metric("可借闲置", len([i for i in d["items"] if near(U[i["owner"]]["community"]) and i["status"] == "可借"]))
    c3.metric("待接互助", len([h for h in d["helps"] if near(U[h["publisher"]]["community"]) and h["status"] == "待接单"]))
    c4.metric("有效互助关系", d["relations"])
    st.divider()
    a, b = st.columns(2)
    with a:
        st.subheader("刚刚发生在身边")
        for i in d["items"][:3]:
            st.markdown(f'<div class="card"><div class="card-title">{i["title"]}'
                        f'<span class="badge">{i["status"]}</span></div>'
                        f'<div class="meta">{U[i["owner"]]["name"]} · 押金 ¥{i["deposit"]} · {when(i["created"])}</div></div>',
                        unsafe_allow_html=True)
    with b:
        st.subheader("邻里互助需求")
        for h in d["helps"][:3]:
            st.markdown(f'<div class="card"><div class="card-title">{h["title"]}'
                        f'<span class="badge">{h["status"]}</span></div>'
                        f'<div class="meta">{U[h["publisher"]]["name"]} · {h["kind"]} · {h["reward"]}</div></div>',
                        unsafe_allow_html=True)

elif nav == "闲置借用":
    st.subheader("闲置借用 · 借用 → 归还 → 互评")
    with st.expander("发布闲置"):
        with st.form("new_item"):
            title = st.text_input("物品名称")
            desc = st.text_area("使用说明")
            deposit = st.number_input("押金（元）", min_value=0, value=0, step=10)
            if st.form_submit_button("发布") and title.strip():
                d["items"].insert(0, dict(id=f'i{len(d["items"])+1}', owner=uid, title=title.strip(),
                                          desc=desc, deposit=deposit, status="可借", borrower=None, created=now()))
                st.success("已发布")
                st.rerun()
    for i in d["items"]:
        if not near(U[i["owner"]]["community"]):
            continue
        st.markdown(f'<div class="card"><div class="card-title">{i["title"]}'
                    f'<span class="badge {"badge-o" if i["status"]!="可借" else ""}">{i["status"]}</span></div>'
                    f'<div class="meta">{U[i["owner"]]["name"]} · 押金 ¥{i["deposit"]} · {i["desc"]}</div></div>',
                    unsafe_allow_html=True)
        if i["status"] == "可借" and i["owner"] != uid and st.button("立即借用", key=f'b{i["id"]}'):
            i.update(status="借出中", borrower=uid)
            st.toast(f'押金托管演示 ¥{i["deposit"]}')
            st.rerun()
        if i["status"] == "借出中" and i["borrower"] == uid and st.button("我已归还", key=f'r{i["id"]}'):
            i["status"] = "待确认"
            st.rerun()
        if i["status"] == "待确认" and i["owner"] == uid and st.button("确认归还并互评完成", key=f'c{i["id"]}'):
            i["status"] = "可借"
            add_credit(i["owner"], 2)
            add_credit(i["borrower"], 2)
            d["relations"] += 1
            st.toast("双方信用分 +2")
            st.rerun()
        if i["status"] == "借出中" and i["owner"] == uid and st.button("标记违约（借用者 -10）", key=f'x{i["id"]}'):
            add_credit(i["borrower"], -10)
            i.update(status="可借", borrower=None)
            st.rerun()

elif nav == "邻里互助":
    st.subheader("邻里轻互助 · 发布 → 接单 → 完成 → 互评")
    with st.expander("发起互助"):
        with st.form("new_help"):
            title = st.text_input("一句话需求")
            kind = st.selectbox("类型", ["代收快递", "临时遛狗", "浇花照看", "照看孩子", "跑腿代办"])
            reward = st.text_input("回馈方式")
            if st.form_submit_button("发布") and title.strip():
                d["helps"].insert(0, dict(id=f'h{len(d["helps"])+1}', publisher=uid, title=title.strip(),
                                          kind=kind, reward=reward or "当面致谢", status="待接单",
                                          taker=None, created=now()))
                st.success("已发布")
                st.rerun()
    for h in d["helps"]:
        if not near(U[h["publisher"]]["community"]):
            continue
        st.markdown(f'<div class="card"><div class="card-title">{h["title"]}'
                    f'<span class="badge {"badge-o" if h["status"]!="待接单" else ""}">{h["status"]}</span></div>'
                    f'<div class="meta">{U[h["publisher"]]["name"]} · {h["kind"]} · {h["reward"]} · {when(h["created"])}</div></div>',
                    unsafe_allow_html=True)
        if h["status"] == "待接单" and h["publisher"] != uid and st.button("我来接单", key=f't{h["id"]}'):
            h.update(status="进行中", taker=uid)
            st.rerun()
        if h["status"] == "进行中" and h["publisher"] == uid and st.button("确认完成并互评", key=f'd{h["id"]}'):
            h["status"] = "已完成"
            add_credit(h["publisher"], 3)
            add_credit(h["taker"], 3)
            d["relations"] += 1
            st.toast("双方信用分 +3")
            st.rerun()

else:
    u = me(uid)
    st.markdown(f'<div class="hero"><div class="hero-title">{u["name"]}</div>'
                f'<div class="hero-sub">{u["community"]} · 信用分 {u["credit"]} · 已实名 / 已认证住户</div></div>',
                unsafe_allow_html=True)
    recent = [x for x in d["users"] if (datetime.now() - datetime.fromisoformat(x["active"])).days < 7]
    c1, c2, c3 = st.columns(3)
    c1.metric("信用分", u["credit"])
    c2.metric("有效互助关系数", d["relations"])
    c3.metric("7日留存率", f'{round(len(recent)/len(d["users"])*100)}%')
    st.caption("冷启动重点看有效互助关系数与 7 日留存率。")
    st.divider()
    st.warning("注销将清除当前会话数据并重置授权。")
    if st.checkbox("确认注销") and st.button("申请注销账号"):
        st.session_state.clear()
        st.rerun()
