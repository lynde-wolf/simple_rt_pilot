# Simple RT Pilot

A standalone pilot of the **shape simple RT** baseline task — a triangle appears after a non-aging foreperiod and the participant presses the spacebar as quickly as possible. Extracted from Experiment 4 (`stop_signal_with_integrated_memory_e4`) so it can be deployed and analyzed independently.

## Layout

```
simple_rt_pilot/
├── pyproject.toml            # uv project for the pytest harness
├── uv.lock
├── tests/                    # Node-backed unit tests for experiment.js
└── simple_rt_task/           # the deployable jsPsych task
    ├── config.json
    ├── experiment.js
    ├── index.html
    ├── style.css
    └── images/triangle.png
```

## Trial structure

Each trial has two events:

| Event    | Duration                                                           |
| -------- | ------------------------------------------------------------------ |
| Fixation | jittered foreperiod **1000–5000 ms**, truncated decaying exponential on a 50 ms grid, mean 2000 ms (`Math.floor` snap) |
| Shape    | **1000 ms** fixed. A triangle or a diamond appears (the diamond is `square.png` rotated 45°), randomly chosen per trial. Spacebar is the response for **any** shape; the trial does not end on response |

The non-aging foreperiod makes shape onset unpredictable.

## Errant key logging

A document-level `keydown` listener captures every key press for the entire session — including during fixation, ITI, instructions, and the attention check — annotated with the active `trial_id` and time-in-trial. The full log is serialized to `all_keypresses` (and `total_keypress_count`) on the experiment data object at the end of the run.

## Block structure

| Phase    | Blocks | Trials per block | Total |
| -------- | ------ | ---------------- | ----- |
| Practice | 1      | 8                | 8     |
| Test     | 3      | 60               | 180   |

Between test blocks the participant sees a feedback screen (omission rate, average RT). An attention-check probe runs before each test block.

## Estimated duration
~10 minutes (instructions + practice + 3 test blocks + post-task survey).

## Local testing
Open [`simple_rt_task/index.html`](simple_rt_task/index.html) in Chrome or Firefox. jsPsych is loaded from a CDN and the attention-check plugin plus the expfactory globals are shimmed locally, so no server is required. The launch screen lets you set `group_index` (recorded with the data; reserved for future counterbalancing across pilots).

## Running tests

```sh
uv sync
uv run pytest -v
```

The harness loads `experiment.js` into Node and exercises pure-JS helpers (foreperiod sampling, shuffle, timeline construction, configuration constants). Requires `node` on the path.

## Deployment

Update the `pathSource` in `simple_rt_task/experiment.js` to point at the deployed image directory before publishing.
