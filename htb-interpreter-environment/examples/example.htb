
func oopify(prefix) -> prefix + "oop"

func join(elements, seperator)
    let result = ""
    let len = length(elements)

    for i = 0 to len do
        let result = result + elements/i
        if i == len - 1 then break
        let result = result + seperator
    end

    return result
end

func map(elements, f)
    let new_elements = []

    for i = 0 to length(elements) do
        append(new_elements, f(elements/i))
    end

    return new_elements
end

print("Hello world");

for i = 0 to 5 do
    print(join(map(["l", "sp"], oopify), ", "))
end

