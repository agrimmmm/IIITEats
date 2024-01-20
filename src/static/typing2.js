const typingText2 = "We Have Still Got You Covered!!";
const typingDelay2 = 40; // in milliseconds
let index2 = 0;
const typingEl2 = document.getElementById("typing2");

function type2() {
    typingEl2.textContent += typingText2[index];

    if (++index < typingText2.length) {
        setTimeout(type, typingDelay2);
    }
}

setTimeout(type2, typingDelay2);