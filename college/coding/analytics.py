import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime

def generate_difficulty_distribution_chart(easy, medium, hard):
    """
    Generates a Plotly pie chart showing solved problem difficulty distribution.
    """
    labels = ['Easy', 'Medium', 'Hard']
    values = [easy, medium, hard]
    
    # Matching custom dark-theme colors
    colors = ['#10b981', '#f59e0b', '#ef4444'] 
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker=dict(colors=colors, line=dict(color='#0f172a', width=2)),
        textinfo='value+percent',
        hoverinfo='label+value'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family='Inter, sans-serif'),
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        height=260
    )
    return fig

def generate_weekly_activity_chart(daily_analytics):
    """
    Generates a Plotly bar chart showing problems solved over the last 7 days.
    """
    today = datetime.date.today()
    last_7_days = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]
    dates_str = [d.isoformat() for d in last_7_days]
    display_names = [d.strftime('%a') for d in last_7_days]
    
    db_map = {item["date"]: item["problems_solved"] for item in daily_analytics}
    solved_counts = [db_map.get(d, 0) for d in dates_str]
    
    df = pd.DataFrame({
        "Day": display_names,
        "Problems Solved": solved_counts
    })
    
    fig = px.bar(
        df,
        x="Day",
        y="Problems Solved",
        color_discrete_sequence=['#3b82f6']
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family='Inter, sans-serif'),
        margin=dict(t=30, b=20, l=40, r=20),
        xaxis=dict(showgrid=False, color='#94a3b8'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#94a3b8', tickformat=',d'),
        height=260
    )
    return fig

def generate_topic_mastery_chart(topic_stats):
    """
    Generates a horizontal bar chart showing solved counts by topic area.
    """
    topics = list(topic_stats.keys())
    solved = [stats["solved"] for stats in topic_stats.values()]
    total = [stats["total"] for stats in topic_stats.values()]
    
    mastery_pct = []
    for s, t in zip(solved, total):
        pct = int((s / t) * 100) if t > 0 else 0
        mastery_pct.append(pct)
        
    df = pd.DataFrame({
        "Topic": topics,
        "Mastery %": mastery_pct,
        "Label": [f"{s}/{t} Solved" for s, t in zip(solved, total)]
    }).sort_values("Mastery %", ascending=True)
    
    fig = px.bar(
        df,
        y="Topic",
        x="Mastery %",
        orientation="h",
        text="Label",
        color="Mastery %",
        color_continuous_scale=['#1e3b8a', '#3b82f6', '#60a5fa']
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family='Inter, sans-serif'),
        margin=dict(t=20, b=20, l=80, r=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#94a3b8', range=[0, 100]),
        yaxis=dict(showgrid=False, color='#94a3b8'),
        coloraxis_showscale=False,
        height=260
    )
    fig.update_traces(textposition='inside', insidetextanchor='end')
    return fig

def generate_readiness_gauge(score, title, color="#3b82f6"):
    """
    Generates a single circular gauge chart representing a readiness score.
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': title, 'font': {'size': 13, 'color': '#94a3b8', 'family': 'Inter, sans-serif'}},
        number = {'font': {'color': '#f8fafc', 'size': 26, 'family': 'Inter, sans-serif'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': color},
            'bgcolor': "rgba(30, 41, 59, 0.5)",
            'borderwidth': 2,
            'bordercolor': "#475569",
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=10, l=30, r=30),
        height=180
    )
    return fig
