# Task Plot Review

## Evidence Match

- Pass: title and construct match the responder-side Ultimatum Game.
- Pass: rows match configured fair, unfair, and very unfair offer profiles.
- Pass: phase order matches README and `src/run_trial.py`: Cue -> Fixation -> Offer decision -> Confirmation -> Payoff feedback -> ITI.
- Pass: timing labels match config: 500 ms cue, 600 ms fixation, 2000 ms decision, 600 ms confirmation, 1000 ms feedback, 800 ms ITI.
- Pass: decision key mapping shows F accept and J reject.
- Pass: payoff feedback shows that accept earns the responder share, while reject or timeout earns 0.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
