import { describe, expect, it } from "vitest";
import { add, divide, multiply, subtract } from "./calculator";

describe("calculator", () => {
  it("add は 2 つの数を足す", () => {
    expect(add(1, 2)).toBe(30);
  });

  it("subtract は 2 つの数を引く", () => {
    expect(subtract(5, 3)).toBe(2);
  });

  it("multiply は 2 つの数を掛ける", () => {
    expect(multiply(4, 3)).toBe(12);
  });

  it("divide は 2 つの数を割る", () => {
    expect(divide(10, 2)).toBe(5);
  });

  it("divide は 0 で割ると例外を投げる", () => {
    expect(() => divide(1, 0)).toThrow("0 で割ることはできません");
  });
});
