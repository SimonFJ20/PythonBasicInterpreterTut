
const codeIn = document.getElementById('code-in');
const runButton = document.getElementById('run');
const showTokensCheckbox = document.getElementById('show-tokens');
const codeOut = document.getElementById('code-out');

runButton.addEventListener('click', () => {

    const code = codeIn.value;

    const lexer = new Lexer();
    const tokens = lexer.lex(code);

    const tstr = tokens.map(token => token.toString()).join('\n');

    if (showTokensCheckbox.checked)
        codeOut.innerText = tstr;

    const builder = new Builder();
    const html = builder.build(tokens);

    if (!showTokensCheckbox.checked)
        codeOut.innerHTML = html;

});

