import { interpret } from './jsua';
import './style.css'

const input = document.getElementById('input') as HTMLTextAreaElement;
const output = document.getElementById('output') as HTMLTextAreaElement;
const run = document.getElementById('run') as HTMLTextAreaElement;

run.addEventListener('click', () => {
    const text = input.value;
    const tokens = interpret(text);
    let out = '';
    for (let i in tokens) {
        out += tokens[i].value ? `[${tokens[i].type}: ${tokens[i].value}]\n` : `[${tokens[i].type}]\n`;
    }
    output.value = out;
});
