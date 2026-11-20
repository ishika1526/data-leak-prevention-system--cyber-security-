"""app.py - Streamlit UI: input panel, result card and dashboard.

Run with:  streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

from detector import SEVERITY
from logger import ALERTS, LOGS
from simulator import CHANNELS, simulate

st.set_page_config(page_title="Data Leak Prevention Simulator", layout="wide")
st.title("Data Leak Prevention Simulator")
st.caption("Use DUMMY data only. Nothing here touches real information.")

SAMPLE = (
    "Hi team, my card is 4111 1111 1111 1111, PAN ABCDE1234F, "
    "call +91 98765 43210 or mail name@example.com"
)

# ---------------- Input panel ----------------
left, right = st.columns(2)
with left:
    st.subheader("1. Input")
    user = st.text_input("User name", value="ishika")
    channel = st.selectbox("Leak channel", CHANNELS)
    text = st.text_area("Paste sample text", value=SAMPLE, height=150)
    upload = st.file_uploader("...or upload a sample .txt file", type=["txt"])
    run = st.button("Simulate", type="primary")

# ---------------- Result card ----------------
with right:
    st.subheader("2. Result")
    if run:
        payload = upload.read().decode("utf-8", errors="ignore") if upload else text
        action, out, hits = simulate(user, channel, payload)

        if action == "BLOCK":
            st.error("BLOCKED - transfer stopped and admin alerted.")
        elif action == "MASK":
            st.warning("MASKED - sensitive values hidden before release.")
        elif action == "WARN":
            st.info("WARNED - low-risk data detected; user notified.")
        else:
            st.success("ALLOWED - nothing sensitive found. Event logged.")

        if hits:
            st.write("**Findings**")
            st.table(pd.DataFrame(
                [{"Type": n, "Severity": SEVERITY.get(n, "-"), "Value": v}
                 for n, v in hits]
            ))
        st.write("**Output released**")
        st.code(out if out else "(payload withheld)")
    else:
        st.write("Choose a channel and click **Simulate**.")

# ---------------- Dashboard ----------------
st.divider()
st.subheader("3. Dashboard")

if LOGS:
    df = pd.DataFrame(LOGS)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total events", len(df))
    c2.metric("Blocked", int((df["action"] == "BLOCK").sum()))
    c3.metric("Masked", int((df["action"] == "MASK").sum()))

    col_a, col_b = st.columns(2)
    types = df.explode("types").dropna(subset=["types"])
    if not types.empty:
        by_type = types["types"].value_counts().reset_index()
        by_type.columns = ["Data type", "Count"]
        col_a.plotly_chart(
            px.bar(by_type, x="Data type", y="Count", title="Leaks by type"),
            use_container_width=True,
        )
    by_channel = df["channel"].value_counts().reset_index()
    by_channel.columns = ["Channel", "Count"]
    col_b.plotly_chart(
        px.pie(by_channel, names="Channel", values="Count", title="Events by channel"),
        use_container_width=True,
    )

    st.write("**Event log**")
    st.dataframe(df, use_container_width=True)
    if ALERTS:
        st.write("**Admin alerts**")
        for a in ALERTS[-5:]:
            st.write(a)
else:
    st.write("No events yet. Run a simulation to populate the dashboard.")
