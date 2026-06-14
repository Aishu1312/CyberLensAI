import plotly.express as px
from modules.timeline import create_timeline

def create_timeline(df):
fig = create_timeline(df)
st.plotly_chart(fig)
    fig = px.scatter(
        df,
        x="Date",
        y="Sender",
        color="Sender",
        title="Communication Timeline"
    )

    return fig
