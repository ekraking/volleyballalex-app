import streamlit as st
import pandas as pd

# --------------------------
# تحميل البيانات من Excel
# --------------------------


@st.cache_data
def load_data():
    teams = pd.read_excel("teams_expanded.xlsx")
    matches = pd.read_excel("matches_expanded.xlsx")
    return teams, matches


teams, matches = load_data()

# --------------------------
# واجهة التطبيق
# --------------------------
st.set_page_config(page_title="Volleyball League", layout="wide")
st.title("🏐 Volleyball Village League")

# جميع المراحل السنية
age_categories = teams["age_category"].unique()

# Tabs رئيسية لكل مرحلة سنية
main_tabs = st.tabs(age_categories)

# --------------------------
# بناء تبويبات فرعية لكل مرحلة
# --------------------------
for i, age in enumerate(age_categories):
    with main_tabs[i]:
        st.subheader(f"📌 المرحلة: {age}")

        # Tabs داخلية
        tab1, tab2, tab3 = st.tabs(["📅 المباريات", "📊 النتائج", "🏆 الترتيب"])

        # --------------------------
        # المباريات
        # --------------------------
        with tab1:
            st.markdown("### 📅 المباريات القادمة")
            upcoming = matches[(matches["age_category"] == age)
                               & (matches["home_score"].isna())]
            st.dataframe(upcoming)

        # --------------------------
        # النتائج
        # --------------------------
        with tab2:
            st.markdown("### 📊 إدخال النتائج")
            for idx, row in matches.iterrows():
                if row["age_category"] == age:
                    home_score = st.number_input(
                        f"{row['home_team']} 🏐", min_value=0, step=1, key=f"h{age}{idx}")
                    away_score = st.number_input(
                        f"{row['away_team']} 🏐", min_value=0, step=1, key=f"a{age}{idx}")
                    if st.button(f"تحديث نتيجة مباراة {row['match_id']} ({age})", key=f"btn{age}{idx}"):
                        matches.at[idx, "home_score"] = home_score
                        matches.at[idx, "away_score"] = away_score
                        # تحديث ملف Excel
                        matches.to_excel("matches_expanded.xlsx", index=False)
                        st.success("✅ تم تحديث النتيجة وحفظها")

        # --------------------------
        # الترتيب
        # --------------------------
        with tab3:
            st.markdown("### 🏆 جدول الترتيب")
            results = matches.dropna(subset=["home_score", "away_score"])
            standings = teams[teams["age_category"] == age].copy()
            standings["points"] = 0

            for _, row in results.iterrows():
                if row["age_category"] == age:
                    if row["home_score"] > row["away_score"]:
                        standings.loc[standings["team_name"]
                                      == row["home_team"], "points"] += 3
                    elif row["home_score"] < row["away_score"]:
                        standings.loc[standings["team_name"]
                                      == row["away_team"], "points"] += 3
                    else:
                        standings.loc[standings["team_name"].isin(
                            [row["home_team"], row["away_team"]]), "points"] += 1

            standings = standings.sort_values(by="points", ascending=False)
            st.dataframe(standings)
