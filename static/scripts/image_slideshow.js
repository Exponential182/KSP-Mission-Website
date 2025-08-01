let slide_index = 1;
go_to_slide(slide_index);

function slide_shift(n) {
    go_to_slide(slide_index += n)
}

function go_to_slide(n) {
    let i;
    let slides = document.getElementsByClassName("image-slide")
    let previews = document.getElementsByClassName("image-preview")
    if (n > slides.length) {slide_index = 1}
    else if (n < 1) {slide_index = slides.length}
    else {slide_index = n}
    for (i = 0; i < slides.length; i++) {
        if (i == slide_index) {slides[i].style.display = "block"}
        else {slides[i].style.display = "none"}
        
    }
    for (i = 0; i < previews.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }    
    dots[slide_index-1].className += " active"
}
