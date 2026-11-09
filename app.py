"""
SkillPath AI – AI-Powered Corporate Employee Upskilling Platform
Main Streamlit Application with Modern Bright Pastel UI, Interactive Tabs,
Dynamic Step Cards, Lottie Animations, and Explainable AI Engine.
"""
import streamlit as st
import pandas as pd
import numpy as np

from config import PROFICIENCY_LEVELS, SKILL_CATEGORIES, STANDARD_ROLES, DEPARTMENTS
from database import (
    init_db,
    get_all_employees,
    get_employee_by_id,
    get_all_skills,
    get_skills_by_category,
    get_employee_skills,
    get_all_courses
)
from modules.assessment import (
    validate_employee_input,
    save_or_update_employee,
    save_employee_skill_assessment,
    score_diagnostic_quiz,
    DIAGNOSTIC_QUESTIONS
)
from modules.skill_gap import (
    analyze_skill_gap,
    create_radar_chart,
    create_gap_bar_chart
)
from modules.recommender import recommend_courses
from modules.roadmap import (
    generate_learning_roadmap,
    create_roadmap_timeline_chart
)
from modules.tracker import (
    enroll_employee_in_course,
    update_course_progress,
    log_learning_activity,
    get_employee_tracker_summary
)
from modules.analytics import (
    get_workforce_overview,
    create_department_readiness_chart,
    create_org_gaps_chart,
    create_talent_mobility_donut,
    create_skill_distribution_heatmap
)
from modules.ui_theme import (
    apply_custom_theme,
    render_top_hero_banner,
    render_section_header,
    render_roadmap_step_card,
    render_course_card,
    render_skill_progress_item,
    load_lottie_file,
    render_lottie
)

# Page configuration
st.set_page_config(
    page_title="SkillPath AI | Corporate Upskilling Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Apply Bright Pastel Theme & Custom CSS
apply_custom_theme()


def polish_fig(fig):
    """Polishes Plotly charts to match the pastel light theme."""
    if fig:
        fig.update_layout(
            paper_bgcolor="rgba(255, 255, 255, 0)",
            plot_bgcolor="rgba(255, 255, 255, 0)",
            font=dict(family="Plus Jakarta Sans, sans-serif", color="#1E293B"),
            margin=dict(l=25, r=25, t=45, b=35)
        )
    return fig


# --- Sidebar: Active Employee Context & Navigation ---
st.sidebar.image("https://img.icons8.com/isometric/100/compass--v1.png", width=70)
st.sidebar.title("🎯 SkillPath AI")
st.sidebar.caption("✨ Enterprise Talent Intelligence & Upskilling")

# Navigation with bright emojis
page = st.sidebar.radio(
    "🧭 Navigation Menu",
    [
        "🏠 Executive Dashboard",
        "📝 Skill Assessment",
        "🎯 Skill Gap Analyzer",
        "💡 Course Recommendations",
        "🗺️ Personalized Roadmap",
        "📈 Learning Tracker",
        "📊 HR Workforce Analytics"
    ]
)

st.sidebar.markdown("---")

# Employee Context Selector
employees_df = get_all_employees()
if not employees_df.empty:
    emp_options = {
        f"{row['name']} ({row['current_role']} ➔ {row['target_role']})": row["id"]
        for _, row in employees_df.iterrows()
    }
    selected_label = st.sidebar.selectbox("👤 Active Employee View", list(emp_options.keys()))
    current_emp_id = emp_options[selected_label]
    active_emp = get_employee_by_id(current_emp_id)

    # Sidebar Employee Profile Card
    with st.sidebar.expander("👤 Active Employee Details", expanded=True):
        st.write(f"🏢 **Department:** {active_emp['department']}")
        st.write(f"🎯 **Target Role:** {active_emp['target_role']}")
        st.write(f"💼 **Experience:** {active_emp['experience_years']} yrs")
        st.write(f"⏱️ **Weekly Pace:** {active_emp['weekly_learning_hours']} hrs/week")
else:
    active_emp = None
    current_emp_id = None

st.sidebar.markdown("---")
# Admin tools
with st.sidebar.expander("⚙️ System & Demo Controls"):
    if st.button("🔄 Reset Demo Seed Data", use_container_width=True):
        init_db(force_reseed=True)
        st.success("✅ Database re-seeded with realistic enterprise data!")
        st.rerun()

# Top Hero Banner (Always visible for maximum brand engagement)
render_top_hero_banner()


# -------------------------------------------------------------
# PAGE 1: EXECUTIVE DASHBOARD
# -------------------------------------------------------------
if page == "🏠 Executive Dashboard":
    render_section_header(
        title="🏠 Executive Talent & Capability Dashboard",
        subtitle=f"Tracking employee benchmark readiness, immediate interventions, and personalized career growth for <b>{active_emp['name'] if active_emp else 'Active Employee'}</b>.",
        badge="📊 EXECUTIVE TALENT PULSE",
        lottie_filename="growth.json",
        image_url="https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=600&q=80",
        anim_height=160,
        key_prefix="dash_header"
    )

    if active_emp:
        gap_res = analyze_skill_gap(current_emp_id)
        tracker_res = get_employee_tracker_summary(current_emp_id)

        # High level metric cards for active employee
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="🎯 Target Role Readiness",
                value=f"{gap_res['readiness_score']}%",
                delta=f"{len(gap_res['strengths'])} skills benchmark met"
            )
        with col2:
            st.metric(
                label="🚨 Critical Skill Deficits",
                value=len(gap_res["critical_gaps"]),
                delta=f"-{len(gap_res['critical_gaps'])} required" if gap_res["critical_gaps"] else "All core met",
                delta_color="inverse"
            )
        with col3:
            st.metric(
                label="📚 Active Enrollments",
                value=tracker_res["active_courses"],
                delta=f"{tracker_res['completed_courses']} completed"
            )
        with col4:
            st.metric(
                label="⏱️ Logged Learning Time",
                value=f"{tracker_res['total_hours']} hrs",
                delta=f"Pace: {active_emp['weekly_learning_hours']} hrs/wk"
            )

        # Readiness progress meter
        st.markdown(f"**🎯 Overall Target Role Benchmark Readiness:** `{gap_res['readiness_score']}%`")
        st.progress(max(0.0, min(1.0, gap_res['readiness_score'] / 100.0)))
        st.markdown("<br>", unsafe_allow_html=True)

        # Section Tabs
        dash_tab1, dash_tab2, dash_tab3 = st.tabs([
            "🌐 Competency Radar & Action Plan",
            "🏆 Unlocked Achievements & Badges",
            "📋 Active Employee Summary Profile"
        ])

        with dash_tab1:
            col_left, col_right = st.columns([1.25, 1])

            with col_left:
                st.subheader(f"🌐 Competency Radar: {active_emp['name']}")
                st.caption(f"Comparing current proficiency against benchmark for **{active_emp['target_role']}**")
                radar_fig = polish_fig(create_radar_chart(gap_res["gap_df"], active_emp["target_role"], active_emp["name"]))
                st.plotly_chart(radar_fig, use_container_width=True)

            with col_right:
                st.subheader("⚡ Priority Capability Intervention")
                if gap_res["critical_gaps"]:
                    st.warning(f"🚨 **{len(gap_res['critical_gaps'])} Critical Skill Gaps** require immediate intervention:")
                    for cg in gap_res["critical_gaps"][:3]:
                        st.markdown(
                            f"- **🎯 {cg['skill_name']}**: Current Level {cg['current_level']} ➔ Required Level {cg['required_level']} (*Gap: +{cg['gap']}*)"
                        )
                else:
                    st.success("✅ **No critical gaps detected!** You are well-aligned with your target role benchmark.")

                st.markdown("#### 💡 Recommended Next Course")
                recs = recommend_courses(current_emp_id, top_n=1)
                if recs:
                    top_rec = recs[0]
                    st.markdown(f"**[{top_rec['title']}]({top_rec['platform_url']})**")
                    st.caption(f"🏛️ Provider: {top_rec['provider']} | 🎯 Skill: {top_rec['skill_name']} (Lvl {top_rec['level']})")
                    st.info(f"💡 {top_rec['explanation']}")
                    if st.button("➕ Quick Enroll in Next Course", key="dash_quick_enroll"):
                        ok, err = enroll_employee_in_course(current_emp_id, top_rec["course_id"])
                        if ok:
                            st.success(f"Enrolled in {top_rec['title']}!")
                            st.rerun()
                        else:
                            st.warning(err)

        with dash_tab2:
            st.subheader("🏆 Unlocked Badges & Upskilling Achievements")
            if tracker_res["badges"]:
                b_cols = st.columns(min(4, len(tracker_res["badges"])))
                for i, badge in enumerate(tracker_res["badges"]):
                    with b_cols[i % len(b_cols)]:
                        st.markdown(f"""
                        <div class="badge-pill-card">
                            <div style="font-size: 2.2rem; margin-bottom: 6px;">{badge['icon']}</div>
                            <h4 style="margin: 0; color: #1E293B;">{badge['title']}</h4>
                            <p style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">{badge['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("🎓 Enroll in courses and log study sessions to unlock enterprise capability achievements!")

        with dash_tab3:
            st.subheader(f"📋 Employee Profile Overview: {active_emp['name']}")
            sc1, sc2 = st.columns(2)
            with sc1:
                st.write(f"👤 **Full Name:** {active_emp['name']}")
                st.write(f"✉️ **Corporate Email:** {active_emp['email']}")
                st.write(f"🏢 **Department:** {active_emp['department']}")
                st.write(f"💼 **Current Designation:** {active_emp['current_role']}")
            with sc2:
                st.write(f"🎯 **Target Aspirational Role:** {active_emp['target_role']}")
                st.write(f"📅 **Industry Experience:** {active_emp['experience_years']} years")
                st.write(f"⏱️ **Weekly Study Commitment:** {active_emp['weekly_learning_hours']} hrs/week")
                st.write(f"📈 **Active In Progress Courses:** {tracker_res['active_courses']}")


# -------------------------------------------------------------
# PAGE 2: EMPLOYEE SKILL ASSESSMENT
# -------------------------------------------------------------
elif page == "📝 Skill Assessment":
    render_section_header(
        title="📝 Employee Skill Assessment & Diagnostics",
        subtitle="Benchmark employee competencies via self-rating or take the objective diagnostic mini-quiz to eliminate self-assessment bias.",
        badge="📝 CAPABILITY BENCHMARKING",
        lottie_filename="skills.json",
        image_url="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=600&q=80",
        anim_height=160,
        key_prefix="assess_header"
    )

    tab_profile, tab_self_assess, tab_quiz = st.tabs([
        "👤 Employee Profile & Registration",
        "🎚️ Competency Self-Assessment Rating",
        "🧠 Objective Diagnostic Mini-Quiz"
    ])

    with tab_profile:
        st.subheader("👤 Employee Details Management")
        with st.form("employee_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                form_name = st.text_input("Full Name", value=active_emp["name"] if active_emp else "")
                form_email = st.text_input("Corporate Email", value=active_emp["email"] if active_emp else "")
                form_dept = st.selectbox(
                    "Department",
                    DEPARTMENTS,
                    index=DEPARTMENTS.index(active_emp["department"]) if active_emp and active_emp["department"] in DEPARTMENTS else 0
                )
            with col2:
                form_curr_role = st.text_input("Current Role Designation", value=active_emp["current_role"] if active_emp else "")
                form_target_role = st.selectbox(
                    "Target Aspirational Role",
                    STANDARD_ROLES,
                    index=STANDARD_ROLES.index(active_emp["target_role"]) if active_emp and active_emp["target_role"] in STANDARD_ROLES else 0
                )
                sub_col1, sub_col2 = st.columns(2)
                with sub_col1:
                    form_exp = st.number_input(
                        "Years of Experience",
                        min_value=0.0,
                        max_value=50.0,
                        value=float(active_emp["experience_years"]) if active_emp else 2.0,
                        step=0.5
                    )
                with sub_col2:
                    form_hours = st.number_input(
                        "Weekly Learning Hours",
                        min_value=1.0,
                        max_value=40.0,
                        value=float(active_emp["weekly_learning_hours"]) if active_emp else 5.0,
                        step=1.0
                    )

            submitted = st.form_submit_button("💾 Save Employee Profile")
            if submitted:
                emp_id, err = save_or_update_employee(
                    name=form_name,
                    email=form_email,
                    department=form_dept,
                    current_role=form_curr_role,
                    target_role=form_target_role,
                    experience_years=form_exp,
                    weekly_learning_hours=form_hours,
                    employee_id=current_emp_id
                )
                if err:
                    st.error(f"❌ Validation Error: {err}")
                else:
                    st.success("✅ Employee profile successfully updated!")
                    st.rerun()

    with tab_self_assess:
        st.subheader(f"🎚️ Rate Competencies for: {active_emp['name']}")
        st.info("💡 **Proficiency Scale:** **1: Novice** (Theory only) | **2: Elementary** (Assisted tasks) | **3: Intermediate** (Independent practitioner) | **4: Advanced** (Leads & designs) | **5: Expert** (Architect & innovator)")

        emp_skills_df = get_employee_skills(current_emp_id)
        current_ratings = dict(zip(emp_skills_df["skill_id"], emp_skills_df["proficiency_level"]))

        skills_by_cat = get_skills_by_category()
        updated_ratings = {}

        with st.form("self_assessment_form"):
            for category, skills_list in skills_by_cat.items():
                st.markdown(f"#### 📂 {category}")
                cols = st.columns(2)
                for i, skill in enumerate(skills_list):
                    sid = skill["id"]
                    curr_val = current_ratings.get(sid, 1)
                    curr_val = max(1, min(5, curr_val))
                    with cols[i % 2]:
                        updated_ratings[sid] = st.slider(
                            f"🎯 {skill['name']}",
                            min_value=1,
                            max_value=5,
                            value=curr_val,
                            key=f"skill_slider_{sid}",
                            help=skill["description"]
                        )
                        # Visual progress bar for skill level
                        level_pct = updated_ratings[sid] / 5.0
                        st.progress(level_pct)
                        st.caption(f"Current Rating: **Level {updated_ratings[sid]}/5** ({PROFICIENCY_LEVELS[updated_ratings[sid]]['name']})")
                st.markdown("---")

            if st.form_submit_button("✅ Update Self-Assessment Ratings"):
                success, err = save_employee_skill_assessment(current_emp_id, updated_ratings)
                if success:
                    st.success("✅ Skill assessment ratings successfully saved!")
                    st.rerun()
                else:
                    st.error(f"❌ Error saving ratings: {err}")

    with tab_quiz:
        st.subheader("🧠 Objective Skill Diagnostic Mini-Quiz")
        st.caption("Standardized questions to objectively benchmark employee foundational competencies and eliminate self-reporting bias.")

        with st.form("diagnostic_quiz_form"):
            user_answers = {}
            for q in DIAGNOSTIC_QUESTIONS:
                st.markdown(f"**Q{q['id']}. [{q['category']} / {q['skill']}]** {q['question']}")
                selected_idx = st.radio(
                    "Select best answer:",
                    options=range(len(q["options"])),
                    format_func=lambda i, opts=q["options"]: opts[i],
                    key=f"quiz_q_{q['id']}"
                )
                user_answers[q["id"]] = selected_idx
                st.markdown("---")

            if st.form_submit_button("📊 Submit Diagnostic Answers"):
                quiz_result = score_diagnostic_quiz(user_answers)
                st.subheader(f"🎯 Diagnostic Score: {quiz_result['score_pct']}% ({quiz_result['correct_answers']}/{quiz_result['total_questions']} correct)")
                st.progress(quiz_result['score_pct'] / 100.0)
                st.info(f"🎯 **Suggested Baseline Proficiency Level:** Level {quiz_result['suggested_baseline']} ({PROFICIENCY_LEVELS[quiz_result['suggested_baseline']]['name']})")

                with st.expander("🔍 Review Answer Breakdown", expanded=True):
                    for b in quiz_result["breakdown"]:
                        if b["is_correct"]:
                            st.success(f"✅ **{b['skill']}**: Correct ({b['correct_option']})")
                        else:
                            st.error(f"❌ **{b['skill']}**: Your answer: '{b['selected_option']}' | Correct: '{b['correct_option']}'")


# -------------------------------------------------------------
# PAGE 3: SKILL GAP ANALYZER
# -------------------------------------------------------------
elif page == "🎯 Skill Gap Analyzer":
    render_section_header(
        title="🎯 Target Role Skill Gap Analyzer",
        subtitle=f"Evaluating <b>{active_emp['name']}</b>'s skill profile against <b>{active_emp['target_role']}</b> benchmarks with what-if scenario simulation.",
        badge="🎯 GAP ANALYSIS & SIMULATION",
        lottie_filename="ai.json",
        image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80",
        anim_height=160,
        key_prefix="gap_header"
    )

    # What-if role benchmark switching
    col_t1, _ = st.columns([2.5, 1])
    with col_t1:
        target_role_eval = st.selectbox(
            "🔮 Simulate Target Role Benchmark (What-if scenario):",
            STANDARD_ROLES,
            index=STANDARD_ROLES.index(active_emp["target_role"]) if active_emp["target_role"] in STANDARD_ROLES else 0
        )

    gap_data = analyze_skill_gap(current_emp_id, target_role=target_role_eval)
    gap_df = gap_data["gap_df"]

    # Top KPI row with rounded st.metric cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("🎯 Benchmark Readiness Score", f"{gap_data['readiness_score']}%")
    with kpi2:
        st.metric("📚 Total Skills Evaluated", gap_data["total_skills_required"])
    with kpi3:
        st.metric("🚨 Critical Gaps", len(gap_data["critical_gaps"]))
    with kpi4:
        st.metric("✅ Competencies Met", len(gap_data["strengths"]))

    # Visual readiness progress bar
    st.markdown(f"**🎯 Benchmark Readiness Meter:** `{gap_data['readiness_score']}%`")
    st.progress(max(0.0, min(1.0, gap_data['readiness_score'] / 100.0)))
    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for Gap Analyzer
    gap_tab1, gap_tab2, gap_tab3 = st.tabs([
        "🌐 Competency Radar & Benchmarks",
        "📉 Gap Severity Breakdown",
        "📋 Full Competency Matrix & Progress Levels"
    ])

    with gap_tab1:
        st.subheader("🌐 Competency Radar vs Role Benchmark")
        radar_fig = polish_fig(create_radar_chart(gap_df, target_role_eval, active_emp["name"]))
        st.plotly_chart(radar_fig, use_container_width=True)

    with gap_tab2:
        st.subheader("📉 Gap Severity by Competency")
        bar_fig = polish_fig(create_gap_bar_chart(gap_df))
        st.plotly_chart(bar_fig, use_container_width=True)

    with gap_tab3:
        st.subheader("📋 Individual Skill Progress Levels")
        st.caption("Visual breakdown of current proficiency versus required role benchmarks for all competencies.")

        if not gap_df.empty:
            for _, row in gap_df.iterrows():
                render_skill_progress_item(
                    skill_name=row["skill_name"],
                    category=row["category"],
                    current_lvl=int(row["current_level"]),
                    required_lvl=int(row["required_level"]),
                    gap=int(row["gap"]),
                    status=row["status"],
                    is_core=int(row["is_core"])
                )

            st.markdown("---")
            st.subheader("📑 Tabular Gap Breakdown")
            display_df = gap_df[["skill_name", "category", "current_level", "required_level", "gap", "is_core", "status"]].copy()
            display_df["is_core"] = display_df["is_core"].apply(lambda x: "⭐ Core" if x == 1 else "Elective")
            display_df.columns = ["Skill Name", "Category", "Current Level", "Required Benchmark", "Gap", "Role Importance", "Status"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# PAGE 4: COURSE RECOMMENDATION ENGINE
# -------------------------------------------------------------
elif page == "💡 Course Recommendations":
    render_section_header(
        title="💡 AI-Powered Course Recommendations",
        subtitle="Personalized course suggestions targeting identified skill gaps with transparent, explainable multi-criteria scoring.",
        badge="💡 EXPLAINABLE AI SCORING",
        lottie_filename="learning.json",
        image_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=600&q=80",
        anim_height=160,
        key_prefix="recs_header"
    )

    # Controls row
    rc1, rc2, rc3 = st.columns([1.5, 1.5, 1])
    with rc1:
        use_ai = st.toggle("🤖 Use AI Multi-Criteria Scoring (vs Deterministic Fallback)", value=True)
    with rc2:
        skills_df = get_all_skills()
        skill_filter = st.selectbox(
            "🎯 Filter by Specific Gap Skill",
            options=["All Gap Skills"] + list(skills_df["name"].unique())
        )
        selected_skill_id = None
        if skill_filter != "All Gap Skills":
            match = skills_df[skills_df["name"] == skill_filter]
            if not match.empty:
                selected_skill_id = int(match.iloc[0]["id"])
    with rc3:
        num_recs = st.slider("🔢 Top Recommendations Count", min_value=3, max_value=10, value=6)

    recs = recommend_courses(
        current_emp_id,
        use_ai_heuristic=use_ai,
        top_n=num_recs,
        filter_skill_id=selected_skill_id
    )

    rec_tab1, rec_tab2, rec_tab3 = st.tabs([
        "✨ Curated AI Recommendations",
        "⚙️ Scoring Rationale & Heuristic Weights",
        "📚 Full Course Catalog & Provider Coverage"
    ])

    with rec_tab1:
        if not recs:
            st.info("ℹ️ No courses found matching current criteria.")
        else:
            st.caption(f"Showing **{len(recs)}** recommended courses sorted by relevance score.")
            for rec in recs:
                render_course_card(rec)
                col_btn1, col_btn2, _ = st.columns([1.5, 2, 5])
                with col_btn1:
                    st.link_button("🔗 View Official Course", rec["platform_url"])
                with col_btn2:
                    if st.button("➕ Enroll Now", key=f"rec_enroll_{rec['course_id']}"):
                        ok, err = enroll_employee_in_course(current_emp_id, rec["course_id"])
                        if ok:
                            st.success(f"✅ Successfully enrolled in {rec['title']}!")
                            st.rerun()
                        else:
                            st.warning(err)
                st.markdown("<br>", unsafe_allow_html=True)

    with rec_tab2:
        st.subheader("⚙️ Transparent Multi-Criteria AI Heuristic Weights")
        st.markdown("""
        <div class="white-card">
            <h4>🧠 Scoring Mathematical Breakdown:</h4>
            <p>Every course recommendation score (0 - 100) is deterministically calculated using 4 weighted parameters:</p>
            <ul>
                <li><b>🎯 Skill Gap Magnitude (45% weight):</b> Direct alignment with the employee's critical deficits for their target role benchmark.</li>
                <li><b>📈 Difficulty Alignment (25% weight):</b> Ensures course level (1-5) matches the employee's current capability for optimal learning zone.</li>
                <li><b>⭐ Course Quality Rating (15% weight):</b> Verified external learner rating (out of 5.0).</li>
                <li><b>⏱️ Weekly Study Fit (15% weight):</b> Feasibility of course completion based on the employee's weekly time commitment.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with rec_tab3:
        st.subheader("📚 Enterprise Course Catalog & Provider Coverage")
        all_courses = get_all_courses()
        st.caption(f"Covering **{len(all_courses)}** verified courses from Coursera, edX, MIT OCW, freeCodeCamp, and official docs.")
        cat_df = pd.DataFrame(all_courses)[["title", "provider", "skill_name", "level", "duration_hours", "rating"]]
        cat_df.columns = ["Course Title", "Provider", "Target Skill", "Level (1-5)", "Duration (Hours)", "Rating"]
        st.dataframe(cat_df, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# PAGE 5: PERSONALIZED LEARNING ROADMAP
# -------------------------------------------------------------
elif page == "🗺️ Personalized Roadmap":
    render_section_header(
        title="🗺️ Personalized Phased Upskilling Roadmap",
        subtitle=f"Structured learning trajectory for <b>{active_emp['name']}</b> at <b>{active_emp['weekly_learning_hours']} hrs/week</b>.",
        badge="🗺️ PHASED CAREER TRAJECTORY",
        lottie_filename="roadmap.json",
        image_url="https://images.unsplash.com/photo-1508830524289-0adcbe822b40?auto=format&fit=crop&w=600&q=80",
        anim_height=160,
        key_prefix="road_header"
    )

    roadmap = generate_learning_roadmap(current_emp_id)

    # Roadmap Metrics Row with rounded white cards
    rcol1, rcol2, rcol3, rcol4 = st.columns(4)
    with rcol1:
        st.metric("📚 Total Recommended Modules", roadmap["total_courses"])
    with rcol2:
        st.metric("⏱️ Total Learning Commitment", f"{roadmap['total_hours']} hrs")
    with rcol3:
        st.metric("📅 Estimated Program Timeline", f"{roadmap['total_weeks']} weeks")
    with rcol4:
        st.metric("⏳ Weekly Study Pace", f"{roadmap['weekly_hours']} hrs/wk")

    st.markdown("<br>", unsafe_allow_html=True)

    road_tab1, road_tab2, road_tab3 = st.tabs([
        "🏁 Sequential Phased Milestone Steps",
        "📅 Interactive Gantt Schedule Timeline",
        "⚡ Accelerated Study Strategy & Pace"
    ])

    with road_tab1:
        st.subheader("🏁 Phased Learning Milestones")
        st.caption("Each phase builds upon prerequisites to systematically elevate capability to benchmark proficiency.")

        if not roadmap["phases"]:
            st.info("ℹ️ No milestones found. Ensure target role skills are configured.")
        else:
            for phase_name, milestone_list in roadmap["phases"].items():
                st.markdown(f"### 📂 {phase_name}")
                for m in milestone_list:
                    render_roadmap_step_card(m)
                    col_m1, col_m2, _ = st.columns([1.5, 2, 5])
                    with col_m1:
                        st.link_button("🔗 View Course", m["platform_url"])
                    with col_m2:
                        if st.button("➕ Enroll in Module", key=f"road_enroll_{m['course_id']}"):
                            ok, err = enroll_employee_in_course(current_emp_id, m["course_id"])
                            if ok:
                                st.success(f"✅ Enrolled in {m['title']}!")
                                st.rerun()
                            else:
                                st.warning(err)
                    st.markdown("<div style='margin-bottom: 1.25rem;'></div>", unsafe_allow_html=True)

    with road_tab2:
        st.subheader("📅 Interactive Roadmap Timeline (Gantt)")
        timeline_fig = polish_fig(create_roadmap_timeline_chart(roadmap))
        st.plotly_chart(timeline_fig, use_container_width=True)

    with road_tab3:
        st.subheader("⚡ Accelerated Study Pace Simulation")
        st.markdown(f"""
        <div class="white-card">
            <h4>🚀 Fast-Track Your Roadmap:</h4>
            <p>At your current weekly commitment of <b>{roadmap['weekly_hours']} hrs/week</b>, your program duration is estimated at <b>{roadmap['total_weeks']} weeks</b>.</p>
            <div style="display: flex; gap: 16px; margin-top: 1rem; flex-wrap: wrap;">
                <div style="background: #EEF2FF; padding: 12px 18px; border-radius: 12px; border: 1px solid #C7D2FE;">
                    <b>Pace: 5 hrs/week</b> ➔ ~{round(roadmap['total_hours'] / 5.0, 1)} weeks
                </div>
                <div style="background: #F0FDF4; padding: 12px 18px; border-radius: 12px; border: 1px solid #BBF7D0;">
                    <b>Pace: 8 hrs/week</b> ➔ ~{round(roadmap['total_hours'] / 8.0, 1)} weeks
                </div>
                <div style="background: #FDF2F8; padding: 12px 18px; border-radius: 12px; border: 1px solid #FBCFE8;">
                    <b>Pace: 12 hrs/week</b> ➔ ~{round(roadmap['total_hours'] / 12.0, 1)} weeks
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# -------------------------------------------------------------
# PAGE 6: LEARNING PROGRESS TRACKER
# -------------------------------------------------------------
elif page == "📈 Learning Tracker":
    render_section_header(
        title="📈 Employee Learning Progress Tracker",
        subtitle=f"Track active courses, log study hours, and earn automated skill promotions for <b>{active_emp['name']}</b>.",
        badge="📈 REAL-TIME LEARNING TRACKER",
        lottie_filename="celebrate.json",
        image_url="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80",
        anim_height=160,
        key_prefix="track_header"
    )

    tracker_data = get_employee_tracker_summary(current_emp_id)

    # Top tracker metrics
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric("📚 Enrolled Courses", tracker_data["total_enrollments"])
    with t2:
        st.metric("✅ Completed Courses", tracker_data["completed_courses"])
    with t3:
        st.metric("⏱️ Total Hours Invested", f"{tracker_data['total_hours']} hrs")
    with t4:
        st.metric("📈 Avg Course Completion", f"{tracker_data['avg_progress']}%")

    st.markdown("<br>", unsafe_allow_html=True)

    track_tab1, track_tab2, track_tab3 = st.tabs([
        "📖 Active Course Enrollments & Progress",
        "⏱️ Record New Study Activity Session",
        "🏆 Unlocked Badges & Activity History"
    ])

    with track_tab1:
        st.subheader("📖 Current Enrollments & Course Progress")
        enrollments_df = tracker_data["enrollments_df"]

        if enrollments_df.empty:
            st.info("ℹ️ No active course enrollments yet. Visit '💡 Course Recommendations' or '🗺️ Personalized Roadmap' to enroll!")
        else:
            for _, enroll in enrollments_df.iterrows():
                cid = enroll["course_id"]
                st.markdown(f"""
                <div class="white-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #1E293B;">
                            <a href="{enroll['platform_url']}" target="_blank" style="color: #4338CA; text-decoration: none;">
                                🎓 {enroll['title']}
                            </a>
                        </h4>
                        <span style="background: #EEF2FF; color: #4338CA; font-weight: 700; font-size: 0.8rem; padding: 3px 10px; border-radius: 12px;">
                            {enroll['status'].replace('_', ' ').title()}
                        </span>
                    </div>
                    <p style="color: #64748B; font-size: 0.85rem; margin: 4px 0 10px 0;">
                        🎯 <b>Target Skill:</b> {enroll['skill_name']} | 📅 <b>Enrolled:</b> {enroll['enrolled_date']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Progress Bar
                st.progress(enroll["progress_pct"] / 100.0)

                col_p1, col_p2 = st.columns([3, 1])
                with col_p1:
                    new_prog = st.slider(
                        f"Update Progress for: {enroll['title']} (%)",
                        min_value=0,
                        max_value=100,
                        value=int(enroll["progress_pct"]),
                        key=f"slider_prog_{cid}"
                    )
                with col_p2:
                    if st.button("💾 Update Progress", key=f"btn_prog_{cid}"):
                        ok, err, notif = update_course_progress(current_emp_id, cid, new_prog)
                        if ok:
                            if notif:
                                st.balloons()
                                st.success(notif)
                            else:
                                st.success(f"Progress updated to {new_prog}%!")
                            st.rerun()
                        else:
                            st.error(err)
                st.markdown("<hr style='border: 0; height: 1px; background: #E2E8F0; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    with track_tab2:
        st.subheader("⏱️ Record New Study Session")
        if not enrollments_df.empty:
            with st.form("log_study_form"):
                course_map = dict(zip(enrollments_df["title"], enrollments_df["course_id"]))
                selected_course_title = st.selectbox("Select Enrolled Course", list(course_map.keys()))
                hours_input = st.number_input("Study Time (Hours)", min_value=0.5, max_value=20.0, value=2.0, step=0.5)
                notes_input = st.text_area("Learning Notes / Summary", placeholder="Key topics reviewed, code built, or concepts mastered...")

                if st.form_submit_button("📝 Record Study Activity"):
                    cid_selected = course_map[selected_course_title]
                    ok, err = log_learning_activity(current_emp_id, cid_selected, hours_input, notes_input)
                    if ok:
                        st.success(f"✅ Successfully logged {hours_input} hrs for {selected_course_title}!")
                        st.rerun()
                    else:
                        st.error(err)
        else:
            st.info("ℹ️ Enroll in a course first to record study activity logs.")

    with track_tab3:
        st.subheader("🏆 Unlocked Achievement Badges")
        if tracker_data["badges"]:
            b_cols = st.columns(min(4, len(tracker_data["badges"])))
            for i, b in enumerate(tracker_data["badges"]):
                with b_cols[i % len(b_cols)]:
                    st.markdown(f"""
                    <div class="badge-pill-card">
                        <div style="font-size: 2.2rem; margin-bottom: 6px;">{b['icon']}</div>
                        <h4 style="margin: 0; color: #1E293B;">{b['title']}</h4>
                        <p style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">{b['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.caption("Enroll in courses and log study hours to unlock achievements.")

        if tracker_data["recent_logs"]:
            st.markdown("---")
            st.subheader("📜 Recent Learning Activity History")
            for rlog in tracker_data["recent_logs"]:
                st.caption(f"⏱️ **{rlog['hours_spent']} hrs** on *{rlog['course_title']}* ({rlog['logged_at']})")
                if rlog["notes"]:
                    st.write(f"> 💬 {rlog['notes']}")


# -------------------------------------------------------------
# PAGE 7: HR WORKFORCE ANALYTICS
# -------------------------------------------------------------
elif page == "📊 HR Workforce Analytics":
    render_section_header(
        title="📊 HR Workforce Talent Intelligence",
        subtitle="Company-wide skill distribution, department benchmark readiness, and organizational skill deficits.",
        badge="📊 MACRO TALENT INTELLIGENCE",
        lottie_filename="growth.json",
        image_url="https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=600&q=80",
        anim_height=160,
        key_prefix="hr_header"
    )

    overview = get_workforce_overview()

    # Macro KPIs with rounded cards
    hkpi1, hkpi2, hkpi3, hkpi4 = st.columns(4)
    with hkpi1:
        st.metric("👥 Total Workforce Tracked", overview["total_employees"])
    with hkpi2:
        st.metric("🎯 Company Avg Skill Readiness", f"{overview['avg_readiness']}%")
    with hkpi3:
        st.metric("⏱️ Cumulative Training Hours", f"{overview['overall_training_hours']} hrs")
    with hkpi4:
        st.metric("📚 Total Active Course Enrollments", overview["total_enrollments"])

    st.markdown("<br>", unsafe_allow_html=True)

    hr_tab1, hr_tab2, hr_tab3 = st.tabs([
        "🏢 Departmental Upskilling & Talent Mobility",
        "⚠️ Organizational Skill Deficits & Heatmap",
        "👥 Workforce Talent Mobility Master Index"
    ])

    with hr_tab1:
        col_hr1, col_hr2 = st.columns([1.3, 1])
        with col_hr1:
            st.subheader("🏢 Departmental Upskilling Readiness (%)")
            dept_fig = polish_fig(create_department_readiness_chart(overview["department_metrics"]))
            st.plotly_chart(dept_fig, use_container_width=True)

        with col_hr2:
            st.subheader("🔄 Talent Mobility Proportions")
            mobility_fig = polish_fig(create_talent_mobility_donut(overview["employee_readiness_df"]))
            st.plotly_chart(mobility_fig, use_container_width=True)

    with hr_tab2:
        col_hr3, col_hr4 = st.columns([1, 1.3])
        with col_hr3:
            st.subheader("⚠️ Top Critical Organizational Skill Gaps")
            gaps_fig = polish_fig(create_org_gaps_chart(overview["top_org_gaps"]))
            st.plotly_chart(gaps_fig, use_container_width=True)

        with col_hr4:
            st.subheader("🗺️ Departmental Skill Proficiency Heatmap")
            heatmap_fig = polish_fig(create_skill_distribution_heatmap())
            st.plotly_chart(heatmap_fig, use_container_width=True)

    with hr_tab3:
        st.subheader("👥 Employee Talent Mobility Index Table")
        if not overview["employee_readiness_df"].empty:
            st.dataframe(
                overview["employee_readiness_df"][[
                    "name", "department", "current_role", "target_role", "readiness_score", "critical_gap_count", "mobility_status"
                ]],
                use_container_width=True,
                hide_index=True
            )
