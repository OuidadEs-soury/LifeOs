function allowDrop(ev){
ev.preventDefault()
}

function drag(ev){
ev.dataTransfer.setData("text",ev.target.id)
}

function drop(ev){

ev.preventDefault()

const taskId = ev.dataTransfer.getData("text")

const taskElement = document.getElementById(taskId)

const column = ev.target.closest(".column")

column.appendChild(taskElement)

const newStatus = column.dataset.status

const id = taskId.split("-")[1]

fetch("/update_task",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
task_id:id,
status:newStatus
})

})

}