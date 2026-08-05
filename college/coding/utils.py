# utils.py - Coding Hub Layout and Theme configuration

CODING_CUSTOM_CSS = """
<style>
/* Developer-grade dashboard card layouts */
.metric-card {
    border-radius: 8px;
    padding: 20px;
    background-color: #1e293b;
    border: 1px solid #334155;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    margin-bottom: 15px;
}

.metric-card-title {
    font-size: 13px;
    color: #94a3b8;
    font-weight: 600;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-card-value {
    font-size: 26px;
    font-weight: 700;
    color: #f8fafc;
}

/* Badge indicators */
.badge-easy {
    background-color: rgba(34, 197, 94, 0.1);
    color: #4ade80;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 11px;
    border: 1px solid rgba(34, 197, 94, 0.2);
}

.badge-medium {
    background-color: rgba(234, 179, 8, 0.1);
    color: #facc15;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 11px;
    border: 1px solid rgba(234, 179, 8, 0.2);
}

.badge-hard {
    background-color: rgba(239, 68, 68, 0.1);
    color: #f87171;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 11px;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.badge-solved {
    background-color: rgba(34, 197, 94, 0.15);
    color: #22c55e;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
}

.badge-attempted {
    background-color: rgba(234, 179, 8, 0.15);
    color: #eab308;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
}

.badge-pending {
    background-color: rgba(148, 163, 184, 0.15);
    color: #94a3b8;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
}

/* Stepper items */
.stepper-item-completed {
    background-color: #0f172a;
    border-left: 4px solid #10b981;
    padding: 14px;
    border-radius: 6px;
    margin-bottom: 8px;
}

.stepper-item-unlocked {
    background-color: #1e293b;
    border-left: 4px solid #3b82f6;
    padding: 14px;
    border-radius: 6px;
    margin-bottom: 8px;
}

.stepper-item-locked {
    background-color: #0f172a;
    border-left: 4px solid #475569;
    padding: 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    opacity: 0.5;
}

/* Chat bubble styling */
.chat-bubble-user {
    background-color: #334155;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    border-left: 3px solid #3b82f6;
    color: #f1f5f9;
}

.chat-bubble-assistant {
    background-color: #1e293b;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    border-left: 3px solid #10b981;
    color: #f1f5f9;
}

/* Quick start prompts styling */
.quick-prompt-card {
    background-color: #0f172a;
    border: 1px solid #334155;
    padding: 10px;
    border-radius: 6px;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s;
}

.quick-prompt-card:hover {
    border-color: #3b82f6;
    background-color: #1e293b;
}

/* Custom list layout */
ul.clean-list {
    list-style-type: none;
    padding-left: 0;
}
ul.clean-list li {
    position: relative;
    padding-left: 20px;
    margin-bottom: 8px;
    font-size: 14px;
}
ul.clean-list li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #3b82f6;
    font-weight: bold;
}
</style>
"""

def format_minutes_to_hours(minutes):
    """
    Formats minute durations to a reader-friendly hours/minutes string.
    """
    hours = minutes // 60
    rem_min = minutes % 60
    if hours > 0:
        return f"{hours}h {rem_min}m"
    return f"{rem_min}m"
