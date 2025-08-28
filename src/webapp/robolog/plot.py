"""Plot page for visualizing two topics against each other."""

import plotly.express as px
import streamlit as st

from settings import settings
from src.reader import factory

if not st.session_state.get("robolog_path") or not st.session_state.get("topic_reader"):
    st.info("Select a robolog file in the summary page first.")
    st.page_link("src/webapp/robolog/summary.py", label="Go to Summary", icon="👉")
    st.stop()


with st.container():
    st.write(f"### Robolog ID: {st.session_state.topic_reader.robolog_id}")
    st.caption(st.session_state.robolog_path)
    st.markdown("<br>", unsafe_allow_html=True)


with st.container():
    # First, let user select topics
    col1, col2 = st.columns(2)

    with col1:
        x_topic = st.selectbox(
            "Select X-axis topic",
            st.session_state.topic_reader.topics,
            key="x_topic"
        )

    with col2:
        y_topic = st.selectbox(
            "Select Y-axis topic",
            st.session_state.topic_reader.topics,
            key="y_topic"
        )

    st.markdown("<br>", unsafe_allow_html=True)


if not x_topic or not y_topic:
    st.warning("Please select both X and Y topics.")
    st.stop()


# Read sample data to get field information
with st.spinner("Loading topic structure...", show_time=True):
    # Read small sample to get schema
    x_sample_dataset = st.session_state.topic_reader.read([x_topic], peek=True)
    y_sample_dataset = st.session_state.topic_reader.read([y_topic], peek=True)

    x_sample_df = x_sample_dataset.to_pandas()
    y_sample_df = y_sample_dataset.to_pandas()

    # Get field names from the actual topic data structure (not column names)
    # The topic data is stored as dictionaries in the topic column
    x_sample_data = x_sample_df[x_topic].dropna().iloc[0] if not x_sample_df[x_topic].dropna().empty else {}
    y_sample_data = y_sample_df[y_topic].dropna().iloc[0] if not y_sample_df[y_topic].dropna().empty else {}
    
    x_fields = list(x_sample_data.keys()) if isinstance(x_sample_data, dict) else []
    y_fields = list(y_sample_data.keys()) if isinstance(y_sample_data, dict) else []


with st.container():
    # Now let user select specific fields
    col1, col2 = st.columns(2)

    with col1:
        x_field = st.selectbox(
            f"Select field from {x_topic}",
            x_fields,
            key="x_field"
        )

    with col2:
        y_field = st.selectbox(
            f"Select field from {y_topic}",
            y_fields,
            key="y_field"
        )

    st.markdown("<br>", unsafe_allow_html=True)


if not x_field or not y_field:
    st.warning("Please select both X and Y fields.")
    st.stop()


with st.spinner(f"Reading data for {x_topic} and {y_topic}...", show_time=True):
    topic_reader = factory.make_topic_message_reader(st.session_state.robolog_path)

    # Read both topics
    x_dataset = topic_reader.read([x_topic])
    y_dataset = topic_reader.read([y_topic])

    # Convert to pandas DataFrames
    x_df = x_dataset.to_pandas()
    y_df = y_dataset.to_pandas()


with st.container():
    if x_df.empty or y_df.empty:
        st.warning("No data found for selected topics.")
        st.stop()

    # Extract the selected fields from the structured topic data
    # The topic data is structured, so we need to access the field within the topic column
    x_data = x_df[[settings.TIMESTAMP_SECONDS_COLUMN_NAME, x_topic]].copy()
    y_data = y_df[[settings.TIMESTAMP_SECONDS_COLUMN_NAME, y_topic]].copy()

    # Extract the specific field values from the structured data
    # The data is stored as dictionaries, so we access the field as a dictionary key
    x_data["x_value"] = x_data[x_topic].apply(lambda x: x.get(x_field, None) if isinstance(x, dict) else None)
    y_data["y_value"] = y_data[y_topic].apply(lambda x: x.get(y_field, None) if isinstance(x, dict) else None)

    # Rename timestamp column for consistency
    x_data = x_data.rename(columns={settings.TIMESTAMP_SECONDS_COLUMN_NAME: "timestamp"})[["timestamp", "x_value"]]
    y_data = y_data.rename(columns={settings.TIMESTAMP_SECONDS_COLUMN_NAME: "timestamp"})[["timestamp", "y_value"]]

    # Merge on timestamp (outer join to handle different sampling rates)
    merged_data = x_data.merge(y_data, on="timestamp", how="outer").sort_values("timestamp")

    # Drop rows where either x or y is NaN
    plot_data = merged_data.dropna(subset=["x_value", "y_value"])

    if plot_data.empty:
        st.warning("No overlapping data found between selected fields.")
        st.stop()

    # Create scatter plot
    fig = px.scatter(
        plot_data,
        x="x_value",
        y="y_value",
        title=f"{y_topic}.{y_field} vs {x_topic}.{x_field}",
        labels={
            "x_value": f"{x_topic}.{x_field}",
            "y_value": f"{y_topic}.{y_field}"
        },
        height=600,
    )

    # Add line connecting points if data is time-ordered
    fig.add_trace(
        px.line(plot_data, x="x_value", y="y_value").data[0]
    )

    # Update layout for better visualization
    fig.update_layout(
        xaxis=dict(title=dict(text=f"{x_topic}.{x_field}")),
        yaxis=dict(title=dict(text=f"{y_topic}.{y_field}")),
        showlegend=False
    )

    # Enable autoscaling (plotly default)
    fig.update_xaxes(autorange=True)
    fig.update_yaxes(autorange=True)

    st.plotly_chart(fig, use_container_width=True)

    # Display data info
    st.markdown("**Data Information:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Data Points", len(plot_data))
    with col2:
        time_range = plot_data["timestamp"].max() - plot_data["timestamp"].min()
        st.metric("Time Range (s)", f"{time_range:.2f}")
    with col3:
        st.metric("X Field", f"{x_topic}.{x_field}")

    # Future timeline container (prepared for timeline scrubber)
    timeline_container = st.container()
    with timeline_container:
        st.markdown("---")
        # Placeholder for future timeline component
        st.write("Timeline component will be added here")
