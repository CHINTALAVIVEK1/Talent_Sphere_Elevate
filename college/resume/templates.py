# templates.py - Theme and UI configuration for Resume Studio

DEFAULT_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Machine Learning"
]

# CSS styles to give the Resume Studio a premium, rich aesthetic
CUSTOM_CSS = """
<style>
/* Gradient borders & card structures */
.resume-card {
    border-radius: 12px;
    padding: 24px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
}

.dark-mode-card {
    padding: 20px;
    border-radius: 10px;
    background-color: #1e293b;
    border-left: 5px solid #3b82f6;
    margin-bottom: 15px;
}

/* Metric / ATS styling */
.ats-score-container {
    background: radial-gradient(circle, #1e3a8a 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    border: 2px solid #3b82f6;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
    margin-bottom: 25px;
}

.ats-score-title {
    font-size: 20px;
    color: #93c5fd;
    font-weight: 600;
    margin-bottom: 5px;
}

.ats-score-value {
    font-size: 64px;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 10px rgba(59, 130, 246, 0.8);
    margin: 10px 0;
}

.ats-score-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 14px;
    text-transform: uppercase;
}

.badge-excellent { background-color: #10b981; color: white; }
.badge-good { background-color: #f59e0b; color: white; }
.badge-needs-improvement { background-color: #ef4444; color: white; }

/* Micro-animations and premium UI lists */
ul.suggestion-list {
    list-style-type: none;
    padding-left: 0;
}
ul.suggestion-list li {
    position: relative;
    padding-left: 24px;
    margin-bottom: 10px;
    font-size: 15px;
}
ul.suggestion-list li::before {
    content: "💡";
    position: absolute;
    left: 0;
    top: 1px;
}

ul.strength-list {
    list-style-type: none;
    padding-left: 0;
}
ul.strength-list li {
    position: relative;
    padding-left: 24px;
    margin-bottom: 10px;
    font-size: 15px;
}
ul.strength-list li::before {
    content: "✅";
    position: absolute;
    left: 0;
    top: 1px;
}

ul.weakness-list {
    list-style-type: none;
    padding-left: 0;
}
ul.weakness-list li {
    position: relative;
    padding-left: 24px;
    margin-bottom: 10px;
    font-size: 15px;
}
ul.weakness-list li::before {
    content: "❌";
    position: absolute;
    left: 0;
    top: 1px;
}
</style>
"""
