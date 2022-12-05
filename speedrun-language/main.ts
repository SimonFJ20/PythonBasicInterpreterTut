import {
    Grammar,
    Parser,
} from "https://deno.land/x/nearley@2.19.7-deno/mod.ts";
import { Checker } from "./checker.ts";
import { generate } from "./code_generator.ts";
import compiled_grammar from "./grammar.out.ts";

const parse = (text: string) => {
    const parser = new Parser(Grammar.fromCompiled(compiled_grammar));
    parser.feed(text);
    return parser.results[0];
};

const compileToBinary = async (target_file_name: string, c_code: string) => {
    const temp_c_file = await Deno.makeTempFile();
    await Deno.writeTextFile(temp_c_file, c_code);
    const process = Deno.run({
        cmd: ["gcc", "-xc", temp_c_file, "-o", target_file_name],
    });
    await process.status();
    process.close();
    Deno.remove(temp_c_file);
};

if (Deno.args.length < 1) throw new Error("not enough args");
const text = await Deno.readTextFile(Deno.args[0]);
const res = parse(text);

console.log(JSON.stringify(res, null, "│   "));
const { functions, st, errors } = new Checker().check_program(res);
if (errors.length === 0) {
    const c_code = generate({ st, functions }, res);
    console.log(c_code);
    await compileToBinary("a.out", c_code);
} else {
    console.log("Compilation failed:");
    for (const v of errors) console.log(errors);
}
