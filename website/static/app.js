


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

let display_solutions = function(solutions){
  
    $("span#solution").html("<em>Level 0:</em> " + solutions.p0.toFixed(4) + " <em>Level 1: </em> " +  solutions.p1.toFixed(4) + " <br><em>Level 2:</em> " + solutions.p2.toFixed(4)  + " <br>" + "<em>Level 3:</em> " + solutions.p3.toFixed(4)  + " <br> " + "<em>Level 3 - OIS: </em>" + solutions.p4.toFixed(4) )
};
console.log("hello")
        $(document).ready(function() {
            $("button#solve").click(function() {
                
                let coefficients = get_input();
                
                send_inputs_json(coefficients);
            })
})