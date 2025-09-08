export type TInstallmentSettings = {
    initial_payment_percentage: number,
    installment_percentage: number,
    installment_period: number,
    intermediate_payments: number[][],
    monthly_payment_percentage: number,
};