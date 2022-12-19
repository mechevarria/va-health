import streamlit as st
import requests
from numerize.numerize import numerize

import pandas as pd
import numpy as np
import matplotlib

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from streamlit_d3graph import d3graph


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def build_adjaceny_matrix(data):
    items = [x[0] for x in data] + [x[1] for x in data] 
    v = list(set(items))

    # #create matrix of size V
    df = pd.DataFrame(0, index=v, columns=v)
    for pair in data:
        # if not pair[0] == pair[1]:
        #     df.loc[str(pair[0]),str(pair[1])] = 1 
        df.loc[str(pair[0]),str(pair[1])] = 1 
    return df

st.set_page_config(layout="wide")



st.title("Clinical Dashboard")

#KPI Section
@st.cache(suppress_st_warning=True)
def get_kpi(filter_id=None):
    kpi_url = "http://localhost:5000/kpi"

    if filter_id:
        kpi_url = "http://localhost:5000/kpi/filter_id"
    
    response = requests.get(kpi_url)
    return response.json()

kpis = get_kpi()
with st.container():
    cols = st.columns(7)

    for e, r in enumerate(kpis):
        with cols[e+1]:
            st.metric(label=r['name'], value=r['value'], delta="1")


#Network Graph Section
@st.cache(suppress_st_warning=True)
def get_graph(color_name='A1Clast_period2_to_4_change'):
    graph_url = "http://localhost:5000/graph"
    response = requests.post(graph_url, json={
    	"color_name": color_name
    })

    return response.json()

g = get_graph()
with st.container():
    st.header("Patient Segments")
    # Initialize
    d3 = d3graph(slider=[1,4])

    data = g['data']
    df = build_adjaceny_matrix(data)

    #Build colormap and size vectors
    cmin = min(n['colorIndex'] for n in g['nodes'])
    cmax = max(n['colorIndex'] for n in g['nodes'])
    norm = matplotlib.colors.Normalize(vmin=cmin, vmax=cmax)
    m = cm.ScalarMappable(norm=norm, cmap=cm.hsv)

    color=[m.to_rgba(n['colorIndex']) for n in g['nodes']]
    color=[rgb_to_hex((int(n[0]*255), int(n[1]*255), int(n[2]*255)))  for n in color]
    size=[n['radius'] for n in g['nodes']]

    d3.graph(df)
    # d3.set_node_properties(color=color)
    d3.set_node_properties(size=size, color=color)
    d3.show(figsize = (1200,300), title='Cohort Network')

#Top Explainers section
@st.cache(suppress_st_warning=True)
def get_explain(filter_id=None):
    explain_url = "http://localhost:5000/explain"
    if filter_id: graph_url = "http://localhost:5000/explain/filter_id"

    response = requests.get(explain_url)
    return response.json()

explains = get_explain()
details_chk_boxes = {}
with st.container():
    cols = st.columns(3)

    for e, r in enumerate(explains):
        with cols[e % 3]:
            # st.write(r)
            with st.expander(f"{r['id']}   |    Patients: {r['group_size']}    |    # Explains: {len(r['explains'])}"):
                details_chk_boxes[r['id']] = st.checkbox('View Details', key=r['id'])
                for ex in r['explains']:
                    st.write(ex)

#details view
@st.cache(suppress_st_warning=True)
def get_group_details(group_id):
    group_url = f"http://localhost:5000/group/{group_id}" 
    response = requests.get(group_url)
    return response.json()

def gen_box_plt(data, label=None):

    stats = [
        {'med': data[2], 'q1': data[1], 'q3': data[4], 'whislo': data[0], 'whishi': data[4]}
    ]

    fig,ax = plt.subplots(1, figsize=(5, 0.5))

    ax.bxp(stats, showfliers=False, vert=False, patch_artist=True);
    formated_label = "{:>75}".format(label)
    ax.set_yticklabels([formated_label]);
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', labelsize=8)
    return(fig)

#Get the clicked on
# for gid, v in details_chk_boxes.items():
#     if v:
#         details = get_group_details(gid)
#         with st.container():
#             cols = st.columns(2)
#             with cols[1]:
#             for detail in details['explains']:
#                 if detail["type"] =="continuous":
#                     with cols[0]:
#                         b = gen_box_plt(detail['primary_group_quartiles'], detail["name"])
#                         st.pyplot(b)
#                 else:
#                     with cols[1]:
#                          with sub_cols[1]:
#                             st.write(detail["name"])
#                          with sub_cols[2]:
#                             st.progress(detail['primary_group_percent']/100)

for k in details_chk_boxes.keys():
    details_chk_boxes[k] = False