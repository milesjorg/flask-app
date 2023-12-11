const colorSwapToggle = document.querySelector('#colorSwap');
const colorChanger = document.querySelector('#colorChanger');

function swapColors() {
    const currentBackgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color');
    const currentTextColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary-color');

    document.documentElement.style.setProperty('--primary-color', currentTextColor);
    document.documentElement.style.setProperty('--secondary-color', currentBackgroundColor);

    saveColorsToStorage();
}

function getRandomColor() {
    //TODO: Fix getRandomHexColor - making nonhex values occasionally
    const getRandomHexColor = () => '#' + Math.floor(Math.random() * 16777215).toString(16);
    
    const isValidHexColor = (color) => /^#[0-9A-Fa-f]{6}$/.test(color);

    const getContrastRatio = (primaryColor, secondaryColor) => {
        const luminance1 = getLuminance(primaryColor);
        const luminance2 = getLuminance(secondaryColor);
        const brighter = Math.max(luminance1, luminance2);
        const darker = Math.min(luminance1, luminance2);
        return (brighter + 0.05) / (darker + 0.05);
    };

    const getLuminance = (color) => {
        const rgb = parseInt(color.slice(1), 16);
        const r = (rgb >> 16) & 0xff;
        const g = (rgb >>  8) & 0xff;
        const b = (rgb >>  0) & 0xff;
        const luminance = 0.2126 * (r / 255) + 0.7152 * (g / 255) + 0.0722 * (b / 255);
        return luminance;
    };

    let primaryColor = getRandomHexColor();
    let secondaryColor;
    let maxAttempts = 100;
    let attempts = 0;
    do {
        secondaryColor = getRandomHexColor();
        attempts++;

        if (attempts >= 200) {
            console.log("Max attempts reached, breaking loop");
            break;
        }
    } while (!isValidHexColor(secondaryColor) || getContrastRatio(primaryColor, secondaryColor) < 4.5);

    saveColorsToStorage();
    return { primary: primaryColor, secondary: secondaryColor };
}

function setRandomColors() {
    const newColors = getRandomColor();
    document.documentElement.style.setProperty('--primary-color', newColors.primary);
    document.documentElement.style.setProperty('--secondary-color', newColors.secondary);
    console.log(newColors);
}

function applyColorsFromStorage() {
    const storedPrimaryColor = localStorage.getItem('primary-color');
    const storedSecondaryColor = localStorage.getItem('secondary-color');

    if (storedPrimaryColor && storedSecondaryColor) {
        document.documentElement.style.setProperty('--primary-color', storedPrimaryColor);
        document.documentElement.style.setProperty('--secondary-color', storedSecondaryColor);
    }
}

function saveColorsToStorage() {
    const currentPrimaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color');
    const currentSecondaryColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary-color');

    localStorage.setItem('primary-color', currentPrimaryColor);
    localStorage.setItem('secondary-color', currentSecondaryColor);
}

colorSwapToggle.addEventListener('click', swapColors);
colorChanger.addEventListener('click', setRandomColors);

applyColorsFromStorage();