import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute

st.session_state['url'] = st.text_input("Enter Databricks URL")
st.session_state['token'] = st.text_input("Enter token")


if st.button("List Scopes"):
    w = WorkspaceClient(host=st.session_state['url'], token=st.session_state['token'])
    scopes = w.secrets.list_scopes()
    st.dataframe(scopes)
    
with st.expander("Create scope"):
    v_scope_name = st.text_input("scope name")
    if st.button("Create"):
        w = WorkspaceClient(host=st.session_state['url'], token=st.session_state['token'])
        w.secrets.create_scope(scope=v_scope_name)



    