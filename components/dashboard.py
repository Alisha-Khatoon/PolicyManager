import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard(doc_manager, ai_analyzer, enterprise=None):
    st.title("Policy Management Dashboard")

    # Statistics Cards
    col1, col2, col3 = st.columns(3)

    policies = doc_manager.get_all_policies()
    total_policies = len(policies)

    with col1:
        st.metric("Total Policies", total_policies)

    with col2:
        departments = len(set(policy['department'] for policy in policies))
        st.metric("Departments", departments)

    with col3:
        updates_this_month = sum(
            1 for policy in policies
            if (pd.Timestamp.now() - pd.Timestamp(policy['updated_at'])).days <= 30
        )
        st.metric("Updates This Month", updates_this_month)

    # Policy Upload Section
    st.subheader("Upload New Policy")
    with st.form("policy_upload"):
        title = st.text_input("Policy Title")
        department = st.selectbox(
            "Department",
            ["HR", "IT", "Finance", "Legal", "Operations"]
        )
        content = st.text_area("Policy Content")

        if st.form_submit_button("Upload Policy"):
            if title and content:
                policy_id = doc_manager.add_policy(title, content, department)
                analysis = ai_analyzer.analyze_policy(content)
                st.success("Policy uploaded successfully!")
                st.json(analysis)
            else:
                st.error("Please fill in all fields.")

    # Recent Policies Table
    st.subheader("Recent Policies")
    if policies:
        df = pd.DataFrame(policies)
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        df = df.sort_values('updated_at', ascending=False).head(5)

        st.dataframe(
            df[['title', 'department', 'updated_at', 'version']],
            hide_index=True
        )
    else:
        st.info("No policies uploaded yet.")

    # Department Distribution Chart
    if policies:
        st.subheader("Policy Distribution by Department")
        dept_counts = pd.DataFrame(policies)['department'].value_counts()
        fig = px.pie(
            values=dept_counts.values,
            names=dept_counts.index,
            title="Policies by Department"
        )
        st.plotly_chart(fig)