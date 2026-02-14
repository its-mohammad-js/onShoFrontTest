export default defineNuxtPlugin(() => {
    const convertToPersianNumbers = (text) => {
        if (!text) return text;

        const englishNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
        const persianNumbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

        return text.replace(/[0-9]/g, (char) => persianNumbers[englishNumbers.indexOf(char)]);
    };

    const convertNumbersInDOM = () => {
        const elements = document.body.querySelectorAll('*:not(script):not(style):not(noscript)');
        elements.forEach((element) => {
            element.childNodes.forEach((node) => {
                if (node.nodeType === Node.TEXT_NODE && /\d/.test(node.nodeValue)) {
                    node.nodeValue = convertToPersianNumbers(node.nodeValue);
                }
            });
        });
    };

    const observer = new MutationObserver(() => {
        convertNumbersInDOM();
    });

    // شروع مشاهده تغییرات در کل DOM
    observer.observe(document.body, { childList: true, subtree: true });

    // اجرای اولیه تبدیل اعداد
    convertNumbersInDOM();
});
