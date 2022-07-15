let butUp = document.getElementById("upper-case");
let butLo = document.getElementById("lower-case");
let butPr = document.getElementById("proper-case");
let butSe = document.getElementById("sentence-case");
let butSa = document.getElementById("save-text-file");
let text = document.querySelector("textarea");

function download(filename, text) {
    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

butUp.addEventListener("click", function () {
    text.value = text.value.toUpperCase();
});

butLo.addEventListener("click", function () {
    text.value = text.value.toLowerCase();
});

butPr.addEventListener("click", function () {
    text.value = text.value.toLowerCase().split(' ').map(txt => txt.replace(txt.charAt(0), txt.charAt(0).toUpperCase()))
        .join(' ');

});

butSe.addEventListener("click", function () {
    text.value = text.value.toLowerCase().split('. ').map(txt => txt.replace(txt.charAt(0), txt.charAt(0).toUpperCase()))
        .join('. ');
});

butSa.addEventListener("click", function () {
    download("text.txt",text.value);
});

