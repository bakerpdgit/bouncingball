const output = document.getElementById("output");

$(document).ready(function() {
  $.get('code.py', function(data) {
    evaluatePython(data);
  });
});

OUTPUT_PATCH = `
import sys
import io
sys.stdout = io.StringIO()
from js import addToOutput
orig_print = print
# redirect print via output textarea and console
def new_print(*args, **kwargs):
  stdout_len = len(sys.stdout.getvalue())
  orig_print(*args, **kwargs)
  stdout = sys.stdout.getvalue()
  addToOutput(stdout[stdout_len:])
  sys.stdout.flush()
print = new_print
`

INPUT_PATCH = `
from js import input_patch
input = input_patch
__builtins__.input = input_patch
`

function addToOutput(s) {
  output.value += s;
  console.log(s);
}

window.onerror = function(msg, url, lineNo, columnNo, error) {
  try {
    addToOutput("Error occurred: to view, run page in new tab & use ctrl-shift-j to view console");  
    //for clearing all intervals
    //var interval_id = window.setInterval("", 9999); // Get a reference to the last interval +1
    //for (var i = 1; i < interval_id; i++) {
    //    try {
    //        window.clearInterval(i);
    //    } catch {}
    //}
    pyodide.runPython("window.clearInterval(intervalHandle)");  
  } catch(err) {}
};

addToOutput('Initializing...\n');
// init Pyodide

async function main(){
  await loadPyodide({ indexURL : 'https://cdn.jsdelivr.net/pyodide/v0.17.0/full/' });
  addToOutput('Ready!\n');
}

function input_patch(text) {
    return prompt(text);
};

pyodideReadyPromise = main();

async function evaluatePython(code) {
  await pyodideReadyPromise;
  await pyodide.runPythonAsync(OUTPUT_PATCH);
  await pyodide.runPythonAsync(INPUT_PATCH);
      
  try {
    let output = await pyodide.runPythonAsync(code);
    var stdout = pyodide.runPython("sys.stdout.getvalue()");
    addToOutput(stdout);
  } catch(err) {
    addToOutput(err);
  }
}






