export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("0 で割ることはできません");
  }
  return a / b;
}

export function average(values: number[]): number {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

export function percentOf(part: number, total: number): number {
  return (part / total) * 100;
}

export function parseNumber(input: string): number {
  return Number(input);
}
