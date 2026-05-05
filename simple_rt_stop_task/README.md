# Simple RT Stop Task

A simple-RT task with an integrated stop signal. A triangle or diamond (square rotated 45°) appears after a jittered non-aging foreperiod; the participant presses the spacebar as quickly as possible. On 1/3 of trials a star appears overlaid on the shape after a tracked stop-signal delay (SSD), and the participant should withhold the response.

## Trial structure

| Event    | Duration (ms) |
| -------- | -------------- |
| Fixation | 1000–5000, truncated decaying exponential, 50 ms grid, mean 2000 (`Math.floor` snap) |
| Shape    | Visible 1000 ms inside a 1500 ms trial window. Triangle or diamond, randomly per trial. Spacebar = any shape (single response, no choice); trial does not end on response. |
| Star (stop signal) | On stop trials only: appears `SSD` ms after shape onset, visible 500 ms, overlaid on the shape. |

## Conditions

- `go` (2/3 of trials): respond with spacebar.
- `stop` (1/3 of trials): a star appears after the SSD; withhold the response.
- Conditions are precomputed per block from `['go', 'go', 'stop']` shuffled to enforce the 2:1 ratio in every block.

## Stop-signal delay (SSD) staircase

- Initial SSD = 250 ms.
- Range: [0, 1000] ms, ±50 ms steps.
- Successful inhibition (no response on stop trial) → SSD += 50 ms.
- Failed inhibition (response on stop trial) → SSD −= 50 ms.

## Blocks

| Block Type | Number of Blocks | Trials per Block | Notes |
| ---------- | ---------------- | ---------------- | ----- |
| Practice   | 1 (up to 3 reps) | 12 (8 go / 4 stop) | Repeats up to 3× if go-trial accuracy ≤ 75%. |
| Test       | 3                | 60 (40 go / 20 stop) | 180 total trials, ~60 stop. |

## Per-block feedback

Reports go-trial accuracy, mean go RT, and the false-alarm rate on stop trials. Warnings fire if accuracy is low, RT is slow, omissions are high, FA rate ≥ 75%, or FA rate ≤ 25% (suggesting strategic slowing).

## Response

- Place the **thumb** on the **spacebar**.
- Press as soon as a shape appears.
- If a star appears on the shape, try not to press anything on that trial.

## Files

| File           | Purpose |
| -------------- | ------- |
| `index.html`   | Local test runner (jsPsych from CDN, inline `jsPoldracklabStopSignal` plugin stub, expfactory shims). |
| `experiment.js`| Timeline definition (`simple_rt_stop_task_init`, `simple_rt_stop_task_experiment`). |
| `style.css`    | Layout for fixation, prompt box, and shape stimuli. |
| `config.json`  | expFactory deployment metadata. |
| `images/triangle.png`, `images/square.png` | Shape stimuli. |
| `images/stopSignal.png` | Star image used as the stop cue. |

## Local testing

Open `index.html` directly in Chrome or Firefox (or serve with `python3 -m http.server`). A small launch screen lets you set `group_index` before the experiment starts.
