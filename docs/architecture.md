# OpsBeacon AI - Architecture Documentation

This document outlines the architecture, data flow, and design patterns utilized in **OpsBeacon AI: An Always-On AI DevOps Intelligence Agent**.

OpsBeacon AI operates as a completely serverless, automated agent on AWS, utilizing AWS Free Tier services where possible.

## System Architecture Diagram

Below is the high-level system architecture illustrating how the EventBridge Scheduler triggers the orchestration Lambda, which interacts with RSS feeds, Bedrock Nova Lite, and SES.

```mermaid
graph TD
    A[EventBridge Scheduler] -->|1. Scheduled Trigger 8:00 AM UTC| B[OpsBeacon AI Lambda Function]
    B -->|2. Scrape Feeds| C[RSS Feeds]
    C -->|3. Feed Entries last 24h| B
    B -->|4. Request Synthesis & Learning| D[Amazon Bedrock Nova Lite]
    D -->|5. Structured JSON Response| B
    B -->|6. Compile HTML Email| E[HTML Generator]
    B -->|7. Send Email Request| F[Amazon SES]
    F -->|8. Deliver daily briefing| G[DevOps Engineer Inbox]
    
    subgraph AWS Cloud
        B
        D
        F
        A
    end
    
    subgraph External Sources
        C
    end
    
    subgraph User
        G
    end

    style B fill:#4f46e5,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#06b6d4,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#0284c7,stroke:#fff,stroke-width:2px,color:#fff
    style A fill:#f59e0b,stroke:#fff,stroke-width:2px,color:#fff
```

## System Sequence Diagram

This sequence diagram depicts the chronological flow of execution when the EventBridge Scheduler fires.

```mermaid
sequenceDiagram
    autonumber
    actor User as DevOps Engineer
    participant EB as EventBridge Scheduler
    participant L as Lambda Function
    participant RSS as RSS Feeds (AWS, K8s, CNCF, Docker)
    participant B as Amazon Bedrock (Nova Lite)
    participant SES as Amazon SES

    EB->>L: Trigger Lambda execution (cron 0 8 * * ? *)
    activate L
    L->>L: Load Configurations (Env variables)
    
    rect rgb(240, 240, 255)
        note right of L: Scrape RSS Feeds phase
        L->>RSS: Request RSS XML Feed
        RSS-->>L: Return Feed XML content
        L->>L: Filter entries published in last 24 hours
    end

    rect rgb(240, 255, 240)
        note right of L: AI Summarization & Content Gen phase
        L->>B: Invoke Converse API with RSS Updates list & instruction prompt
        B-->>L: Return structured JSON (Updates, Interview Q, Challenge, Recommendation)
    end

    rect rgb(255, 240, 240)
        note right of L: Email Generation & Sending phase
        L->>L: Compile HTML newsletter from JSON digest using Jinja2
        L->>SES: Request email dispatch (Verified Sender to Recipient)
        SES-->>L: Send Confirmation (MessageId)
    end
    
    SES->>User: Deliver HTML newsletter in Inbox
    L-->>EB: Return execution success response (200 OK)
    deactivate L
```

## Component Breakdown

1. **Amazon EventBridge Scheduler**: Triggered every morning at 8:00 AM UTC. It leverages the modern `AWS::Scheduler::Schedule` resource, invoking the Lambda target.
2. **AWS Lambda**: The orchestrator written in Python 3.12. It packages code, fetches feeds using `feedparser`, interacts with Bedrock Runtime via `boto3`, generates templates with `Jinja2`, and submits to SES.
3. **Amazon Bedrock (Nova Lite)**: Synthesizes the filtered updates. We use Nova Lite (`amazon.nova-lite-v1:0`) because it is fast, cost-effective, and highly capable of following structured output instructions (JSON schemas).
4. **HTML Generator**: Compiles a professional newsletter. We use Jinja2 to render cards, badges, and callouts matching corporate DevOps brand aesthetics.
5. **Amazon SES**: Transmits the message over SMTP/API using TLS. It restricts traffic to verified domain identities to enforce security.
6. **Amazon CloudWatch Logs**: Captures structured JSON log streams printed by our custom logger, facilitating auditing, metrics compilation, and troubleshooting.

## Diagram Assets Directory
For drawing applications (e.g., Draw.io):
- **Draw.io editable source file**: Deployed under [docs/assets/architecture.drawio](file:///d:/AWS-weekend-challenge/docs/assets/architecture.drawio) (Instructions: Import this XML script inside [draw.io](https://app.diagrams.net/) to edit the diagrams).
- **SVG export**: Deployed under [docs/assets/architecture.svg](file:///d:/AWS-weekend-challenge/docs/assets/architecture.svg).
- **PNG export**: Deployed under [docs/assets/architecture.png](file:///d:/AWS-weekend-challenge/docs/assets/architecture.png).

<!-- IMAGE_PLACEHOLDER: Architecture Diagram -->
*Note: Capture a screenshot of the system architecture diagram rendered above or from Draw.io to display in the final project documentation.*
