import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
import plotly.figure_factory as ff
import streamlit as st
import numpy as np
import plotly.graph_objects as go


def create_dist_plot(df, feature: str, colorhash: str, bin_size, curve_type: str, title: str, show_curve=True,
                     show_hist=True, show_rug=True, histnorm='probability density'):
    """
    Function that create a distribution plot with/without:
    :param df: dataframe to get data from
    :param feature: feature in question
    :param colorhash: color hash
    :param bin_size: bin size of the histogram
    :param curve_type: whether it shows a kde or normal distribution
    :param title: title of the plot
    :param show_curve: Whether to show the curve
    :param show_hist: whether to show the histogram
    :param show_rug: whether to show the rug
    :param histnorm:
    :return:
    """
    my_fig = ff.create_distplot(
        [df.loc[:, feature]],
        group_labels=[feature],
        show_curve=show_curve,
        colors=[colorhash],
        bin_size=bin_size,
        curve_type=curve_type,
        show_hist=show_hist,
        show_rug=show_rug,
        histnorm=histnorm)
    my_fig.update_layout(title_text=title,
                         title_x=0.16,
                         xaxis_title="Values that your feature can take",
                         yaxis_title="Their density/frequency",
                         width=600,
                         height=600,
                         legend=dict(
                             yanchor="top",
                             y=1.1,
                             xanchor="left",
                             x=0.01),
                         template='plotly_white',
                         plot_bgcolor="rgb(255,255,255)",
                         font=dict(family="Courier New, monospace",
                                   size=14))

    return my_fig


# build our functions that will perform the scaling
def MinMaxScaling(df, num_cols):
    df_norm = df.copy()
    for i in num_cols:
        # fit on training data column
        scale = MinMaxScaler().fit(df[[i]])

        # transform the training data column
        df_norm[i] = scale.transform(df[[i]])
    return df_norm


def MaxAbsScaling(df, num_cols):
    df_maxabs = df.copy()
    for i in num_cols:
        # fit on training data column
        scale = MaxAbsScaler().fit(df[[i]])

        # transform the training data column
        df_maxabs[i] = scale.transform(df[[i]])
    return df_maxabs


def RobsustScaling(df):
    df_rob = df.copy()
    for i in list(df_rob.columns):
        # fit on training data column
        scale = RobustScaler().fit(df[[i]])

        # transform the training data column
        df_rob[i] = scale.transform(df[[i]])
    return df_rob


def StandardScaling(df, num_cols):
    df_stan = df.copy()
    for i in num_cols:
        scale = StandardScaler().fit(df[[i]])
        df_stan[i] = scale.transform(df[[i]])
    return df_stan


def Standardscaling_feature(df, feature):
    df_stand = df.copy()
    scale = StandardScaler().fit(df[[feature]])
    df_stand[[feature]] = scale.transform(df[[feature]])
    return df_stand


def PowerTransformer1(df, num_cols):
    from sklearn.preprocessing import PowerTransformer
    df_power = df.copy()
    for i in num_cols:
        scale = PowerTransformer().fit(df[[i]])

        df_power[i] = scale.transform(df[[i]])
    return df_power


def PowerTransformer(df, feature, order):
    df_power = df.copy()
    df_power[feature] = np.power(df_power[feature], order)
    return df_power


def normalization_board(df, num_cols):
    # -------------------- generate scaled dataframes
    df_minmax = MinMaxScaling(df, num_cols)
    df_maxabs = MaxAbsScaling(df, num_cols)
    df_rob = RobsustScaling(df)
    return df_minmax, df_maxabs, df_rob


def upload_data(sep, file_uploader):
    df = pd.read_csv(file_uploader, sep=sep)
    return df


def encoded_data_checker(df):
    """
    Check if the data contains categorical (string) values.
    It should return a boolean
    True = There is categorical values / False = No string values are found
    :param df: dataframe in question
    :return: Bool
    """
    categorical_columns = []
    for col in list(df.columns):
        if df[col].dtype == 'object':
            categorical_columns.append(col)
    if len(categorical_columns) == 0:
        return True
    else:
        return False


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def log_transform(df, feature, log_type):
    df_new = df.copy()
    if log_type == 'log':
        df_new[feature] = np.log(df_new[feature])
        return df_new
    elif log_type == 'log2':
        df_new[feature] = np.log2(df_new[feature])
        return df_new
    elif log_type == 'log10':
        df_new[feature] = np.log10(df_new[feature])
        return df_new


def clip_feature(df, feature, upper, lower):
    df_clipped = df.copy()
    df_clipped[feature] = df_clipped[feature].clip(lower, upper)
    return df_clipped


def draw_box(df, feature_list, title, showle=True):
    color_palette = ['#A7D2CB', '#F2D388', '#FAAB78', '#C98474', '#874C62', '#9A1663']
    fig = go.Figure()
    for yd, cls in zip(feature_list, color_palette):
        fig.add_trace(
            go.Box(y=df[yd], name=yd, boxmean=True, marker=dict(color=cls))
        )
    fig.update_layout(title_text=title,
                      title_x=0.16,
                      yaxis_title="features' values",
                      width=600,
                      height=600,
                      showlegend=showle,
                      legend=dict(
                          yanchor="auto",
                          y=1.1,
                          xanchor="left",
                          x=1),
                      template='plotly_white',
                      plot_bgcolor="rgb(255,255,255)",
                      font=dict(family="Courier New, monospace",
                                size=14))

    return fig
