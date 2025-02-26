import streamlit as st
from models.database import db, GovernmentPolicy, EnterprisePolicy

def render_policy_viewer(doc_manager, version_control):
    st.title("Policy Viewer")

    # Tab selection
    tab1, tab2 = st.tabs(["Government Policies", "Enterprise Policies"])

    with tab1:
        st.subheader("Government Policies")
        categories = ["All"] + [cat for cat, in db.query(GovernmentPolicy.category).distinct()]
        selected_category = st.selectbox("Filter by category", categories)

        query = db.query(GovernmentPolicy)
        if selected_category != "All":
            query = query.filter(GovernmentPolicy.category == selected_category)

        policies = query.all()

        for policy in policies:
            with st.expander(f"{policy.title} ({policy.category})"):
                st.write("**Content:**")
                st.write(policy.content)
                st.write("**Effective Date:**", policy.effective_date)

    with tab2:
        st.subheader("Enterprise Policies")
        if 'user' in st.session_state and st.session_state.user.enterprise_id:
            enterprise_policies = db.query(EnterprisePolicy).filter_by(
                enterprise_id=st.session_state.user.enterprise_id
            ).all()

            for policy in enterprise_policies:
                with st.expander(f"{policy.title} (v{policy.version})"):
                    st.write("**Content:**")
                    st.write(policy.content)
                    st.write("**Last Updated:**", policy.updated_at)
        else:
            st.info("Please select an enterprise to view its policies")