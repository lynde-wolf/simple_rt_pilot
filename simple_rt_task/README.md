# Shape Simple RT Task

A baseline reaction-time task: a triangle appears after a jittered non-aging foreperiod and the participant presses the spacebar as quickly as possible.

## Trial structure

| Event    | Duration (ms)                                            |
| -------- | -------------------------------------------------------- |
| Fixation | 250–1000, truncated decaying exponential, 50 ms grid     |
| Triangle | 1000 (response logged any time during this window; trial does not end on response) |

## Blocks

| Block Type | Number of Blocks | Trials per Block |
| ---------- | ---------------- | ---------------- |
| Practice   | 1                | 8                |
| Test       | 3                | 60               |

## Response

- Place the **thumb** on the **spacebar**.
- Respond as soon as the triangle appears.

## Files

| File           | Purpose                                                       |
| -------------- | ------------------------------------------------------------- |
| `index.html`   | Local test runner (jsPsych from CDN, expfactory shims, attention-check stub). |
| `experiment.js`| Timeline definition (`simple_rt_pilot_init`, `simple_rt_pilot_experiment`). |
| `style.css`    | Layout for fixation, prompt box, and triangle stimulus.       |
| `config.json`  | expFactory deployment metadata.                                |
| `images/triangle.png` | Stimulus image.                                         |

## Local testing

Open `index.html` directly in Chrome or Firefox. A small launch screen lets you set `group_index` before the experiment starts.
