

let get_input = function() {
    let Address = $("input#Address").val()
    let ICT = $("select#ICT").val()
    let Race = $("select#Race").val()
    let Gender = $("select#Gender").val()
    let d = new Date()
    let dayofweek = d.getDay()
    let month = d.getMonth()
    let hour = d.getHours()
    return {'Address': Address,
            'ICT': ICT,
            'Race': Race,
            'Gender': Gender,
            "dayofweek": dayofweek,
            "month": month,
            "hour": hour} 
};

let send_inputs_json = function(coefficients) {
    $.ajax({
    url: '/solve',
    contentType: "application/json; charset=utf-8",
    type: 'POST',
    success: function(data) {
        display_solutions(data);
    },
    data: JSON.stringify(coefficients)
});
};

let display_solutions = function(solutions) {
    $("span#solution").html("<em>no force:</em> " + solutions.p0.toFixed(4) + " <br>"  + "Level 1: " + solutions.p1.toFixed(4)  + " <br> " + "Level 2: " + solutions.p2.toFixed(4)  + " <br>" + "Level 3: " + solutions.p3.toFixed(4)  + " <br> " + "Level 3 - OIS: " + solutions.p4.toFixed(4) )
};
console.log("hello")
        $(document).ready(function() {
            $("button#solve").click(function() {
                
                let coefficients = get_input();
                
                send_inputs_json(coefficients);
            })
})