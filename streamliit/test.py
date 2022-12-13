import streamlit as st
from streamlit_d3graph import d3graph
import matplotlib
import matplotlib.cm as cm

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# Initialize
d3 = d3graph()
# Load karate example
adjmat, df = d3.import_example('karate')

label = df['label'].values
node_size = df['degree'].values

d3.graph(adjmat)
color = ['#00FF00' for i in label]

norm = matplotlib.colors.Normalize(vmin=-0, vmax=32)
m = cm.ScalarMappable(norm=norm, cmap=cm.hot)

color=[m.to_rgba(n)  for n in range(len(label))]
color=[rgb_to_hex((int(n[0]*255), int(n[1]*255), int(n[2]*255)))  for n in color]
# st.write(color)

# d3.set_node_properties(color=df['label'].values)
d3.set_node_properties(color=color)
d3.show()

# d3.set_node_properties(label=label, color=label, cmap='Set1')
# d3.show()
