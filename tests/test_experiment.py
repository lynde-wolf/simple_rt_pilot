"""Tests for simple_rt_pilot experiment.js functions.

Run with:
    cd simple_rt_pilot
    uv run pytest -v
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

HARNESS = Path(__file__).parent / 'js_harness.js'


def call_js(fn: str, *args) -> dict | list:
    """Execute a JS function via the Node harness and return parsed JSON."""
    cmd = json.dumps({'fn': fn, 'args': list(args)})
    result = subprocess.run(
        ['node', str(HARNESS), cmd],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        raise RuntimeError(f'Node error:\n{result.stderr}')
    return json.loads(result.stdout)


# ---------------------------------------------------------------
# Experiment variables
# ---------------------------------------------------------------

class TestExperimentVariables:
    @pytest.fixture(autouse=True)
    def _load_vars(self):
        self.vars = call_js('getVars')

    def test_practice_length(self):
        assert self.vars['shapeRtPracticeLen'] == 8

    def test_test_block_size(self):
        assert self.vars['numTrialsPerShapeRtBlock'] == 60

    def test_num_test_blocks(self):
        assert self.vars['numShapeRtTestBlocks'] == 3

    def test_stim_duration(self):
        assert self.vars['shapeRtStimDuration'] == 1000

    def test_omission_threshold(self):
        assert self.vars['omissionResponseThresh'] == 0.2

    def test_rt_threshold(self):
        assert self.vars['rtThresh'] == 1000

    def test_fixation_window(self):
        assert self.vars['FIXATION_MIN_MS'] == 250
        assert self.vars['FIXATION_MAX_MS'] == 1000
        assert self.vars['FIXATION_STEP_MS'] == 50

    def test_default_group_index(self):
        assert self.vars['group_index'] == 1

    def test_exp_id(self):
        assert self.vars['expID'] == 'simple_rt_pilot'


# ---------------------------------------------------------------
# Foreperiod sampling
# ---------------------------------------------------------------

class TestSampleFixationDuration:
    @pytest.fixture(scope='class')
    def samples(self):
        return call_js('sampleFixationDuration', 2000)

    def test_within_bounds(self, samples):
        assert all(250 <= s <= 1000 for s in samples)

    def test_on_50ms_grid(self, samples):
        assert all(s % 50 == 0 for s in samples)

    def test_covers_range(self, samples):
        # Over 2000 draws we should hit both extremes plus several middle values
        assert min(samples) <= 300
        assert max(samples) >= 900
        assert len(set(samples)) >= 8

    def test_decaying_distribution(self, samples):
        # Truncated decaying exponential: more mass near MIN than near MAX.
        below_500 = sum(1 for s in samples if s <= 500)
        above_500 = sum(1 for s in samples if s > 500)
        assert below_500 > above_500, (
            f'Distribution not decaying: {below_500} below 500ms, '
            f'{above_500} above'
        )


# ---------------------------------------------------------------
# shuffleArray
# ---------------------------------------------------------------

class TestShuffleArray:
    def test_preserves_length(self):
        result = call_js('shuffleArray', [1, 2, 3, 4, 5])
        assert len(result) == 5

    def test_preserves_elements(self):
        result = call_js('shuffleArray', [10, 20, 30, 40])
        assert sorted(result) == [10, 20, 30, 40]

    def test_does_not_mutate_input_in_js(self):
        result = call_js('shuffleArrayWithMutationCheck', [1, 2, 3, 4, 5])
        assert result['inputAfter'] == result['inputBefore']
        assert sorted(result['output']) == sorted(result['inputBefore'])

    def test_empty_array(self):
        assert call_js('shuffleArray', []) == []

    def test_single_element(self):
        assert call_js('shuffleArray', [42]) == [42]


# ---------------------------------------------------------------
# Timeline construction
# ---------------------------------------------------------------

class TestTimeline:
    @pytest.fixture(scope='class')
    def timeline(self):
        return call_js('getTimeline')

    def test_timeline_built(self, timeline):
        assert timeline['length'] > 0

    def test_includes_test_key_reminder(self, timeline):
        assert 'test_key_reminder' in timeline['trialIds']

    def test_ends_with_post_task_and_end(self, timeline):
        ids = timeline['trialIds']
        assert 'post_task_feedback' in ids
        assert 'end' in ids
