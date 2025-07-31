let slide_index = 1;
go_to_slide(slide_index);

function slide_shift(n) {
    go_to_slide(slide_index += n)
}

function go_to_slide(n) {
    let i;
    let slides = document.getElementsByClassName("image-slide")
    let previews = document.getElementsByClassName("image-preview-slide")
    console.log(n)


}
