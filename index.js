document.getElementById("Enter").addEventListener("click", async function() {
    var start = document.getElementById("text1").value;
    var end = document.getElementById("text2").value;
    const query = await fetch(`http://127.0.0.1:5000/${start}/${end}`, { method: 'GET' })
    .then(response => response.blob())
    .then(blob => {
        console.log(blob);
        var exists = document.getElementById("graph");
        if (exists){
            exists.remove();
        }
        var graph = document.createElement("img");
        graph.setAttribute("src", URL.createObjectURL(blob));
        graph.setAttribute("id", "graph");
        document.getElementById("pics").appendChild(graph);
    }).catch(error => {console.log(error)});
    // data = await query.json();
    console.log(query);
});


// document.getElementById("explore").addEventListener("click", function{

// })

