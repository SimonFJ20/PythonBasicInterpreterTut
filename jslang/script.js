
const codeIn = document.getElementById('code-in');
const runButton = document.getElementById('run');
const codeOut = document.getElementById('code-out');

const lexer = new Lexer();

runButton.addEventListener('click', () => {

    const code = codeIn.value;

    const tokens = lexer.lex(code);

    const tstr = tokens.map(token => token.toString()).join('\n');

    codeOut.innerText = tstr;

});

