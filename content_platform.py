# Platform page copy (English only). Sources: PRD §5.2, §9 (NFR-1..9), §11 and the architecture diagram;
# DECISIONS D2, D7, D13. Describes the platform's design; the model provider is deliberately not named (D13).

PLATFORM = {
    "meta_title": "Platform | obscur4",
    "hero_h": "The platform behind every ==engagement==.",
    "hero_sub": "One governed system is designed to run both services, from request to report. This is how it fits together and where the boundaries sit.",

    "stack_h": "Seven layers, one direction of travel",
    "stack_intro": "A request moves down through the same seven layers every time. Nothing reaches a test environment without passing the authorization layer first.",
    "layers": [
        ("Engagement interface",
         "Requests arrive through a web console, the command line or chat. Nothing runs from here directly."),
        ("Authorization and scope control",
         "Every action is checked against a written authorization: scope, time-box and target allowlist. Out-of-scope requests are refused with a reason."),
        ("Orchestration core",
         "A planner breaks the work into steps, picks the model lane and tool for each, and records every run in a ledger."),
        ("Execution harnesses",
         "Isolated workers carry out the steps: they write probes, run commands and call tools, each with its own credentials."),
        ("Assessment tooling",
         "Mobile static and runtime analysis, code and dependency scanning, web testing and passive reconnaissance."),
        ("Isolated test environments",
         "Disposable, network-segmented environments: ephemeral containers, an emulated device farm, loopback labs and client-authorized staging."),
        ("Evidence, analysis and reporting",
         "Raw artifacts are stored with hashes, findings are written from them, and reports are sanitized on export."),
    ],
    "feedback": "Lessons from each engagement return to the knowledge layer, so the next one starts from the last.",

    "lanes_h": "Model lanes",
    "lanes_intro": "Work is routed by difficulty, so depth is paid for only where it is needed.",
    "lanes": [
        ("Frontier", "Hard reasoning and judgment.",
         ["Decode an obfuscated record table", "Plan a controlled comparison", "Review a finding before it ships"]),
        ("Cost-efficient", "Routine, well-defined steps.",
         ["Extract fields from launch logs", "Assemble the report", "Check a run against its runbook"]),
        ("Self-hosted", "Work that should not leave our environment.",
         ["Process client artifacts that must stay with us"]),
    ],

    "provider_h": "Built on an enterprise model platform",
    "provider_intro": "Model access is designed around a leading frontier-model provider's enterprise platform and console, used as infrastructure rather than as the product.",
    "provider": [
        ("Workspaces per lane", "Each model lane runs in its own workspace, so lanes never share keys, limits or logs."),
        ("Scoped keys", "Keys are issued per workspace and per worker, and rotated. They never appear in reports or logs."),
        ("Spend limits", "Every engagement has a cost ceiling, enforced at the workspace level."),
        ("Usage logs", "Model calls are logged and tied back to the run ledger, so every step can be traced."),
        ("No training on our data", "We choose providers whose commercial terms exclude our inputs and outputs from model training."),
        ("Provider-independent", "The orchestration core addresses lanes, not vendors. A lane can change provider without touching the layers above it."),
    ],

    "controls_h": "Controls at every layer",
    "controls": [
        ("Identity and secret isolation", "Per-lane and per-client credentials; no path from one client to another."),
        ("Data-boundary control", "Client artifacts stay in their workspace; exports pass a redaction step."),
        ("Auditability", "Every action is attributable to an actor and an authorization reference, and reproducible."),
        ("Safe defaults", "Passive and read-only first; anything intrusive needs recorded authorization and is time-boxed."),
    ],

    "boundary_h": "What clients see, and what stays internal",
    "boundary_client": ("Clients see", ["Intake and scope", "Authorization records", "Reports and evidence export"]),
    "boundary_internal": ("Stays internal", ["Orchestration and model lanes", "Execution harnesses", "Runbooks and the knowledge layer"]),

    "band_h": "Want to see the platform in detail?",
    "band_cta": "Request a technical briefing",
}
