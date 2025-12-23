"""
Performance optimization utilities for Streamlit app.

Includes cache management and performance monitoring.
"""

import streamlit as st
import time
from typing import Callable, Any


def clear_cache():
    """Clear Streamlit cache."""
    st.cache_data.clear()
    st.success("✅ Cache cleared successfully!")


def show_cache_status():
    """Display cache status information."""
    st.info("💡 Cache helps improve performance by storing calculation results. Clear cache if you need fresh calculations.")


def performance_monitor(func: Callable) -> Callable:
    """
    Decorator to monitor function performance.

    Usage:
        @performance_monitor
        def my_function():
            ...
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time

        if 'performance_log' not in st.session_state:
            st.session_state.performance_log = []

        st.session_state.performance_log.append({
            'function': func.__name__,
            'elapsed': elapsed,
            'timestamp': time.time()
        })

        return result
    return wrapper


def show_performance_info():
    """Display performance information."""
    if 'performance_log' in st.session_state and st.session_state.performance_log:
        latest = st.session_state.performance_log[-1]
        st.caption(f"⏱️ Last calculation took {latest['elapsed']:.2f} seconds")

        if len(st.session_state.performance_log) > 1:
            avg_time = sum(log['elapsed'] for log in st.session_state.performance_log[-5:]) / min(5, len(st.session_state.performance_log))
            st.caption(f"📊 Average (last 5): {avg_time:.2f} seconds")


def add_cache_management_ui():
    """Add cache management UI to sidebar or page."""
    with st.expander("⚡ Performance & Cache", expanded=False):
        st.markdown("**Cache Management**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Cache", help="Clear cached calculation results"):
                clear_cache()
                st.rerun()

        with col2:
            if st.button("📊 Show Cache Info"):
                show_cache_status()

        show_performance_info()

        st.markdown("**Performance Tips**")
        st.markdown("""
        - Cache stores calculation results for faster access
        - Calculations are cached based on input parameters
        - Clear cache if you need fresh calculations
        - Use the Calculate button to trigger new calculations
        """)
