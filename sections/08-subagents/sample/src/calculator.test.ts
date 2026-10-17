import { describe, expect, it } from "vitest";
import { add, divide } from "./calculator";

describe("calculator", () => {
  it("add は 2 つの数を足す", () => {
    expect(add(1, 2)).toBe(3);
  });

  it("divide は 2 つの数を割る", () => {
    expect(divide(10, 2)).toBe(5);
  });
});
