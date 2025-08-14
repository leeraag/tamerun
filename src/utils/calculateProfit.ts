export const calculateProfit = (
    initialAmount: number,
    annualRate: number,
    years: number
): number => {
    return initialAmount + initialAmount * (annualRate / 100) * years;
}