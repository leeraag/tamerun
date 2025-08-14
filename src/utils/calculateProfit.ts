export type TYearlyData = {
  year: number;
  initialAmount: number;
  income: number;
  finalAmount: number;
}

export const calculateProfit = (
  initialAmount: number,
  annualRate: number,
  years: number
): { total: number; yearlyData: TYearlyData[] } => {
  let currentAmount = initialAmount;
  const yearlyData: TYearlyData[] = [];

  for (let year = 1; year <= years; year++) {
    const income = currentAmount * (annualRate / 100);
    const finalAmount = currentAmount + income;
    
    yearlyData.push({
      year,
      initialAmount: currentAmount,
      income,
      finalAmount
    });

    currentAmount = finalAmount;
  }

  return {
    total: currentAmount,
    yearlyData
  };
};