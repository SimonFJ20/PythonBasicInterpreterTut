export class Res<T, E = Error> {
    private constructor(
        public readonly ok: boolean,
        public readonly value: T | null,
        public readonly error: E | null,
    ) {}

    public static ok<T, E = Error>(value: T): Res<T, E> {
        return new Res<T, E>(true, value, null);
    }

    public static error<T, E = Error>(error: E): Res<T, E> {
        return new Res<T, E>(false, null, error);
    }

    public transform<Y, N extends E>(): Res<Y, N> {
        if (this.ok) throw new Error("cannot transform ok result");
        return this as unknown as Res<Y, N>;
    }

    public unwrap(): T {
        if (!this.ok) throw new Error("cannot unwrap non-ok result");
        return this.value!;
    }

    public match<K>(ok: (value: T) => K, error: (error: E) => K): K {
        if (this.ok) return ok(this.value!);
        else return error(this.error!);
    }
}

export const ok = <T, E = Error>(value: T) => Res.ok<T, E>(value);
export const error = <T, E = Error>(error: E) => Res.error<T, E>(error);
