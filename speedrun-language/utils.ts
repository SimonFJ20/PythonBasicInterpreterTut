export class Option<T> {
    private static None = Symbol("None");

    private constructor(
        private ok: boolean,
        private value: T | typeof Option.None,
    ) {}

    public static some<T>(value: T): Option<T> {
        return new Option<T>(true, value);
    }

    public static none<T>(): Option<T> {
        return new Option<T>(false, Option.None);
    }

    public is_ok(): boolean {
        return this.ok;
    }

    public is_err(): boolean {
        return !this.ok;
    }

    public unwrap(): T {
        if (this.ok) return this.value as T;
        else throw new Error("cannot unwrap non-ok result");
    }

    public expect(msg: string): T {
        if (this.ok) return this.value as T;
        else throw new Error(`cannot unwrap non-ok result, expected ${msg}`);
    }

    public match<Y>(case_some: (v: T) => Y, case_none: () => Y): Y {
        return this.ok ? case_some(this.value as T) : case_none();
    }
}

export const Some = <T>(value: T): Option<T> => Option.some<T>(value);
export const None = <T>(): Option<T> => Option.none<T>();

export class Result<T, E> {
    private constructor(
        private ok: boolean,
        private value: Option<T>,
        private error: Option<E>,
    ) {}

    public static ok<T, E>(value: T): Result<T, E> {
        return new Result<T, E>(true, Some(value), None());
    }

    public static error<T, E>(error: E): Result<T, E> {
        return new Result<T, E>(false, None(), Some(error));
    }

    public is_ok(): boolean {
        return this.ok;
    }

    public is_err(): boolean {
        return !this.ok;
    }

    public transform<NT, NE extends E>(): Result<NT, NE> {
        if (!this.ok) return this as unknown as Result<NT, NE>;
        else throw new Error("cannot transform ok result");
    }

    public unwrap(): T {
        if (this.ok) return this.value.unwrap();
        else throw new Error("cannot unwrap non-ok result");
    }

    public unwrap_err(): E {
        if (!this.ok) return this.error.unwrap();
        else throw new Error("cannot unwrap error of ok result");
    }

    public expect(msg: string): T {
        if (this.ok) return this.value.unwrap();
        else throw new Error(`cannot unwrap non-ok result, expected ${msg}`);
    }

    public expect_err(msg: string): E {
        if (!this.ok) return this.error.unwrap();
        else
            throw new Error(
                `cannot unwrap error of ok result, expected ${msg}`,
            );
    }

    public match<Y>(case_ok: (v: T) => Y, case_error: (e: E) => Y): Y {
        return this.ok
            ? case_ok(this.value.unwrap())
            : case_error(this.error.unwrap());
    }
}

export const Ok = <T, E>(value: T) => Result.ok<T, E>(value);
export const Err = <T, E>(error: E) => Result.error<T, E>(error);

export const force = <T extends U, U>(v: U) => v as unknown as T;

export const qmark = <Y, T, E>(
    result: Result<T, E>,
    action: (value: T) => Y,
) => {
    if (result.is_err()) return result;
    else return action(result.unwrap());
};

export const _ = Symbol("_");
export const Or = Symbol("|");

export const match = <V, T>(
    value: V,
    cases: [v: V | typeof _, action: (() => T) | typeof Or][],
): T => {
    for (const [v, action] of cases)
        if ((v === _ || v === value) && action !== Or) return action();
    throw new Error("unexhaustive match");
};

export const id_generator = () =>
    (
        (ids) => () =>
            ids.next().value!
    )(
        (function* () {
            for (let i = 0; true; i++) yield i;
        })(),
    );
