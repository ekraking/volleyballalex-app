import streamlit as st
import pandas as pd

# تحميل البيانات من Excel


@st.cache_data
def load_data():
    try:
        teams = pd.read_excel("teams_final.xlsx")
        matches = pd.read_excel("matches_final.xlsx")
    except Exception as e:
        st.error(f"Error loading Excel files: {e}")
        teams, matches = pd.DataFrame(), pd.DataFrame()
    return teams, matches


teams, matches = load_data()

# تحديد المراحل السنية
if not teams.empty and "AgeCategory" in teams.columns:
    age_categories = teams["AgeCategory"].unique().tolist()
else:
    # قائمة افتراضية لو الملف مش موجود أو العمود ناقص
    age_categories = [
        "براعم بنات تحت 9 سنوات", "براعم بنين تحت 9 سنوات",
        "براعم بنات تحت 10 سنوات", "براعم بنين تحت 10 سنوات",
        "براعم بنات تحت 11 سنة", "براعم بنين تحت 11 سنة",
        "براعم بنات تحت 12 سنة", "براعم بنين تحت 12 سنة",
        "الأشبال بنات تحت 13 سنة", "الأشبال بنين تحت 13 سنة"
    ]

# دالة لحساب النقاط من النتيجة


def calculate_points(row):
    score_a = str(row["ScoreA"])
    score_b = str(row["ScoreB"])
    try:
        sa, sb = map(int, [score_a, score_b])
    except:
        return 0, 0  # لو النتيجة مش مدخلة صح

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


# اختيار المرحلة من selectbox
category = st.selectbox("اختر المرحلة السنية:", age_categories)
st.subheader(f"مرحلة {category}")

# التابات الفرعية داخل كل مرحلة
sub_tabs = st.tabs(["📅 المباريات", "📊 النتائج", "🏆 الترتيب"])

with sub_tabs[0]:
    st.write(f"📅 جدول المباريات لمرحلة {category}")
    if not matches.empty and "AgeCategory" in matches.columns:
        st.dataframe(matches[matches["AgeCategory"] == category])

with sub_tabs[1]:
    st.write(f"📊 النتائج لمرحلة {category}")
    if not matches.empty and "AgeCategory" in matches.columns:
        st.dataframe(matches[matches["AgeCategory"] == category][[
            "TeamA", "TeamB", "ScoreA", "ScoreB"
        ]])

with sub_tabs[2]:
    st.write(f"🏆 الترتيب لمرحلة {category}")
    if not matches.empty and "AgeCategory" in matches.columns:
        cat_matches = matches[matches["AgeCategory"] == category].copy()
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
