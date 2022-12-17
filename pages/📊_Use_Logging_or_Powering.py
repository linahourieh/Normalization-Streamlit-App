from backend.src import log_transform, create_dist_plot, PowerTransformer, PowerTransformer1
import streamlit as st

# title
st.title("How applying log would affect my data?")

# get the saved data
df = st.session_state['df']
num_cols = st.session_state['num_cols']

# ----------- streamlit skeleton
col_a, col_b, col_c = st.columns([0.4, 0.4, 0.2])

# ----------- widgets
feature = col_c.selectbox('Select the feature you want to apply log scale on', list(df.columns))
log_type = col_c.radio('Select the log type you wish to apply', ['log', 'log2', 'log10'])
bin_size = col_c.slider('Select your bin size:', 0.0, 5.0, (0.2))

# ---------- apply the backend function
df_logged = log_transform(df, feature, log_type)

# ---------- draw up the visualization plots
col_a.plotly_chart(create_dist_plot(df,
                                    feature=feature,
                                    colorhash='#e0baab',
                                    bin_size=bin_size,
                                    curve_type='kde',
                                    show_curve=False,
                                    title='Original Data'))

col_b.plotly_chart(create_dist_plot(df_logged,
                                    feature=feature,
                                    colorhash='#f0765d',
                                    bin_size=bin_size,
                                    curve_type='kde',
                                    show_curve=False,
                                    title=f'Data with {log_type}'))
button = col_c.button('Transform all features', help='all features will be changed.')

# ---------- save the changes
if button:
    st.session_state['df'] = log_transform(df, feature, log_type)
    st.success('Updated your Dataframe Successfully!')

# title
st.title("How applying PowerTransformation would affect my data?")

# ----------- streamlit skeleton
col1, col2, col3 = st.columns([0.4, 0.4, 0.2])

# ----------- widgets
feature = col3.selectbox('Select the feature you want to apply log scale on', list(df.columns), key=34)
bin_size = col3.slider('Select your bin size:', 0.0, 5.0, 0.2, key=234)

# ---------- apply the backend function
df_power = PowerTransformer1(df, num_cols)

# ---------- draw up the visualization plots
col1.plotly_chart(create_dist_plot(df,
                                   feature=feature,
                                   colorhash='#e0baab',
                                   bin_size=bin_size,
                                   curve_type='kde',
                                   show_curve=False,
                                   title='Original Data'))
col2.plotly_chart(create_dist_plot(df_power,
                                   feature=feature,
                                   colorhash='#f0765d',
                                   bin_size=bin_size,
                                   curve_type='kde',
                                   show_curve=False,
                                   title=f'Data with {log_type}'))
button = col3.button('Transform all features', help='All features will be changed.', key=4536)

# ---------- save the changes
if button:
    st.session_state['df'] = df_power
    st.success('Updated your Dataframe Successfully!')
