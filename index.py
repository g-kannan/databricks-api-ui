import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute

st.set_page_config("Litbricks", "https://streamlit.io/favicon.svg",layout="wide")
st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=78)

st.write(
    """
    # LitBricks

    Welcome to LitBricks! 👋 This app helps to work with Databricks API easily via Streamlit ✨
    """
)

host_name = st.text_input("Enter Databricks URL")
token = st.text_input("Enter token", type="password")

with st.expander("Create cluster policy"):
    st.info('*NOTE:* Policies require the Premium plan', icon="ℹ️")
    st.link_button("Go to Policy Definition guide", "https://learn.microsoft.com/en-us/azure/databricks/administration-guide/clusters/policy-definition")
    v_policy_name = st.text_input("Policy name")
    v_policy_desc = st.text_input("Policy description")
    auto_term_mins = st.number_input("Idle Minutes to Terminate cluster",min_value=10,step=1)
    photon_required = st.selectbox("Photon Required?",("Yes",'No'))
    spot_usage = st.checkbox("Use Spot Instances")
    if spot_usage:
        availability_mode = "SPOT_WITH_FALLBACK_AZURE"
    else:
        availability_mode =  "ON_DEMAND_AZURE"
    auto_scale = st.checkbox('Enable Autoscaling')
    
    if photon_required == "Yes":
        v_runtime = "PHOTON"
    elif photon_required == "No":
        v_runtime = "STANDARD"
    
    if auto_scale:
        autoscale_min_workers = st.number_input("Minimum workers required",min_value=1,step=1)
        autoscale_max_workers = st.number_input("Maximum workers required",min_value=2,max_value=50,step=1)
        policy_def = f"""{{        
        "autotermination_minutes": {{"type": "fixed","value": {auto_term_mins}}},
        "spark_version": {{"type": "fixed","value": "auto:latest-lts"}},
        "runtime_engine": {{"type": "fixed","value": "{v_runtime}","hidden": true}},
        "azure_attributes.availability": {{"type": "fixed","value": "{availability_mode}","hidden": false}},
        "autoscale.min_workers": {{"type": "fixed", "value": {autoscale_min_workers}}},
        "autoscale.max_workers": {{"type": "fixed", "value": {autoscale_max_workers}}},
        "custom_tags.policy_created_by": {{"type": "fixed","value": "API"}}
        }}"""
    else:
        policy_def = f"""{{        
        "autotermination_minutes": {{"type": "fixed","value": {auto_term_mins}}},
        "spark_version": {{"type": "fixed","value": "auto:latest-lts"}},
        "runtime_engine": {{"type": "fixed","value": "{v_runtime}","hidden": true}},
        "azure_attributes.availability": {{"type": "fixed","value": "{availability_mode}","hidden": false}},
        "spark_conf.spark.databricks.cluster.profile": {{"type": "fixed","value": "singleNode","hidden": true}},
        "custom_tags.policy_created_by": {{"type": "fixed","value": "API"}}
        }}"""
    

    # json_data = json.dumps(policy_def)
    if st.button("View Policy Definition JSON"):
        st.code(policy_def, language='json')
        
    if st.button("Create"):
        st.write(policy_def)
        w = WorkspaceClient(host=host_name, token=token)

        created = w.cluster_policies.create(
            name=v_policy_name,
            description=v_policy_desc,
            definition=policy_def,
        )
        st.dataframe(created)



if st.button("List cluster policy"):
    w = WorkspaceClient(host=host_name, token=token)
    list_cluster_policies = w.cluster_policies.list()
    st.dataframe(list_cluster_policies,column_order=("created_at_timestamp","policy_id","Name","is_default","description","definition"),use_container_width=True)
    

if st.button("List Clusters"):
    w = WorkspaceClient(host=host_name, token=token)
    all = w.clusters.list()
    st.dataframe(all)

if st.button("List Jobs"):
    w = WorkspaceClient(host=host_name, token=token)
    job_list = w.jobs.list(expand_tasks=False)
    st.dataframe(job_list)

if st.button("List Catalog"):
    w = WorkspaceClient(host=host_name, token=token)
    all = w.metastores.list()
    st.dataframe(all)
    
st.info(
    """
    Need a feature that's not on here?
    [Let us know by opening a GitHub issue!](https://github.com/g-kannan/databricks-api-ui/issues)
    """,
    icon="👾",
)