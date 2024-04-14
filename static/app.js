let img = document.querySelector("input#img")
let img_show = document.querySelector("img")
let predict_btn = document.querySelector("button")
let h2 = document.querySelector("h2")

// Get prediction by sending POST request
async function getData(image) {
    let data = await fetch("/", {
        method: "POST",
        body: image
    })
    return data.json()
}


predict_btn.addEventListener("click", async () => {
    let image = img.files[0]
    let imgurl = URL.createObjectURL(image)
    img_show.src = imgurl;
    let data = new FormData()
    data.append("image", image)
    h2.innerHTML = "Loading <div id='loading'></div>"
    let response = await getData(data);
    h2.innerText = response
})


img.addEventListener("input", () => {
    let image = img.files[0]
    let imgurl = URL.createObjectURL(image)
    img_show.src = imgurl;
    h2.innerText = ""
    predict_btn.style.display = 'block'
})

