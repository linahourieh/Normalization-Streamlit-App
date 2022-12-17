import streamlit as st
from backend.src import create_dist_plot, normalization_board, upload_data, encoded_data_checker, convert_df, draw_box


st.title("How scaling would affect my data?")
df = st.session_state['df']
num_cols = st.session_state['num_cols']
df_minmax, df_maxabs, df_rob = normalization_board(df, num_cols)



with st.container():
    cola, colb= st.columns([0.80, 0.2])

    with colb:
        list_features = st.multiselect(label='Select a set of features to compare, You can select up to 6', default=num_cols[:3],
                                      options= num_cols, max_selections=6)
        st.markdown("""## Advices
1. Your data is then roughly evenly distributed over this area.
2. You know the approximate upper and lower bounds of your data with few or no outliers.
                       """)

    with cola:
        st.plotly_chart(draw_box(df, list_features, 'Without Scaling', showle=False))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Min Max Scaler')
        with st.expander('What is happening?'):
            st.text(
                """
                The Min Max Scaler scaled each feature to be 
                between 0 and 1.
                """
            )
        st.plotly_chart(draw_box(df_minmax, list_features, 'Min Max Scaling', showle=False))

    with col2:
        st.subheader('Max Abs Scaler')
        with st.expander('What is happening?'):
            st.text(
                """
                The Max Abs Scaler scaled
                each feature by its maximum absolute value.
                If your features contains only positive values
                then you might see that the range will be between
                [0,1]. However, if it contains negative values then 
                you might see that the range will be between 
                [-1,0], and if it contains both: [-1,1]

                """
            )
        st.plotly_chart(draw_box(df_maxabs, list_features, 'Max Abs Scaling', showle=False))
    with col3:
        st.subheader('Robust Scaler')
        with st.expander('What is happening?'):
            st.text(
                """
                Scales each feature according to be between its
                1st quantile and its 3rd quantile.
                Robust scaling performs standardization by 
                centering the data around the median.
                """
            )
        st.plotly_chart(draw_box(df_rob, list_features, 'Robust Scaling', showle=False))

    with st.container():
        st.header('How my data is changed?')
        st.subheader('Original Data')
        st.dataframe(df.head())
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Min Max Scaler')
            st.dataframe(df_minmax.head())
            st.download_button(
                label="Download data as CSV",
                data=convert_df(df_minmax),
                file_name='df_norm.csv',
                mime='text/csv',
            )
        with col2:
            st.subheader('Max Abs Scaler')
            st.dataframe(df_maxabs.head())
            st.download_button(
                label="Download data as CSV",
                data=convert_df(df_maxabs),
                file_name='df_maxabs.csv',
                mime='text/csv',
            )
        with col3:
            st.subheader('Robust Scaler')
            st.dataframe(df_rob.head())
            st.download_button(
                label="Download data as CSV",
                data=convert_df(df_rob),
                file_name='df_rob.csv',
                mime='text/csv',
            )


