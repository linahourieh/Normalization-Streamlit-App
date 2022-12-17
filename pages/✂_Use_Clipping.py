from backend.src import create_dist_plot, clip_feature, convert_df
import streamlit as st

#
st.title("How clipping would affect my data?")

# get the saved data
df = st.session_state['df']
num_cols = st.session_state['num_cols']


# function to display the values of the slider
def display_value():
    st.sidebar.write("The value of the slider is:", st.session_state.myslider)


# ----------- streamlit skeleton
cola, col_b = st.columns(2)

# ----------- widgets
feature = col_b.selectbox('Select the feature you want to apply clipping on', list(num_cols))
range_slider = col_b.slider('Select a value to clip the data to:', value=[df[feature].min(), df[feature].max()],
                            key="myslider", on_change=display_value)
bin_size = col_b.slider('Select your bin size:', 0.0, 5.0, 0.2)
button = col_b.button('Confirm changes', help='Save your clipped feature')
col_b.metric(value=' ', label='Advices', help='1. Useful when feature contains extreme outliers.')

# ---------- apply the backend function
data = clip_feature(df, feature, range_slider[0], range_slider[1])

# ---------- draw up the visualization plots
cola.plotly_chart(create_dist_plot(data, feature, colorhash='#abbfe0',
                                   bin_size=bin_size,
                                   curve_type='kde',
                                   show_curve=False,
                                   title='Clipped Data'))
st.download_button(
    label="Download Clipped Data as CSV",
    data=convert_df(data),
    file_name='df_clipped.csv',
    mime='text/csv',
)

if button:
    st.session_state['df'] = data
    col_b.success('Updated your Dataframe Successfully!')
