
import streamlit as st
import pandas as pd

def render_search(doc_manager, enterprise=None):
    st.title("Search Policies")

    # Search Interface
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search policies by title or content")
    with col2:
        search_type = st.selectbox("Search in", ["All", "Title", "Content", "Department"])

    if search_query:
        results = doc_manager.search_policies(search_query, search_type.lower())

        if results:
            st.subheader(f"Found {len(results)} results")

            # Display results in a clean table
            df = pd.DataFrame(results)
            df['updated_at'] = pd.to_datetime(df['updated_at'])

            # Create expandable sections for each result
            for _, row in df.iterrows():
                with st.expander(f"{row['title']} - {row['department']}"):
                    st.write(f"Last updated: {row['updated_at'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"Version: {row['version']}")
                    st.markdown("#### Content Preview")
                    preview = row['content'][:200] + "..." if len(row['content']) > 200 else row['content']
                    st.write(preview)

                    if st.button("View Full Policy", key=f"view_{row['id']}"):
                        st.session_state.current_page = 'policy_viewer'
                        st.session_state.selected_policy = row['id']
        else:
            st.info("No policies found matching your search.")
