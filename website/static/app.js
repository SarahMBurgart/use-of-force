


let get_input = function() {
    let Address = $("input#Address").val()
    let ICT = $("select#ICT").val()
    let Race = $("select#Race").val()
    let Gender = $("select#Gender").val()
    let Hour = $("select#Hour").val()
    let d = new Date()
    let dayofweek = d.getDay()
    let month = d.getMonth()
 
    return {'Address': Address,
            'ICT': ICT,
            'Race': Race,
            'Gender': Gender,
            "Hour": Hour,
            "dayofweek": dayofweek,
            "month": month,
            } 
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
  
    $("span#solution").html("<h4 >Predicted Probabilities:</h4><strong>No Force: </strong> " + solutions.p0.toFixed(6) + "   |   <strong>average:</strong> 0.994121" + "<br> <strong>Level 1: </strong> " +  solutions.p1.toFixed(6) + "   |   <strong>average:</strong> 0.004418" +" <br><strong>Level 2:</strong> " + solutions.p2.toFixed(6)  + "   |   <strong>average:</strong> 0.001415" + " <br>" + "<strong>Level 3:</strong> " + solutions.p3.toFixed(6)  + "   |   <strong>average:</strong> 0.000036" +" <br> " + "<strong>Level 4: </strong>" + solutions.p4.toFixed(6) +"   |   <strong>average:</strong> 0.000011"  )
};
console.log("hello")
        $(document).ready(function() {


            $("#button2").click(function() {
                send_thank_you()
            })

            $("button#solve").click(function() {
                
                let coefficients = get_input();
                
                send_inputs_json(coefficients);
            })
})

        $(document).ready(function() {
          
       
       
        } )
let send_thank_you = function() {
    email = $("#email").val()
    console.log(email) 

    $("#email").val("Thank you!");

    window.localStorage.setItem(email, email)
    // $.ajax({
    //     url: '/button-addon2',
    //     contentType: "application/json; charset=utf-8",
    //     type: 'POST',
    //     success: function(data) {
            
    //     },
    // }) 
};

