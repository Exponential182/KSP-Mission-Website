/* Mostly based on an image slideshow tutorial from W3schools. */

let slide_index = 0;
go_to_slide(slide_index);

function slide_shift(n) {
    go_to_slide(slide_index = slide_index + n)
}

function go_to_slide(n) {
    let i;
    let slides = document.getElementsByClassName("image-slide")
    let left_arrows = document.getElementsByClassName("previous")
    let right_arrows = document.getElementsByClassName("next")
    console.log(n)
    if (n < 0) {
        slide_index = 0
    } else if (n >= slides.length) {
        slide_index = slides.length - 1
    } else {
        slide_index = n
    }
    for (i = 0; i < slides.length; i++) {
        if (i == slide_index) {
            slides[i].style.display = "block"
        } else {
            slides[i].style.display = "none"
        }
    if (slide_index == 0) {
        left_arrows[0].style.opacity = 0
        left_arrows[0].style.cursor = "default"
    } else if (slide_index == slides.length - 1) {
        right_arrows[slides.length - 1].style.opacity = 0
        right_arrows[slides.length - 1].style.cursor = "default"
    } else {
        left_arrows[0].style.opacity = 1
        right_arrows[slides.length - 1].style.opacity = 1
        left_arrows[0].style.cursor = "pointer"
        right_arrows[slides.length - 1].style.cursor = "pointer"
    }
    }
}
