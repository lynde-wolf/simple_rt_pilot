// Minimal jsPsych mock so experiment.js can be loaded in Node.
// Receives a JSON command on argv[2] and prints JSON results to stdout.

globalThis.window = { efVars: { group_index: 1 } };
globalThis.document = {
  body: {},
  currentScript: null,
  getElementsByTagName: function () { return []; },
  addEventListener: function () {},
};
globalThis.performance = { now: () => Date.now() };
globalThis.navigator = { userAgent: 'node', languages: [], plugins: [] };

globalThis.jsPsych = {
  randomization: {
    repeat: function (arr, reps) {
      var out = [];
      for (var r = 0; r < reps; r++) {
        out = out.concat(JSON.parse(JSON.stringify(arr)));
      }
      for (var i = out.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = out[i];
        out[i] = out[j];
        out[j] = tmp;
      }
      return out;
    },
  },
  pluginAPI: {
    preloadImages: function () {},
  },
  data: {
    addProperties: function () {},
    get: function () {
      return {
        last: function () {
          return { trials: [], values: function () { return [{}]; } };
        },
      };
    },
  },
};

// Stub plugin constructors so experiment.js doesn't error on reference
globalThis.jsPsychHtmlKeyboardResponse = 'jsPsychHtmlKeyboardResponse';
globalThis.jsPsychInstructions = 'jsPsychInstructions';
globalThis.jsPsychHtmlButtonResponse = 'jsPsychHtmlButtonResponse';
globalThis.jsPsychSurveyText = 'jsPsychSurveyText';
globalThis.jsPsychFullscreen = 'jsPsychFullscreen';
globalThis.jsPsychCallFunction = 'jsPsychCallFunction';
globalThis.jsPsychAttentionCheckRdoc = 'jsPsychAttentionCheckRdoc';
globalThis.jsPsychModule = {};
globalThis.initJsPsych = function () { return globalThis.jsPsych; };
globalThis.dataSync = function () {};

const fs = require('fs');
const vm = require('vm');
const path = require('path');
const src = fs.readFileSync(
  path.resolve(__dirname, '..', 'simple_rt_task', 'experiment.js'),
  'utf8',
);
vm.runInThisContext(src, { filename: 'experiment.js' });

const cmd = JSON.parse(process.argv[2]);
let result;

switch (cmd.fn) {
  case 'shuffleArray':
    result = shuffleArray(cmd.args[0]);
    break;
  case 'shuffleArrayWithMutationCheck': {
    var inputBefore = JSON.parse(JSON.stringify(cmd.args[0]));
    var output = shuffleArray(cmd.args[0]);
    result = { inputBefore: inputBefore, inputAfter: cmd.args[0], output: output };
    break;
  }
  case 'sampleFixationDuration': {
    var n = cmd.args[0] || 1000;
    var samples = [];
    for (var i = 0; i < n; i++) samples.push(sampleFixationDuration());
    result = samples;
    break;
  }
  case 'getVars':
    result = {
      shapeRtPracticeLen,
      numTrialsPerShapeRtBlock,
      numShapeRtTestBlocks,
      shapeRtStimDuration,
      omissionResponseThresh,
      rtThresh,
      FIXATION_MIN_MS,
      FIXATION_MAX_MS,
      FIXATION_STEP_MS,
      FIXATION_MEAN_MS,
      shapeStims,
      group_index,
      expID,
    };
    break;
  case 'getTimeline': {
    // Timeline is populated at module load — no init() call required.
    result = {
      length: simple_rt_pilot_experiment.length,
      trialIds: simple_rt_pilot_experiment
        .map(function (t) { return t && t.data && t.data.trial_id; })
        .filter(Boolean),
    };
    break;
  }
  default:
    result = { error: 'Unknown function: ' + cmd.fn };
}

process.stdout.write(JSON.stringify(result));
