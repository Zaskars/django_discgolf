let num_of_inputs = 1;

window.onload = function () {
    num_of_inputs = document.getElementById("num_basket").value;
    num_result_basket = document.getElementById("num_result_basket");
    if (num_result_basket != null) {
        num_result_basket = num_result_basket.value;
    }
}

function new_basket() {
    num_of_inputs++;

    let div = document.createElement('div');
    div.className = "basket input-group";
    div.innerHTML = `<input placeholder="Пар" class="form-control mt-2" type="number" id="basket${num_of_inputs}" name="basket${num_of_inputs}"/>`

    document.getElementById("basket_append").append(div);
    document.getElementById("num_basket").value = num_of_inputs;
}

function delete_basket() {
    if (parseInt(num_of_inputs) !== 1) {
        document.getElementById("basket" + num_of_inputs).remove();
        num_of_inputs--;
        document.getElementById("num_basket").value = num_of_inputs;
    }
}