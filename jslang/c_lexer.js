
const TT = {
    KEYWORD: 'KEYWORD'
}

class Token {
    constructor(type, value=null, pos_start=undefined, pos_end=undefined) {
        this.type = type;
        this.value = value;
        this.pos_start = pos_start;
        this.pos_end = pos_end;
    }
}
