
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

func forEach(elements, f)
    let newElements = map(elements, f)
    let elements = []
    for i = 0 to length(newElements) do
        append(elements, f(newElements/i))
    end
end

func reduce(elements, f)
    let prev = elements/0

    for i = 1 to length(elements) do
        let prev = f(prev, elements/i)
    end

    return prev
end

func reduceStartWith(elements, f, start)
    return reduce(extend([start], elements), f)
end


func reduceRight(elements, f)
    let prev = elements/(length(elements) - 1)

    for i = length(elements) - 2 to 0 step -1 do
        let prev = f(prev, elements/i)
    end

    return prev
end

func reduceRightStartWith(elements, f, start)
    return reduceRight(extend(elements, [start]), f)
end

