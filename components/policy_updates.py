import streamlit as st
from models.database import db, Enterprise, EnterprisePolicy
from utils.government_api import GovernmentPolicyAPI

def render_policy_updates(doc_manager, ai_analyzer, enterprise):
    st.title("Policy Updates")
    
    # Add API test button
    if st.button("Test AI API Connection"):
        result = ai_analyzer.test_api_key()
        if result is True:
            st.success("API connection successful!")
        else:
            st.error(f"API connection failed: {result}")

    if not enterprise:
        # Enterprise setup for first-time users
        st.warning("Please set up your enterprise first")
        with st.form("enterprise_setup"):
            enterprise_name = st.text_input("Enterprise Name")
            industry = st.selectbox("Industry", [
                "Technology", "Healthcare", "Finance", 
                "Manufacturing", "Education", "Retail"
            ])
            initial_policy = st.text_area("Enter your current policy", 
                help="If you have an existing policy, paste it here")

            if st.form_submit_button("Set Up Enterprise"):
                if enterprise_name and industry:
                    try:
                        # Create enterprise
                        new_enterprise = Enterprise(
                            name=enterprise_name,
                            industry=industry
                        )
                        db.add(new_enterprise)
                        db.flush()

                        # Update user's enterprise
                        st.session_state.user.enterprise_id = new_enterprise.id

                        # Add initial policy if provided
                        if initial_policy:
                            enterprise_policy = EnterprisePolicy(
                                enterprise_id=new_enterprise.id,
                                title=f"{industry} Policy",
                                content=initial_policy,
                                version=1
                            )
                            db.add(enterprise_policy)

                        db.commit()
                        st.success("Enterprise setup complete! Please refresh the page.")
                        st.rerun()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Error setting up enterprise: {e}")
        return

    # Display existing policies and updates
    enterprise_policies = db.query(EnterprisePolicy).filter_by(
        enterprise_id=enterprise.id
    ).all()

    if not enterprise_policies:
        st.info("No policies found. Let's create your first policy.")
        with st.form("create_policy"):
            policy_title = st.text_input("Policy Title")
            policy_content = st.text_area("Policy Content")

            if st.form_submit_button("Create Policy"):
                if policy_title and policy_content:
                    try:
                        new_policy = EnterprisePolicy(
                            enterprise_id=enterprise.id,
                            title=policy_title,
                            content=policy_content,
                            version=1
                        )
                        db.add(new_policy)
                        db.commit()
                        st.success("Policy created successfully!")
                        st.rerun()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Error creating policy: {e}")
        return

    # Compare with government policies
    gov_api = GovernmentPolicyAPI()
    relevant_policies = gov_api.search_policies(enterprise.industry)

    st.subheader("Policy Analysis")
    for ep in enterprise_policies:
        with st.expander(f"Policy: {ep.title} (v{ep.version})"):
            st.write("Current Policy Content:")
            st.write(ep.content)

            # Find relevant government policies
            st.write("### Current Enterprise Policy:")
            st.write(ep.content)
            
            matching_gov_policy = None
            for gov_policy in relevant_policies:
                if enterprise.industry.lower() in gov_policy['title'].lower():
                    matching_gov_policy = gov_policy
                    break
            
            if matching_gov_policy:
                st.write("### Relevant Government Policy:")
                st.write(matching_gov_policy['content'])
                
                comparison = ai_analyzer.compare_policies(ep.content, matching_gov_policy['content'])
                
                st.write("### Analysis:")
                st.write(f"Similarity Score: {comparison.get('similarity_score', 0):.2f}")
                st.write("Impact Analysis:", comparison['impact_analysis'])
                
                if comparison.get('similarity_score', 0) < 0.8:
                    st.warning("Policy Update Recommended")
                    updated_policy = ai_analyzer.update_policy(
                        ep.content,
                        matching_gov_policy['content'],
                        enterprise.industry
                    )
                    
                    st.write("### Suggested Updated Policy:")
                    st.write(updated_policy)
                    
                    if st.button("Accept This Policy Update"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_area("Current Version", ep.content, height=200)
                        with col2:
                            st.text_area("Suggested Update", updated_policy, height=200)

                        if st.button(f"Accept Update for {ep.title}"):
                            try:
                                ep.content = updated_policy
                                ep.version += 1
                                db.commit()
                                st.success("Policy updated successfully!")
                                st.rerun()
                            except Exception as e:
                                db.rollback()
                                st.error(f"Error updating policy: {e}")