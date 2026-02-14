export function formatNumber(number) {
  if (number === null || number === undefined) return "";
  if (isNaN(number)) return number;
  return Number(number).toLocaleString("en-US");
}
