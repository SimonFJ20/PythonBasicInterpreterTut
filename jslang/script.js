
const codeIn = document.getElementById('code-in');
const runButton = document.getElementById('run');
const codeOut = document.getElementById('code-out');

runButton.addEventListener('click', () => {

    const code = codeIn.value;

    codeOut.innerText = code;

});

