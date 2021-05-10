import numpy as np
from scipy.stats import norm, multivariate_normal
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from lh_sampling.sampler import lhs


def lhs_example_plot(seed=None):
    mean = [0.5, -0.2]
    cov = [[2.0, 0.5], [0.5, 0.5]]
    rv = multivariate_normal(mean, cov)
    U = np.linalg.cholesky(cov)

    nsamples = list(range(10, 1000))
    mc_mean = []
    mc_cov = np.zeros((len(nsamples), 2, 2))
    lh_mean = []
    lh_cov = np.zeros((len(nsamples), 2, 2))
    for i, s in enumerate(nsamples):
        u, u_lh = lhs(2, s, seed=seed, return_original=True)
        samples_x = norm.ppf(u[:, 0], loc=0, scale=1)
        samples_y = norm.ppf(u[:, 1], loc=0, scale=1)
        samples = np.vstack((samples_x, samples_y))
        t_samples = np.dot(U, samples)
        t_samples += np.array(mean)[:, np.newaxis]
        mc_mean.append(t_samples[0].mean())
        mc_cov[i, :] = np.cov(t_samples)
        
        lh_samples_x = norm.ppf(u_lh[:, 0], loc=0, scale=1)
        lh_samples_y = norm.ppf(u_lh[:, 1], loc=0, scale=1)
        lh_samples = np.vstack((lh_samples_x, lh_samples_y))
        t_lh_samples = np.dot(U, lh_samples)
        t_lh_samples += np.array(mean)[:, np.newaxis]
        lh_mean.append(t_lh_samples[0].mean())
        lh_cov[i, :] = np.cov(t_lh_samples)

    fig = make_subplots(rows=3, cols=2, vertical_spacing=0.1,
                        subplot_titles=['Original', '',
                                        'Latin Hypercube', '',
                                        'Monte Carlo', ''])
    fig.add_trace(go.Scatter(x=nsamples, y=lh_mean, mode='lines', name='Latin Hypercube',
                             line=dict(color='red')), row=1, col=2)
    fig.add_trace(go.Scatter(x=nsamples, y=mc_mean, mode='lines', name='Monte Carlo',
                             line=dict(color='blue')), row=1, col=2)
    
    fig.add_trace(go.Scatter(x=nsamples, y=lh_cov[:, 0, 0] , mode='lines',
                             line=dict(color='red'), showlegend=False), row=2, col=2)
    fig.add_trace(go.Scatter(x=nsamples, y=mc_cov[:, 0, 0], mode='lines',
                             line=dict(color='blue'), showlegend=False), row=2, col=2)
    
    fig.add_trace(go.Scatter(x=nsamples, y=lh_cov[:, 1, 0] , mode='lines',
                             line=dict(color='red'), showlegend=False), row=3, col=2)
    fig.add_trace(go.Scatter(x=nsamples, y=mc_cov[:, 1, 0], mode='lines',
                             line=dict(color='blue'), showlegend=False), row=3, col=2)
    
    x, y = np.mgrid[-3:3.5:.01, -2.5:2:.01]
    pos = np.dstack((x, y))
    fig.add_trace(go.Contour(z=rv.pdf(pos).T,
                             x=np.unique(x), # horizontal axis
                             y=np.unique(y),
                             coloraxis='coloraxis',
                             showscale=False), row=1, col=1)
    u, u_lh = lhs(2, 20, seed=seed, return_original=True)
    lh_samples_x = norm.ppf(u_lh[:, 0], loc=0, scale=1)
    lh_samples_y = norm.ppf(u_lh[:, 1], loc=0, scale=1)
    lh_samples = np.vstack((lh_samples_x, lh_samples_y))
    t_lh_samples = np.dot(U, lh_samples)
    t_lh_samples += np.array(mean)[:, np.newaxis]
    
    samples_x = norm.ppf(u[:, 0], loc=0, scale=1)
    samples_y = norm.ppf(u[:, 1], loc=0, scale=1)
    samples = np.vstack((samples_x, samples_y))
    t_u_samples = np.dot(U, samples)
    t_u_samples += np.array(mean)[:, np.newaxis]
    fig.add_trace(go.Histogram2dContour(x=t_lh_samples[0],
                                        y=t_lh_samples[1],
                                        coloraxis='coloraxis',
                                        histnorm='probability density',
                                        showscale=False,
                                        contours=dict(coloring='lines')), row=2, col=1)
    fig.add_trace(go.Histogram2dContour(x=t_u_samples[0],
                                        y=t_u_samples[1],
                                        coloraxis='coloraxis',
                                        histnorm='probability density',
                                        showscale=False,
                                        contours=dict(coloring='lines')), row=3, col=1)
    fig.add_annotation(x=-2, y=1.5, text="(a)", font_color='white',
                       font_size=10, showarrow=False, row=1, col=1)
    fig.add_annotation(x=-2, y=1.5, text="(b)", font_color='black',
                       font_size=10, showarrow=False, row=2, col=1)
    fig.add_annotation(x=-2, y=1.5, text="(c)", font_color='black',
                       font_size=10, showarrow=False, row=3, col=1)
    fig.add_annotation(x=900, y=1.5, text="(d)", font_color='black',
                       font_size=10, showarrow=False, row=1, col=2)
    fig.add_annotation(x=900, y=3, text="(e)", font_color='black',
                       font_size=10, showarrow=False, row=2, col=2)
    fig.add_annotation(x=900, y=1, text="(f)", font_color='black',
                       font_size=10, showarrow=False, row=3, col=2)
    fig.update_xaxes(title_text="Number of samples", row=3, col=2)
    fig.update_yaxes(title_text="Mean", side='right', row=1, col=2)
    fig.update_yaxes(title_text="Covariance [0, 0]", side='right', row=2, col=2)
    fig.update_yaxes(title_text="Covariance [1, 0]", side='right', row=3, col=2)
    fig.update_yaxes(range=(-2.5, 2.), row=1, col=1)
    fig.update_yaxes(range=(-2.5, 2.), row=2, col=1)
    fig.update_yaxes(range=(-2.5, 2.), row=3, col=1)
    fig.update_xaxes(range=(-3, 3.5), row=1, col=1)
    fig.update_xaxes(range=(-3, 3.5), row=2, col=1)
    fig.update_xaxes(range=(-3, 3.5), row=3, col=1)
    fig.update_layout(coloraxis=dict(colorscale='Inferno',
                                     colorbar=dict(lenmode='fraction',
                                                   len=0.4, yanchor='top',
                                                   y=0.4)))
    fig.update_layout(height=800, width=800)
    return fig

def plot_lhs(nsamples=14, figname=None):
    ro, rs = lhs(2, nsamples, return_original=True,
                 seed=0)
    fig = plt.figure(figsize=(5,5))
    cuts = np.linspace(0, 1, nsamples+1)
    ax = fig.add_subplot(111)
    ax.plot(rs[:, 0], rs[:, 1], markersize=20, marker='+', linestyle='',
            color='black')
    ax.plot(ro[:, 0], rs[:, 1], markersize=10, marker='o', linestyle='',
            color='green', alpha=0.5)
    for c in cuts:
        ax.hlines(c, 0, 1)
        ax.vlines(c, 0, 1)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.xticks([])
    plt.yticks([])
    if figname is not None:
        fig.savefig(figname, bbox_inches='tight', dpi=300)
