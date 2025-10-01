import streamlit as st
import pandas as pd

# -------------------------- # واجهة التطبيق # -------------------------- #
st.set_page_config(
    page_title="Volleyball League",
    page_icon="🏐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# اللوجو والهيدر
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=100)  # صورة اللوجو
with col2:
    st.markdown(
        """
        <h1 style='text-align: center; color: #0026ff;'>
        🏐 نتائج مباريات منطقة الإسكندرية للكرة الطائرة 🏐
        </h1>
        """,
        unsafe_allow_html=True
    )

# صورة بانر أو هيدر أسفل العنوان
# st.image("header.jpg", use_column_width=True)


# -------------------------- # تحميل البيانات # -------------------------- #

@st.cache_data
def load_data():
    try:
        teams = pd.read_excel("teams_final.xlsx")
        matches = pd.read_excel("matches_final.xlsx")
    except Exception as e:
        st.error(f"Error loading Excel files: {e}")
        teams, matches = pd.DataFrame(), pd.DataFrame(
            "date", "TeamA", "TeamB", "ScoreA", "ScoreB")
    return teams, matches


teams, matches = load_data()

# تحديد المراحل السنية
if not teams.empty and "AgeCategory" in teams.columns:
    age_categories = teams["AgeCategory"].unique().tolist()
else:
    age_categories = [
        "براعم بنات تحت 9 سنوات", "براعم بنين تحت 9 سنوات",
        "براعم بنات تحت 10 سنوات", "براعم بنين تحت 10 سنوات",
        "براعم بنات تحت 11 سنة", "براعم بنين تحت 11 سنة",
        "براعم بنات تحت 12 سنة", "براعم بنين تحت 12 سنة",
        "الأشبال بنات تحت 13 سنة", "الأشبال بنين تحت 13 سنة"
    ]


# # الأعمدة اللي مش عايز تعرضها
# cols_to_hide = ["match_id", "round", "AgeCategory"]

# # عند العرض فقط
# if not matches.empty:
#     st.dataframe(matches.drop(
#         columns=[c for c in cols_to_hide if c in matches.columns]))


# -------------------------- # دالة حساب النقاط # -------------------------- #


def calculate_points(row):
    score_a = str(row["ScoreA"])
    score_b = str(row["ScoreB"])
    try:
        sa, sb = map(int, [score_a, score_b])
    except:
        return 0, 0

    if (sa == 3 and sb in [0, 1]):
        return 3, 0
    elif (sb == 3 and sa in [0, 1]):
        return 0, 3
    elif (sa == 3 and sb == 2):
        return 2, 1
    elif (sb == 3 and sa == 2):
        return 1, 2
    else:
        return 0, 0


# -------------------------- # التابات الرئيسية # -------------------------- #
main_tabs = st.tabs(age_categories)

for i, category in enumerate(age_categories):
    with main_tabs[i]:
        st.subheader(f"مرحلة {category}")

        sub_tabs = st.tabs(["📅 المباريات", "📊 النتائج", "🏆 الترتيب"])

        with sub_tabs[0]:
            st.write(f"هنا جدول المباريات لمرحلة {category}")
            if not matches.empty and "AgeCategory" in matches.columns:
                st.dataframe(matches[matches["AgeCategory"] == category])

        with sub_tabs[1]:
            st.write(f"هنا النتائج لمرحلة {category}")
            if not matches.empty and "AgeCategory" in matches.columns:
                st.dataframe(matches[matches["AgeCategory"] == category][[
                    "TeamA", "TeamB", "ScoreA", "ScoreB"
                ]])

        with sub_tabs[2]:
            st.write(f"🏆 الترتيب لمرحلة {category}")
            if not matches.empty and "AgeCategory" in matches.columns:
                cat_matches = matches[matches["AgeCategory"]
                                      == category].copy()

                standings = {}
                for _, row in cat_matches.iterrows():
                    team_a, team_b = row["TeamA"], row["TeamB"]
                    pa, pb = calculate_points(row)

                    standings[team_a] = standings.get(team_a, 0) + pa
                    standings[team_b] = standings.get(team_b, 0) + pb

                standings_df = pd.DataFrame(
                    standings.items(), columns=["Team", "Points"]
                ).sort_values(by="Points", ascending=False)

                st.dataframe(standings_df)
