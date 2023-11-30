let num_of_inputs = 1;

window.onload = function () {
    num_of_inputs = document.getElementById("num_round").value;
    num_result_round = document.getElementById("num_result_round");
    if (num_result_round != null) {
        num_result_round = num_result_round.value;
    }
}

function new_round() {
    num_of_inputs++;

    let div = document.createElement('div');
    div.className = "round input-group";
    div.innerHTML = `<input placeholder="Название раунда" class="form-control mt-2" type="text" id="round${num_of_inputs}" name="round${num_of_inputs}"/>`

    document.getElementById("round_append").append(div);
    document.getElementById("num_round").value = num_of_inputs;
}

function delete_round() {
    if (parseInt(num_of_inputs) !== 1) {
        document.getElementById("round" + num_of_inputs).remove();
        num_of_inputs--;
        document.getElementById("num_round").value = num_of_inputs;
    }
}