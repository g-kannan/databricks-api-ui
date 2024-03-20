import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute

st.set_page_config(
    layout="wide"
)
host_name = st.text_input("Enter Databricks URL")
token = st.text_input("Enter token",type='password')

if st.button("list cluster policy"):
    w = WorkspaceClient(host=host_name, token=token)
    all = w.cluster_policies.list()
    st.table(all)


if st.button("Create cluster policy"):
    w = WorkspaceClient(host=host_name, token=token)

    created = w.cluster_policies.create(name=f'sdk-clusterpolicy',
                                    definition="""{
            "spark_conf.spark.databricks.delta.preview.enabled": {
                "type": "fixed",
                "value": true
            }
        }
""")
    st.write(created)

if st.button("List Clusters"):
    w = WorkspaceClient(host=host_name, token=token)
    all = w.clusters.list()
    st.write(created)

if st.button("List Jobs"):
    w = WorkspaceClient(host=host_name, token=token)
    job_list = w.jobs.list(expand_tasks=False)
    st.write(job_list)

if st.button("List Catalog"):
    w = WorkspaceClient(host=host_name, token=token)
    all = w.metastores.list()
    st.table(all)