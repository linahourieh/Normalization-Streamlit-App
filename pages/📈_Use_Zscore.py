import plotly.figure_factory as ff
from backend.src import StandardScaling, convert_df, Standardscaling_feature
import streamlit as st

#
st.title("How applying Z-score would affect my data?")

# get the saved data
df = st.session_state['df']
num_cols = st.session_state['num_cols']

# ----------- streamlit skeleton
col_a, col_b = st.columns([0.75, 0.25])

# ----------- widgets
feature = col_b.selectbox('Select the feature you want to apply log scale on', list(num_cols))
histnorm = col_b.radio('Select What to represent', ['probability', 'probability density'], help="""**Probability** is 
a specific value realized over the range of [0, 1].It tells us the likelihood to obtain a certain data point 𝒙. 
**Probability density** means how dense the probability is near a certain data point 𝒙. """)
curve_type = col_b.radio('Pick a curve type:', ('kde', 'normal'))
col_b.metric(value=' ', label='Advices',
             help='1. Use this method when your feature distribution contains no extreme outliers.')
button_feature = col_b.button('Transform only this feature')
button_all = col_b.button('Transform all features')

# ---------- apply the backend function
df_stand = StandardScaling(df, num_cols)
df_stand_f = Standardscaling_feature(df, feature)


# ---------- draw up the visualization plots
my_fig = ff.create_distplot(
    [df.loc[:, feature], df_stand.loc[:, feature]],
    group_labels=['Before applying Z-Score', 'After applying Z-Score '],
    show_curve=True,
    colors=['#dfff94', '#f06099'],
    bin_size=0.2,
    curve_type=curve_type,
    show_hist=False,
    show_rug=False,
    histnorm=histnorm)
my_fig.update_layout(title_text='Original and Normalized ',
                     title_x=0.05,
                     xaxis_title="Values that your feature can take",
                     yaxis_title=histnorm,
                     width=100,
                     height=100,
                     legend=dict(
                         yanchor="auto",
                         y=1.2,
                         xanchor="auto",
                         x=1),
                     template='plotly_white',
                     plot_bgcolor="rgb(255,255,255)",
                     font=dict(family="Courier New, monospace",
                               size=14))
col_a.plotly_chart(my_fig)

# ---------- save the changes
if button_all:
    st.session_state['df'] = df_stand
    col_b.success('Updated your whole Dataframe Successfully!')

if button_feature:
    st.session_state['df'] = df_stand_f
    col_b.success('Updated your feature Successfully!')

col1, col2 = st.columns(2)
col1.subheader('Before Applying Z-score')
col2.subheader('After Applying Z-score')
col1.dataframe(df.describe().iloc[1:3, :-1])
col2.dataframe(df_stand.describe().iloc[1:3, :])
col1.download_button(
    label="Download Z-score data as csv",
    data=convert_df(df_stand),
    file_name='df_stand.csv',
    mime='text/csv',
)
