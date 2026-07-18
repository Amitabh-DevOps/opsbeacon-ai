from datetime import datetime, timezone
from typing import Any
from jinja2 import Template
from src.logger import get_logger

logger = get_logger(__name__)

EMAIL_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpsBeacon AI Daily Briefing</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f1f5f9;
            color: #1e293b;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }
        .container {
            max-width: 680px;
            margin: 0 auto;
            padding: 24px 16px;
        }
        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
            border-radius: 16px;
            padding: 32px 24px;
            text-align: center;
            color: #ffffff;
            margin-bottom: 24px;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.15);
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        .header p {
            margin: 8px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }
        .meta-info {
            font-size: 12px;
            background-color: rgba(255, 255, 255, 0.2);
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            margin-top: 12px;
            font-weight: 500;
        }
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
            margin: 32px 0 16px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }
        .card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .badge {
            font-size: 11px;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-aws { background-color: #ffedd5; color: #c2410c; }
        .badge-k8s { background-color: #e0f2fe; color: #0369a1; }
        .badge-cncf { background-color: #dcfce7; color: #15803d; }
        .badge-docker { background-color: #e0f2fe; color: #1d4ed8; }
        .badge-generic { background-color: #f1f5f9; color: #475569; }
        
        .card-title {
            margin: 0 0 12px 0;
            font-size: 18px;
            font-weight: 700;
        }
        .card-title a {
            color: #1e1b4b;
            text-decoration: none;
        }
        .card-title a:hover {
            color: #4f46e5;
            text-decoration: underline;
        }
        .card-body {
            font-size: 14.5px;
            line-height: 1.6;
            color: #334155;
            margin-bottom: 16px;
        }
        .callout-box {
            background-color: #f8fafc;
            border-left: 4px solid #4f46e5;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-top: 12px;
        }
        .callout-box-title {
            font-size: 12px;
            font-weight: 700;
            color: #4f46e5;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .callout-box-content {
            font-size: 13.5px;
            color: #475569;
            line-height: 1.5;
        }
        .callout-impact {
            border-left-color: #06b6d4;
        }
        .callout-impact .callout-box-title {
            color: #0891b2;
        }
        .learning-section {
            background-color: #eef2ff;
            border: 1px dashed #c7d2fe;
            border-radius: 12px;
            padding: 24px;
            margin-top: 32px;
        }
        .learning-header {
            font-size: 18px;
            font-weight: 800;
            color: #3730a3;
            margin: 0 0 16px 0;
            display: flex;
            align-items: center;
        }
        .learning-item {
            margin-bottom: 20px;
        }
        .learning-item:last-child {
            margin-bottom: 0;
        }
        .learning-label {
            font-size: 12px;
            font-weight: 700;
            color: #4f46e5;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .learning-content {
            font-size: 14px;
            line-height: 1.6;
            color: #1e1b4b;
        }
        .footer {
            text-align: center;
            padding: 32px 24px 8px 24px;
            font-size: 12px;
            color: #94a3b8;
        }
        .footer a {
            color: #64748b;
            text-decoration: underline;
        }
        .no-updates {
            text-align: center;
            padding: 40px 20px;
            background-color: #ffffff;
            border-radius: 12px;
            border: 1px dashed #cbd5e1;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>OpsBeacon AI</h1>
            <p>Your Daily DevOps Intelligence Summary</p>
            <div class="meta-info">Triggered: {{ date }} UTC | {{ updates_count }} Updates</div>
        </div>

        <!-- Updates Section -->
        <div class="section-title">Today's Cloud & DevOps Updates</div>
        
        {% if updates %}
            {% for item in updates %}
            <div class="card">
                <div class="card-header">
                    <span class="badge {{ get_badge_class(item.source) }}">{{ item.source }}</span>
                </div>
                <h2 class="card-title">
                    {% if item.url and item.url != 'https://github.com/opsbeacon-ai' %}
                        <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                    {% else %}
                        {{ item.title }}
                    {% endif %}
                </h2>
                <div class="card-body">
                    {{ item.summary }}
                </div>
                
                <div class="callout-box">
                    <div class="callout-box-title">Why It Matters</div>
                    <div class="callout-box-content">{{ item.why_it_matters }}</div>
                </div>
                
                <div class="callout-box callout-impact">
                    <div class="callout-box-title">DevOps Impact</div>
                    <div class="callout-box-content">{{ item.devops_impact }}</div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="no-updates">
                <h3>System Heartbeat</h3>
                <p>No major updates were released by the tracked feeds in the last 24 hours. The automated agent is running unattended and monitoring sources continuously.</p>
            </div>
        {% endif %}

        <!-- Daily Learning & Brain Boost -->
        <div class="learning-section">
            <h2 class="learning-header">🧠 OpsBeacon AI Daily Brain Boost</h2>
            
            <div class="learning-item">
                <div class="learning-label">Daily DevOps Interview Question</div>
                <div class="learning-content"><strong>Q:</strong> {{ learning.interview_question }}</div>
            </div>
            
            <div class="learning-item">
                <div class="learning-label">Hands-On Practice Challenge</div>
                <div class="learning-content">{{ learning.hands_on_challenge }}</div>
            </div>
            
            <div class="learning-item">
                <div class="learning-label">Recommended Topic for Deeper Study</div>
                <div class="learning-content">{{ learning.recommendation }}</div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>This briefing was compiled autonomously by <strong>OpsBeacon AI</strong>, triggered by AWS EventBridge Scheduler.</p>
            <p><a href="https://github.com/opsbeacon-ai/opsbeacon-ai">OpsBeacon AI GitHub Repository</a> | <a href="https://aws.amazon.com/">AWS Builder Center</a></p>
            <p>&copy; 2026 OpsBeacon AI. Always-On DevOps Intelligence Agent.</p>
        </div>
    </div>
</body>
</html>
"""


def get_badge_class(source: str) -> str:
    """
    Returns CSS badge styling class depending on the feed source name.
    """
    s = source.lower()
    if "aws" in s:
        return "badge-aws"
    elif "kubernetes" in s or "k8s" in s:
        return "badge-k8s"
    elif "cncf" in s:
        return "badge-cncf"
    elif "docker" in s:
        return "badge-docker"
    return "badge-generic"


def generate_email_html(digest: dict[str, Any]) -> str:
    """
    Compiles Bedrock intelligence digest into a beautiful responsive HTML email string.

    Args:
        digest: The parsed dictionary containing 'updates' (list) and 'learning' (dict).

    Returns:
        The generated HTML content string.
    """
    logger.info("Generating HTML email from digest data")

    # Standardize time presentation
    now_utc_str = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M")

    template = Template(EMAIL_HTML_TEMPLATE)

    # Inject badge helper into context
    html_content = template.render(
        date=now_utc_str,
        updates=digest.get("updates", []),
        updates_count=len(digest.get("updates", [])),
        learning=digest.get("learning", {}),
        get_badge_class=get_badge_class,
    )

    logger.info("HTML email compilation complete")
    return html_content
