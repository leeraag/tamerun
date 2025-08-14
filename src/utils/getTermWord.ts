export const getTermWord = (term: number) => {
    const lastDigit = term % 10;
    const lastTwoDigits = term % 100;

    if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
        return "лет";
    }

    if (lastDigit === 1) {
        return "год";
    }

    if (lastDigit >= 2 && lastDigit <= 4) {
        return "года";
    }

    return "лет";
}