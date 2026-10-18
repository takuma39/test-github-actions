import { add, divide, multiply, subtract } from "./calculator";

const operations = { add, subtract, multiply, divide } as const;

type OperationName = keyof typeof operations;

function isOperationName(value: string): value is OperationName {
  return value in operations;
}

const form = document.querySelector<HTMLFormElement>("#calc-form");
const lhsInput = document.querySelector<HTMLInputElement>("#lhs");
const rhsInput = document.querySelector<HTMLInputElement>("#rhs");
const operatorSelect = document.querySelector<HTMLSelectElement>("#operator");
const result = document.querySelector<HTMLOutputElement>("#result");

if (!form || !lhsInput || !rhsInput || !operatorSelect || !result) {
  throw new Error("必要な要素が見つかりません");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const lhs = Number(lhsInput.value);
  const rhs = Number(rhsInput.value);
  const operator = operatorSelect.value;

  if (!isOperationName(operator)) {
    result.textContent = "不明な演算子です";
    return;
  }

  try {
    result.textContent = `= ${operations[operator](lhs, rhs)}`;
    result.dataset.state = "ok";
  } catch (error) {
    result.textContent = error instanceof Error ? error.message : "計算に失敗しました";
    result.dataset.state = "error";
  }
});
