function getBlueprintData() {
    console.log("Making Ajax call...")
    
    url = `${window.location.href}/blueprint`
    console.log(`target url: ${url}`)

    fetch(url).then((res) => {
        console.log("command is done")
        output = document.getElementById("output")
        running = document.getElementById("running")
        running.style.display = "none"
        if (res.status == 400) {
            res.json().then(data => {
                errorMsg = data.msg
                output.innerHTML = `
                <h2>Error on Flask Server. Response: ${res.status}</h2>
                <h3 style="color:red">${errorMsg}</h3>
                `
                return
            })
            
        }
        if (res.status != 200) {
            output.innerText = `Error on Server. Response: ${res.status}`
            return
        }
        res.json().then(data => {
            // debugger;
            resultHTML = ""
            console.log(data)
            data.forEach((blueprint) => {
                name = blueprint.Name
                description = blueprint.Description
                cardHTML = `<div class="card border-primary mb-3">
                                <div class="card-body">
                                    <h3 class="card-title">${name}</h3>
                                    <p class="card-text">${description}</p>
                                </div>
                            </div>`
                resultHTML += cardHTML
            })
            output.innerHTML = resultHTML
        })
    })
}

//getBlueprintData()
