import plotly.express as px

def create_timeline(df):

    fig = px.scatter(
        df,
        x="Date",
        y="Sender",
        color="Sender",
        title="Communication Timeline"
    )

    return fig
