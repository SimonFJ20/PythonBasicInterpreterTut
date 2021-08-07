
const htmlSafe = (...strings) => strings.map(str => str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'));

const CC = {
    keyword: 'keyword',
    common: 'common',
    string: 'string',
    symbol: 'symbol'
}

class Builder {

    error = (msg) => {
        console.warn('BuilderError: ' + msg);
    }

    advance = () => {
        this.index++;
        const newToken = this.tokens[this.index];
        this.currentToken = newToken instanceof Token ? newToken : null;
    }
    
    build = (tokens) => {
        this.tokens = tokens;
        this.index = -1;
        this.currentToken = null;
        let html = '';
        this.advance();
        while (this.currentToken !== null) {
            console.log('Building:', this.currentToken.type)
            switch (this.currentToken.type) {
                case TT.HASHTAG:
                    html += this.makePreprocessorKeyword();
                    break;
                case TT.NEWLINE:
                    html += '<br>';
                    this.advance();
                    break;
                case TT.EOF:
                    this.advance();
                    break;
                default:
                    console.log('Unknown token:', this.currentToken.toString());
                    this.advance();
            }
        }
        return html;
    }

    makePreprocessorIncludeValue = () => {
        if (this.currentToken.type !== TT.STRING && this.currentToken.type !== TT.INCLUDESTRING) {
            this.error(`Expected 'STRING' or 'INCLUDESTRING' after '#include' got '${this.currentToken.text}'`);
            return '';
        }
        const text = htmlSafe(this.currentToken.text);
        this.advance()
        return `<span class="${CC.string}">${text}</span>`;
    }

    makePreprocessorDefineKey = () => {
        if (this.currentToken.type !== TT.IDENTIFIER) {
            this.error(`Expected 'IDENTIFIER' after '#define' got '${this.currentToken.text}'`);
            return '';
        }
        const value = htmlSafe(this.currentToken.value);
        this.advance();
        return `<span class="${CC.symbol}">${value}</span>`;
    }

    makePreprocessorDefineValue = () => {
        let text = '';
        while (this.currentToken.type !== TT.NEWLINE) {
            text += this.currentToken.text;
            this.advance();
        }
        return `<span class="${CC.common}">${text}</span>`;
    }

    makePreprocessorKeyword = () => {
        this.advance();
        if (this.currentToken.type !== TT.KEYWORD) {
            this.error(`Expected 'KEYWORD' after '#' got '${this.currentToken.text}'`);
            return '';
        }
        const keyword = this.currentToken.value;
        let html = `<span class="${CC.keyword}">#${keyword}</span>`
        this.advance();
        while (this.currentToken.type === TT.SPACE) {
            html += '&nbsp;';
            this.advance();
        }
        switch (keyword) {
            case 'include':
                html += this.makePreprocessorIncludeValue();
                break;
            case 'define':
                html += this.makePreprocessorDefineKey();
                while (this.currentToken.type === TT.SPACE) {
                    html += '&nbsp;';
                    this.advance();
                }
                html += this.makePreprocessorDefineValue();
                break;
        }            
        while (this.currentToken.type !== TT.NEWLINE) {
            html += this.currentToken;
            this.advance();
        }
        return html;
    }

}
