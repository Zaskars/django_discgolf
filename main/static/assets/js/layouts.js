let num_of_inputs = 1;

window.onload = function () {
    num_of_inputs = document.getElementById("num_layout").value;
    num_result_layout = document.getElementById("num_result_layout");
    if (num_result_layout != null) {
        num_result_layout = num_result_layout.value;
    }
}

function new_layout() {
    num_of_inputs++;

    let div = document.createElement('div');
    div.className = "layout input-group";
    div.innerHTML = `<input placeholder="Название схемы" class="form-control mt-2" type="text" id="layout${num_of_inputs}" name="layout${num_of_inputs}"/>`

    document.getElementById("layout_append").append(div);
    document.getElementById("num_layout").value = num_of_inputs;
}

function delete_layout() {
    if (parseInt(num_of_inputs) !== 1) {
        document.getElementById("layout" + num_of_inputs).remove();
        num_of_inputs--;
        document.getElementById("num_layout").value = num_of_inputs;
    }
}