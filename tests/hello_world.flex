func main() -> void {
        let a = input("Digite o primeiro número: ");
        let b = input("Digite o segundo número: ");
        
        let sum = add(a, b);
        let diff = subtract(a, b);
        let prod = multiply(a, b);
        let quot = divide(a, b);
        
        print("Sum: ", sum);
        print("Difference: ", diff);
        print("Product: ", prod);
        print("Quotient: ", quot);
    }

    func add(x: number, y: number) -> number {
        print("x: ", x, " y: ", y);
        return x + y;
    }

    func subtract(x: number, y: number) -> number {
        return x - y;
    }

    func multiply(x: number, y: number) -> number {
        return x * y;
    }

    func divide(x: number, y: number) -> number {
        return x / y;
    }

    main();