document.addEventListener("DOMContentLoaded", ()=>{
    getJson("/d", (data)=>{
        const parent = document.getElementById('outer')
        console.log(data)
        for (let [timestamp, cmd] of data){
            let ele = document.createElement('p')
            ele.innerHTML = timestamp + ", " + cmd
            parent.appendChild(ele)
        }
        console.log('runned')
    })
})


function getJson(addr, callback){
    const req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           // Typical action to be performed when the document is ready:
            callback(JSON.parse(req.responseText))

        }
    };
    req.open("GET",addr, true);
    req.send();
}