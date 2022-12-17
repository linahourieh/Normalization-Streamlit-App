import streamlit as st
import pandas as pd

st.set_page_config(page_title='Normalization Dashboard', page_icon='📐', layout='wide', initial_sidebar_state='auto')


def streamlit_layout():
    # -------------------------------------streamlit outline
    st.title('Normalization')

    with st.container():
        cola, colc = st.columns([1, 1.5])
        cola.header('What is Normalization?')
        cola.text(
            """
            Normalization is a scaling technique in which all features 
            values are shifted and rescaled so that they end up
            between a similar range, for example: 0 and 1""")
        cola.header('Why should I care?')
        cola.text(
            """
            Simply, it might affect your algorithm performance.
            """)

        from PIL import Image
        image = Image.open('images/noramlize.jpeg')

        colc.image(image)  # , caption='Normalised vs Normalized data')

    with st.container():
        tab1, tab2, tab3 = st.tabs(
            ["Distance Based Algorithms", "Gradient Descent Based Algorithms", "Tree-Based Algorithms"])

        with tab1:
            with st.container():
                st.header("Distance Based Algorithms 📏")
                col1, col2, col3 = st.columns([1.5, 1, 1])
                col2.metric('For KNN, K-means, and SVM', 'Highly Recommended', delta='Algorithms are highly affects')
                col1.text(
                    """
                   Distance algorithms like KNN, K-means, and SVM 
                   are most affected by the range of features. This is 
                   because behind the scenes they are using distances 
                   between data points to determine their similarity.""")

                col1.text(
                    """
                   If features have different scales, there is a chance
                   that higher weight/importance is given to features that possess
                   high values. This will impact the performance of the algorithm
                   and obviously, we do not want our algorithm to be biased towards
                   one feature. """
                )
        with tab2:
            with st.container():
                st.header("Gradient Descent Based Algorithms 🎯")
                col1, col2, col3 = st.columns([1.5, 1, 1])
                with col2:
                    st.metric('For linear regression, logistic regression, and neural networks', 'Highly Recommended',
                              delta='Algorithms are highly affects')
                with col1:
                    st.text(
                        """
                        Machine learning algorithms like linear regression,
                        logistic regression, neural network, etc. that use
                        gradient descent as an optimization technique require
                        data to be scaled. """)

                    st.text(
                        """
                        The difference in features' range will cause the gradient
                        descent to take steps of different sizes for each feature.
                        Thus, the steps that gradient descent takes will not be updated
                        at the same rate, and the algorithm might not be able to converge
                        smoothly to the global minima."""
                    )

        with tab3:
            with st.container():
                st.header("Tree-Based Algorithms 🌲")
                col1, col2, col3 = st.columns([1.5, 1, 1])
                with col2:
                    st.metric('Decision Tree, Random Forests, XGBoost', 'Not Recommended',
                              delta='Algorithms are not affected', delta_color='inverse')
                with col1:
                    st.text(
                        """
                        Tree-based algorithms, on the other hand, are fairly insensitive
                        to the scale of the features. Think about it, a decision tree is only
                        splitting a node based on a single feature. The decision tree splits a
                        node on a feature that increases the homogeneity of the node. This split
                        on a feature is not influenced by other features. """)

                    st.text(
                        """
                        So, there is virtually no effect of the remaining features on the split.
                        This is what makes them invariant to the scale of the features!."""
                    )


with st.sidebar:
    checkbox1 = st.checkbox('Use Example Data', True)
    if checkbox1:
        df = pd.read_csv('Data/data_banknote_authentication.csv')
        st.session_state['df'] = df
        num_cols = [feat for feat in df.columns if df[feat].dtype == 'float64']
        st.session_state['num_cols'] = num_cols
    else:
        data = st.file_uploader('Upload your data')
        sep = st.text_input('What separates your data?', ',')
        a = st.checkbox('Specify an index column', False)
        index = None
        if a:
            index = st.number_input('Which is your index column?', 0)
        if data is not None:
            df = pd.read_csv(data, sep=sep, index_col=index)
            st.dataframe(df.head())
            button = st.button('Confirm data')
            if button:
                st.session_state['df'] = df
                num_cols = [feat for feat in df.columns if df[feat].dtype == 'float64']
                st.session_state['num_cols'] = num_cols
                st.success('Dataframe saved! ')

       # pd.read_csv(data)
      #  sep = st.text_input('What separates your data?', ',')
       # if data is not None:
        #    index_column = st.selectbox('Select an index column', [None] + list(pd.read_csv(data, sep=sep).columns))
         #   pd.read_csv(filepath_or_buffer=data, sep=sep, index_col=index_column)
         #   if index_column != 'None':
           #     st.dataframe(pd.read_csv(data, sep=sep).head())
           #     df = pd.read_csv(data, sep=sep, index_col=index_column)
               # st.dataframe(df.head())
               # confirm_button = st.button('Confirm')
    #if data is not None and confirm_button:
      #  st.session_state['df'] = df
     #   num_cols = [feat for feat in df.columns if df[feat].dtype == 'float64']
     #   st.session_state['num_cols'] = num_cols

streamlit_layout()
