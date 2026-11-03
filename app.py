import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="IPL 2023 Team Analysis", page_icon="🏏", layout="wide")
DATA = Path(__file__).parent
teams = pd.read_csv(DATA / "team_standings.csv")
batters = pd.read_csv(DATA / "top_batters.csv")
bowlers = pd.read_csv(DATA / "top_bowlers.csv")

st.title("🏏 IPL 2023 — Team & Player Analysis")
st.caption("Python • Pandas • Plotly • Streamlit")
st.info("Reconstructed educational dashboard. See README.md for data scope and limitations.")

tab1, tab2, tab3, tab4 = st.tabs(["🏆 Team Standings", "🏏 Batting", "🎯 Bowling", "📊 Insights & Data"])

with tab1:
    a,b,c = st.columns(3)
    a.metric("Teams", len(teams))
    b.metric("Highest points", int(teams.Points.max()))
    c.metric("Top team", teams.loc[teams.Points.idxmax(), "Team"])
    st.dataframe(teams.sort_values(["Points","Net_Run_Rate"], ascending=False), use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(teams.sort_values("Points"), x="Points", y="Team", orientation="h", title="Points by team"), use_container_width=True)
    wins = teams.melt(id_vars="Team", value_vars=["Won","Lost"], var_name="Result", value_name="Matches")
    st.plotly_chart(px.bar(wins, x="Team", y="Matches", color="Result", barmode="group", title="Wins and losses"), use_container_width=True)

with tab2:
    st.dataframe(batters.sort_values("Runs", ascending=False), use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(batters.sort_values("Runs"), x="Runs", y="Player", color="Team", orientation="h", title="Runs by selected leading batters"), use_container_width=True)
    st.plotly_chart(px.scatter(batters, x="Runs", y="Strike_Rate", size="Matches", color="Team", hover_name="Player", title="Runs vs strike rate"), use_container_width=True)

with tab3:
    st.dataframe(bowlers.sort_values("Wickets", ascending=False), use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(bowlers.sort_values("Wickets"), x="Wickets", y="Player", color="Team", orientation="h", title="Wickets by selected leading bowlers"), use_container_width=True)
    st.plotly_chart(px.scatter(bowlers, x="Wickets", y="Economy", size="Matches", color="Team", hover_name="Player", title="Wickets vs economy"), use_container_width=True)

with tab4:
    top_team = teams.loc[teams.Points.idxmax()]
    top_bat = batters.loc[batters.Runs.idxmax()]
    top_bowl = bowlers.loc[bowlers.Wickets.idxmax()]
    st.markdown(f"- **League leader:** {top_team.Team} ({int(top_team.Points)} points).")
    st.markdown(f"- **Leading batter in this dataset:** {top_bat.Player} ({int(top_bat.Runs)} runs).")
    st.markdown(f"- **Leading bowler in this dataset:** {top_bowl.Player} ({int(top_bowl.Wickets)} wickets).")
    st.warning("Player tables are selected leaderboard records, not complete season datasets. No toss-wise, venue-wise, or ball-by-ball analysis is claimed.")
    for label, df, filename in [("Team standings",teams,"team_standings.csv"),("Batting",batters,"top_batters.csv"),("Bowling",bowlers,"top_bowlers.csv")]:
        st.download_button(f"Download {label} CSV", df.to_csv(index=False).encode(), filename, "text/csv")

st.divider()
st.caption("Educational portfolio project. Verify data against a consistent source before formal publication.")
